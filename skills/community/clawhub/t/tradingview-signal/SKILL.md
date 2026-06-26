# TradingView Signal Parser Skill

## Description
Parse and analyze TradingView signals. Extract trading ideas from TradingView links or text, and provide structured analysis including entry price, stop loss, take profit, and risk/reward ratio.

## Usage
```javascript
const result = await callSkill('tradingview-signal', {
  signal: "BTCUSD long from 42000, stop loss 40000, target 45000",
  // OR a TradingView URL
  url: "https://www.tradingview.com/chart/..."
});
```

## Features
- Parse TradingView signal text
- Extract: symbol, direction (long/short), entry, stop loss, take profit
- Calculate risk/reward ratio
- Provide trade analysis

## Price
0.001 USDT per request (paid via SkillPay)

## Integration
- Billing: SkillPay.me
- API Key: sk_4312778b58aa7c81c15bd0e2b4fe544e12ca9e765f0deab630a50ecd4daf4ac2
