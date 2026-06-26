# Zonein Data Schema Reference

## Prediction Market (Polymarket)

### Leaderboard Entry
```json
{
  "wallet": "0x...",
  "proxyWallet": "0x...",
  "userName": "trader_name",
  "profileImage": "https://...",
  "rank": 1,
  "pnl": 50000.0,
  "vol": 200000.0,
  "period": "WEEK",
  "category": "OVERALL"
}
```

### Trader / User
```json
{
  "wallet": "0x...",
  "username": "trader_name",
  "pfp": "https://...",
  "score": 85.5,
  "labels": ["smart_money", "whale", "consistent_winner"],
  "stats": {
    "total_trades": 150,
    "win_rate": 0.68,
    "roi": 0.45,
    "volume": 500000,
    "avg_hold_hours": 48
  }
}
```

### Trader Performance (pre-calculated)
```json
{
  "wallet": "0x...",
  "username": "trader_name",
  "overall": {
    "pnl": 50000,
    "volume": 200000,
    "roi": 0.25,
    "positions_count": 12
  },
  "best_category": "POLITICS",
  "category_stats": [
    {"category": "POLITICS", "pnl": 30000, "volume": 100000, "roi": 0.30},
    {"category": "CRYPTO", "pnl": 20000, "volume": 100000, "roi": 0.20}
  ]
}
```

### Position (PM)
```json
{
  "wallet": "0x...",
  "slug": "will-trump-win-2024",
  "eventSlug": "presidential-election-2024",
  "conditionId": "0x...",
  "title": "Will Trump win the 2024 election?",
  "outcome": "Yes",
  "outcomeIndex": 0,
  "size": 5000.0,
  "avgPrice": 0.45,
  "curPrice": 0.62,
  "totalBought": 5000.0,
  "category": "POLITICS",
  "endDate": "2024-11-05T00:00:00Z",
  "icon": "https://..."
}
```

### PM Signal (consensus-based)
```json
{
  "market_slug": "will-btc-hit-100k",
  "condition_id": "0x...",
  "title": "Will BTC hit $100k by end of 2024?",
  "direction": "YES",
  "consensus": 0.85,
  "total_wallets": 8,
  "yes_wallets": 7,
  "no_wallets": 1,
  "yes_size": 45000.0,
  "no_size": 3000.0,
  "cur_yes_price": 0.42,
  "cur_no_price": 0.58,
  "best_rank": 5,
  "category": "CRYPTO",
  "end_date": "2024-12-31T00:00:00Z"
}
```

## Perp Trading (HyperLiquid)

### Smart Trader
```json
{
  "address": "0x...",
  "smart_trader_score": 85.5,
  "smart_trader_metrics": {
    "win_rate": 0.72,
    "profit_factor": 2.5,
    "avg_trade_duration": 48,
    "max_drawdown": 0.15
  },
  "categories": ["whale", "momentum_trader"],
  "account_value": 500000.0,
  "perp_month_pnl": 50000.0,
  "perp_week_pnl": 12000.0,
  "perp_day_pnl": 3000.0,
  "current_positions": {
    "asset_positions": [
      {
        "position": {
          "coin": "BTC",
          "szi": 0.5,
          "entryPx": 95000.0,
          "positionValue": 47500.0,
          "unrealizedPnl": 1200.0,
          "leverage": {"value": 3.0}
        }
      }
    ]
  }
}
```

### Perp Signal (consensus-based)
```json
{
  "coin": "BTC",
  "direction": "LONG",
  "consensus": 0.82,
  "total_wallets": 15,
  "long_wallets": 12,
  "short_wallets": 3,
  "long_value": 2500000.0,
  "short_value": 300000.0,
  "avg_entry_long": 95500.0,
  "avg_entry_short": 96200.0,
  "best_trader_score": 92.0
}
```

### Coin Distribution
```json
{
  "BTC": {
    "long_count": 45,
    "short_count": 12,
    "total_value": 5000000.0,
    "wallet_count": 57
  }
}
```

## Agent Management

