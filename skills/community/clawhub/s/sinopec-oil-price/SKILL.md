---
name: sinopec-oil-price
description: |
  中石化油价查询 Skill，用于查询实时油价信息。支持按省份查询汽油和柴油价格，显示价格变动信息。
metadata:
  {
    "openclaw": {
      "emoji": "⛽",
      "tools": [
        {
          "name": "sinopec_oil_price_get",
          "description": "获取中石化油价信息",
          "parameters": {
            "type": "object",
            "properties": {
              "province_id": {
                "type": "string",
                "description": "省份ID，不传则使用默认定位"
              },
              "province_name": {
                "type": "string",
                "description": "省份名称（如'北京'、'上海'），与province_id二选一"
              }
            },
            "additionalProperties": false
          },
          "returns": {
            "type": "object",
            "description": "油价数据对象"
          }
        }
      ]
    }
  }
---

# Sinopec Oil Price Skill

查询中国石化实时油价信息。

## Quick Start

This skill provides access to Sinopec's official oil price data.

**Core tool**: `sinopec_oil_price_get`

Use when:
- User asks for today's oil prices
- User wants prices for a specific province/city
- User needs gasoline (92#, 95#, 98#) or diesel (0#) prices
- User wants to see price changes

## Usage

See detailed documentation in bundled references:

- **[API Reference](references/api.md)** - Complete API documentation
- **[Usage Examples](references/examples.md)** - Code patterns and common scenarios

## Notes

- Prices in CNY per liter
- Data from Sinopec official mobile API
- Prices may vary at actual gas stations
