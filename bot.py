#!/usr/bin/env python3
"""
CryptoSignalBot
AI-powered cryptocurrency monitoring bot that tracks blockchain news,
Bitcoin and Ethereum market updates, DeFi trends, Web3 developments,
and digital asset insights in real time.
"""

import sys


def get_status(score: int) -> str:
    if score <= 30:
        return "Critical"
    elif score <= 60:
        return "At Risk"
    elif score <= 80:
        return "Healthy"
    return "Excellent"


def get_priority_action(scores: dict) -> str:
    labels = {
        "signal_strength": "Signal Strength",
        "sentiment": "Sentiment",
        "market_momentum": "Market Momentum",
        "volatility_risk": "Volatility Risk",
        "liquidity": "Liquidity",
    }
    lowest_key = min(scores, key=scores.get)
    return f"{labels[lowest_key]} ({scores[lowest_key]}/100 — act first)"


def get_recommendation(overall: int, signal_type: str) -> str:
    stype = signal_type.upper()
    if overall >= 81:
        action = "BUY" if stype == "BULLISH" else "SELL" if stype == "BEARISH" else "SIGNAL"
        return f"STRONG {action} — High confidence signal"
    elif overall >= 61:
        action = "BUY" if stype == "BULLISH" else "SELL" if stype == "BEARISH" else "WATCH"
        return f"{action} — Moderate confidence signal"
    elif overall >= 31:
        return "CAUTION — Weak signal, wait for confirmation"
    return "AVOID — Low confidence signal"


def analyze_signal(
    asset: str,
    signal_type: str = "bullish",
    signal_strength: int = 88,
    sentiment: int = 75,
    market_momentum: int = 82,
    volatility_risk: int = 70,
    liquidity: int = 90,
) -> dict:
    """
    Analyze and score cryptocurrency signals.

    Args:
        asset: Cryptocurrency ticker (BTC, ETH, etc.)
        signal_type: Type of signal — bullish, bearish, neutral, breakout, reversal
        signal_strength: Signal strength score (0-100)
        sentiment: Market sentiment score (0-100)
        market_momentum: Market momentum score (0-100)
        volatility_risk: Volatility risk score (0-100)
        liquidity: Liquidity score (0-100)

    Returns:
        dict with individual signal scores, overall score, and recommendation
    """
    scores = {
        "signal_strength": signal_strength,
        "sentiment": sentiment,
        "market_momentum": market_momentum,
        "volatility_risk": volatility_risk,
        "liquidity": liquidity,
    }
    overall_signal_score = round(sum(scores.values()) / 5)

    return {
        "asset": asset,
        "signal_type": signal_type.capitalize(),
        "signal_strength_score": signal_strength,
        "sentiment_score": sentiment,
        "market_momentum_score": market_momentum,
        "volatility_risk_score": volatility_risk,
        "liquidity_score": liquidity,
        "overall_signal_score": overall_signal_score,
        "priority_action": get_priority_action(scores),
        "recommendation": get_recommendation(overall_signal_score, signal_type),
    }


if __name__ == "__main__":
    asset = sys.argv[1] if len(sys.argv) > 1 else "BTC"
    signal_type = sys.argv[2] if len(sys.argv) > 2 else "bullish"
    signal_strength = int(sys.argv[3]) if len(sys.argv) > 3 else 88
    sentiment = int(sys.argv[4]) if len(sys.argv) > 4 else 75
    market_momentum = int(sys.argv[5]) if len(sys.argv) > 5 else 82
    volatility_risk = int(sys.argv[6]) if len(sys.argv) > 6 else 70
    liquidity = int(sys.argv[7]) if len(sys.argv) > 7 else 90

    result = analyze_signal(
        asset, signal_type, signal_strength,
        sentiment, market_momentum, volatility_risk, liquidity
    )

    print(f"Asset: {result['asset']}")
    print(f"Signal Type: {result['signal_type']}")
    print("=" * 45)
    print(f"Signal Strength Score:         {result['signal_strength_score']}/100  [{get_status(result['signal_strength_score'])}]")
    print(f"Sentiment Score:               {result['sentiment_score']}/100  [{get_status(result['sentiment_score'])}]")
    print(f"Market Momentum Score:         {result['market_momentum_score']}/100  [{get_status(result['market_momentum_score'])}]")
    print(f"Volatility Risk Score:         {result['volatility_risk_score']}/100  [{get_status(result['volatility_risk_score'])}]")
    print(f"Liquidity Score:               {result['liquidity_score']}/100  [{get_status(result['liquidity_score'])}]")
    print("=" * 45)
    print(f"Overall Signal Score:          {result['overall_signal_score']}/100")
    print(f"Priority Action:               {result['priority_action']}")
    print(f"Recommendation:                {result['recommendation']}")
