---
name: travel-tax-refund
display_name: 旅行退税指南
description: 出境购物退税全流程指引助手；帮旅行者了解各国退税政策、计算退税金额、掌握退税流程和注意事项。当用户需要查询退税政策、退税流程、退税计算、免税店购物、境外购物退税时使用。
---

# 旅行退税指南

出境购物不花冤枉钱——帮你看懂退税政策、算清退税金额、走对退税流程。

## 能力概览

| 序号 | 工具 | 说明 |
|------|------|------|
| 1 | refund_policy | 查询目的地退税政策与流程 |
| 2 | calc_refund | 计算退税金额 |
| 3 | refund_tips | 退税注意事项与避坑指南 |

## 工作流程

1. 根据用户需求判断调用哪个工具
2. 执行 `python3 scripts/tax_refund.py <tool> '<json_params>'`
3. 解析JSON输出，以自然语言回复用户

## 工具参数说明

### refund_policy
查询目的地退税政策。参数：destination(必填，目的地国家)

### calc_refund
计算退税金额。参数：destination(必填), amount(必填，消费金额), currency(选填，货币代码，默认当地货币)

### refund_tips
退税注意事项与避坑指南。参数：scenario(选填，场景如机场/商店/海关)

## 数据说明

- 退税政策基于各国海关2026年公开标准
- 退税率为标准VAT税率，实际退税率可能因退税公司手续费略有差异
- 零配置，无需申请任何API Key
