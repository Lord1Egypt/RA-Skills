---
name: skill_quotation_engine
description: 智能报价引擎 — 根据设备清单和工时自动生成报价单
priority: P1
version: "1.0"
invocation_mode: both
preferred_provider: minimax
---
# 智能报价引擎

## 一、概述
根据演出项目的设备清单、工时、运输成本等自动计算并生成报价单。

## 二、使用示例
```python
from skill_quotation_engine import QuotationEngine
engine = QuotationEngine()
quote = engine.generate(show_data, labor_rate=500, transport_rate=2.0)
engine.export_pdf(quote, "quote.pdf")
```

## 三、报价组成
1. **设备租赁费** — 设备单价 × 天数
2. **人工费** — 技术人员 × 工时 × 费率
3. **运输费** — 距离 × 费率
4. **保险费** — 设备总值 × 保险率
5. **管理费** — 小计 × 管理费率

*版本: v1.0 | 创建: 2026-04-10*
