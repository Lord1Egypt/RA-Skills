---
name: yandun-position-sizer
description: 研盾Skill — 仓位计算、止损/止盈策略、风险预算分配
---
# 研盾 · 仓位计算与止损策略 (yandun-position-sizer)
> **⚠️ 数据来源与限制（重要披露）：**
> 本Skill为课程教学演示：仓位比例、止损止盈位基于输入的风险评分与**内置演示计算规则**生成，输出为教学示例并标注「演示输出」。
> 结果不构成真实仓位/止损建议，不构成投资建议。



## 功能
1. **仓位计算** — 基于风险评分和可用资金计算建议仓位
2. **止损/止盈设定** — 根据波动率和支撑/压力位设定止损止盈位
3. **风险预算分配** — 多标的下按风险预算分配仓位比例
4. **组合风险汇总** — 整体组合风险暴露评估

## 核心逻辑
```
风险评分 → 仓位系数 → 建议仓位 = 总资金 × 仓位系数
波动率 → 止损幅度 → 止损价 = 现价 × (1 - 止损%)
技术位 + 波动率 → 综合止损位（取更严格者）
```

## 调用方式
```bash
python3 {baseDir}/scripts/calc_position.py [--codes sh600519,sz300750] [--capital 1000000] [--output json|text]
```

## 输出示例
```json
{
  "date": "2026-07-03",
  "total_capital": 1000000,
  "positions": {
    "sh600519": {
      "name": "贵州茅台",
      "risk_level": "中低",
      "suggested_pct": 20,
      "suggested_amount": 200000,
      "stop_loss": 1120.00,
      "stop_loss_pct": -6.2,
      "take_profit": 1300.00,
      "take_profit_pct": 8.8
    }
  },
  "portfolio_summary": {
    "total_risk_score": 32,
    "max_single_position": 20,
    "suggested_cash_ratio": 20
  }
}
```