### Agent Config (V2 — Perp Trading)
```json
{
  "agent_id": "agent_abc12345",
  "name": "Momentum Hunter",
  "domain": "trading",
  "agent_type": "momentum_hunter",
  "trading_style": "momentum",
  "description": "Momentum-based trading following high win rate smart wallets",
  "enabled": true,
  "status": "enabled",
  "execution_mode": "auto",
  "allowed_assets": ["BTC", "ETH", "SOL"],
  "smart_money_categories": ["high_risk_high_return", "momentum_trader", "short_term_trading"],
  "llm": {
    "provider": "deepseek",
    "model": "deepseek-v3-1-250821"
  },
  "model_provider": "deepseek",
  "model_name": "deepseek-v3-1-250821",
  "signal_weights": {"sm": 40, "ta": 35, "market": 25},
  "trading_risk": {
    "max_positions": 5,
    "max_position_size_pct": 15,
    "default_stop_loss_pct": 1.0,
    "default_take_profit_pct": 2.0,
    "max_leverage": 5,
    "min_confidence": 0.7
  },
  "trigger_conditions": {
    "entry": {
      "long": {"op": "and", "conditions": [
        {"field": "sm.long_ratio", "compare": ">=", "value": 55},
        {"field": "sm.wallet_count", "compare": ">=", "value": 3},
        {"field": "ta.4h.rsi", "compare": "<=", "value": 65},
        {"field": "market.taker_buy_sell_ratio", "compare": ">", "value": 0.505}
      ]},
      "short": {"op": "and", "conditions": [
        {"field": "sm.short_ratio", "compare": ">=", "value": 55},
        {"field": "sm.wallet_count", "compare": ">=", "value": 3},
        {"field": "ta.4h.rsi", "compare": ">=", "value": 35},
        {"field": "market.taker_buy_sell_ratio", "compare": "<", "value": 0.495}
      ]}
    },
    "exit": {
      "close_long": {"op": "or", "conditions": [
        {"field": "sm.short_ratio", "compare": ">=", "value": 60},
        {"field": "ta.4h.rsi", "compare": ">=", "value": 75}
      ]},
      "close_short": {"op": "or", "conditions": [
        {"field": "sm.long_ratio", "compare": ">=", "value": 60},
        {"field": "ta.4h.rsi", "compare": "<=", "value": 25}
      ]}
    }
  },
  "prompt_config": {
    "trading_strategy": "Momentum-based trading following high win rate smart wallets.",
    "custom_rules": "Enter LONG: SM long_ratio >=55%, >=3 wallets, RSI <=65, taker ratio >0.505.",
    "risk_management": "1:2 risk-reward ratio. Stop-loss at 1%, take-profit at 2%."
  },
  "withdrawal_addresses": ["0x596b6B0b395b9BE4C3a03e371A5E3884D94C91Dd"],
  "risk_profile": {
    "max_daily_loss": 3,
    "risk_per_trade_percent": 1,
    "risk_reward_ratio": "1:2",
    "max_account_leverage": 5
  },
  "strength_thresholds": {
    "BTC": {"min_strength_buy": 70, "min_strength_sell": 65},
    "ETH": {"min_strength_buy": 75, "min_strength_sell": 65}
  },
  "timeframe_weights": {"24h": 0.5, "4h": 0.35, "1h": 0.15},
  "dsl_config": {
    "enabled": true,
    "phase1_retrace": 0.3,
    "phase1_absolute_floor_pct": 0.5,
    "phase2_trigger_roe": 2.0,
    "phase2_lock_pct": 0.5,
    "phase3_trigger_roe": 5.0,
    "phase3_trailing_pct": 0.3
  }
}
```

### Agent Stats (via AgentsArena)
```json
{
  "total_trades": 45,
  "successful_trades": 28,
  "win_rate": 0.622,
  "total_pnl": 1250.50,
  "total_volume": 8500.0,
  "profit_factor": 2.5,
  "sharpe_ratio": 1.8,
  "max_drawdown": 0.15
}
```
