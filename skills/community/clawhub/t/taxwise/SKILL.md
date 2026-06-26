---
name: taxwise
version: 1.0.0
description: >
  中国中小企业智能财税技能。Trigger when user mentions: 税率, 报税, 发票, 记账, 财税,
  税务, 增值税, 企业所得税, 个税, 财务分析, 税务筹划, 合规检查, 纳税申报, 税收优惠,
  小规模纳税人, 一般纳税人, 附加税, 印花税, 房产税, 发票识别, 报销, 费用归类,
  利润表, 资产负债表, 现金流量表, 税负率. Supports freemium: free (税率查询/发票识别/基础记账)
  and premium (智能报税/财务分析/合规检查/税务筹划).
---

# TaxWise — 智能财税

面向中国中小企业的智能财税助手。

## 功能分级

| 功能 | 等级 | 脚本 |
|------|------|------|
| 税率查询 | 免费 | `scripts/tax_query.py` |
| 发票识别 | 免费 | `scripts/invoice_ocr.py` |
| 基础记账 | 免费 | `scripts/bookkeeping.py` |
| 智能报税 | 付费 | `scripts/tax_filing.py` |
| 财务分析 | 付费 | `scripts/financial_analysis.py` |
| 合规检查 | 付费 | `scripts/compliance_check.py` |
| 税务筹划 | 付费 | `scripts/tax_planning.py` |

## 使用流程

### 1. 税率查询（免费）

```bash
python3 scripts/tax_query.py <税种> [--纳税人类型 <小规模|一般>] [--地区 <省份>]
```

支持的税种：增值税、企业所得税、个人所得税、附加税、印花税、房产税、消费税、关税。

### 2. 发票识别（免费）

```bash
python3 scripts/invoice_ocr.py <发票图片路径>
```

支持增值税普通发票、专用发票、电子发票。输出结构化字段（发票代码、号码、金额、税额等）。

如需真实OCR，接入百度OCR API或阿里云OCR（替换mock模式）。

### 3. 基础记账（免费）

```bash
python3 scripts/bookkeeping.py --action <add|list|summary> [--date YYYY-MM-DD] [--category <类别>] [--amount <金额>] [--desc <描述>]
```

类别：收入、办公费、差旅费、工资、采购、服务费、其他。
数据存储在 `scripts/bookkeeping_data.json`。

### 4. 智能报税（付费）

```bash
python3 scripts/tax_filing.py --period <YYYY-MM> [--纳税人类型 <小规模|一般>]
```

计算应纳税额，生成申报表草稿。包含：增值税、附加税、企业所得税（季度）、个人所得税（月度）。

### 5. 财务分析（付费）

```bash
python3 scripts/financial_analysis.py [--data-file <路径>] [--period <YYYY-MM>]
```

生成利润表摘要、税负率分析、同比环比对比。输出Markdown报告。

### 6. 合规检查（付费）

```bash
python3 scripts/compliance_check.py [--data-file <路径>] [--period <YYYY-MM>]
```

检查税务合规风险：逾期申报、税负率异常、发票异常、税收优惠未享受等。

### 7. 税务筹划（付费）

```bash
python3 scripts/tax_planning.py [--data-file <路径>] [--纳税人类型 <小规模|一般>]
```

提供节税建议：纳税人身份选择、税收优惠政策、费用扣除优化等。

## 税种参考

详细中国税种、税率、政策 → `references/china_tax_rates.md`

## API 集成

当前使用Mock数据。生产环境替换方式：

| 功能 | 推荐API | 替换位置 |
|------|---------|----------|
| 发票OCR | 百度AI / 阿里云OCR | `scripts/invoice_ocr.py` 的 `_ocr_mock()` |
| 实时税率 | 国家税务总局API | `scripts/tax_query.py` 的 `TAX_RATES` 常量 |
| 企业征信 | 企查查/天眼查API | `scripts/compliance_check.py` |

## 注意事项

- 所有计算结果仅供参考，不构成税务建议
- 提醒用户最终以税务机关为准
- 付费功能需确认用户已开通相应服务
