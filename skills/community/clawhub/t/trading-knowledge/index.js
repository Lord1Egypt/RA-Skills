/**
 * Trading Knowledge - Reference Module
 * 
 * This skill provides comprehensive trading knowledge
 * for technical analysis and market structure
 */

const knowledge = {
  kline: {
    basics: "K-line (candlestick) shows OHLC data",
    patterns: {
      hammer: "Bullish reversal - long lower wick",
      shootingStar: "Bearish reversal - long upper wick",
      doji: "Indecision - open equals close"
    }
  },
  
  supportResistance: {
    definition: "Support = buying pressure, Resistance = selling pressure",
    rules: [
      "More tests = stronger level",
      "Volume confirms validity",
      "Broken support becomes resistance"
    ]
  },
  
  liquidityHunting: {
    definition: "Market makers hunt stop losses before reversal",
    pattern: [
      "Price approaches liquidity pool",
      "Quick spike to grab stops",
      "Rapid reversal",
      "Original direction continues"
    ]
  },
  
  signalK: {
    definition: "Reversal candle at key level",
    validity: [
      "Must be at support/resistance",
      "Long wick (>2x body)",
      "Small body",
      "Volume confirmation"
    ]
  },
  
  marketMaker: {
    activities: [
      "Provide liquidity",
      "Capture spread",
      "Hunt excess liquidity"
    ]
  },
  
  fundamentalVsTechnical: {
    fundamental: "WHAT to trade - economic data, news, metrics",
    technical: "WHEN to trade - price action, patterns, indicators"
  },
  
  volumeAnalysis: {
    healthy: "Price up + high volume",
    divergence: "Price up + low volume = warning",
    panic: "Price down + high volume = potential bottom"
  }
};

// Get knowledge by topic
function getKnowledge(topic) {
  return knowledge[topic] || "Topic not found";
}

// Get all topics
function getTopics() {
  return Object.keys(knowledge);
}

module.exports = {
  getKnowledge,
  getTopics,
  knowledge
};
