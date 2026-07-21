#!/usr/bin/env node

interface SignalInput {
  asset: string;
  signalType: string;
  signalStrength: number;
  sentiment: number;
  marketMomentum: number;
  volatilityRisk: number;
  liquidity: number;
}

interface SignalOutput {
  asset: string;
  signalType: string;
  signalStrengthScore: number;
  sentimentScore: number;
  marketMomentumScore: number;
  volatilityRiskScore: number;
  liquidityScore: number;
  overallSignalScore: number;
  priorityAction: string;
  recommendation: string;
}

function getStatus(score: number): string {
  if (score <= 30) return "Critical";
  if (score <= 60) return "At Risk";
  if (score <= 80) return "Healthy";
  return "Excellent";
}

function getPriorityAction(scores: Record<string, number>): string {
  const labels: Record<string, string> = {
    signalStrength: "Signal Strength",
    sentiment: "Sentiment",
    marketMomentum: "Market Momentum",
    volatilityRisk: "Volatility Risk",
    liquidity: "Liquidity",
  };
  const lowest = Object.entries(scores).reduce((a, b) => a[1] < b[1] ? a : b);
  return `${labels[lowest[0]]} (${lowest[1]}/100 — act first)`;
}

function getRecommendation(overall: number, signalType: string): string {
  const type = signalType.toUpperCase();
  if (overall >= 81) return `STRONG ${type === "BULLISH" ? "BUY" : type === "BEARISH" ? "SELL" : "SIGNAL"} — High confidence signal`;
  if (overall >= 61) return `${type === "BULLISH" ? "BUY" : type === "BEARISH" ? "SELL" : "WATCH"} — Moderate confidence signal`;
  if (overall >= 31) return `CAUTION — Weak signal, wait for confirmation`;
  return `AVOID — Low confidence signal`;
}

export function analyzeSignal(input: SignalInput): SignalOutput {
  const scores = {
    signalStrength: input.signalStrength,
    sentiment: input.sentiment,
    marketMomentum: input.marketMomentum,
    volatilityRisk: input.volatilityRisk,
    liquidity: input.liquidity,
  };
  const overallSignalScore = Math.round(
    Object.values(scores).reduce((a, b) => a + b, 0) / 5
  );
  return {
    asset: input.asset,
    signalType: input.signalType.charAt(0).toUpperCase() + input.signalType.slice(1),
    signalStrengthScore: input.signalStrength,
    sentimentScore: input.sentiment,
    marketMomentumScore: input.marketMomentum,
    volatilityRiskScore: input.volatilityRisk,
    liquidityScore: input.liquidity,
    overallSignalScore,
    priorityAction: getPriorityAction(scores),
    recommendation: getRecommendation(overallSignalScore, input.signalType),
  };
}

const args = process.argv.slice(2);
const asset = args[0] || "BTC";
const signalType = args[1] || "bullish";
const signalStrength = parseInt(args[2]) || 88;
const sentiment = parseInt(args[3]) || 75;
const marketMomentum = parseInt(args[4]) || 82;
const volatilityRisk = parseInt(args[5]) || 70;
const liquidity = parseInt(args[6]) || 90;

const result = analyzeSignal({
  asset, signalType, signalStrength,
  sentiment, marketMomentum, volatilityRisk, liquidity,
});

console.log(`Asset: ${result.asset}`);
console.log(`Signal Type: ${result.signalType}`);
console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
console.log(`Signal Strength Score:         ${result.signalStrengthScore}/100  [${getStatus(result.signalStrengthScore)}]`);
console.log(`Sentiment Score:               ${result.sentimentScore}/100  [${getStatus(result.sentimentScore)}]`);
console.log(`Market Momentum Score:         ${result.marketMomentumScore}/100  [${getStatus(result.marketMomentumScore)}]`);
console.log(`Volatility Risk Score:         ${result.volatilityRiskScore}/100  [${getStatus(result.volatilityRiskScore)}]`);
console.log(`Liquidity Score:               ${result.liquidityScore}/100  [${getStatus(result.liquidityScore)}]`);
console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
console.log(`Overall Signal Score:          ${result.overallSignalScore}/100`);
console.log(`Priority Action:               ${result.priorityAction}`);
console.log(`Recommendation:                ${result.recommendation}`);
