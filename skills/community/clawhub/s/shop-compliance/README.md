# 🛒 Shop-Compliance — 中小商家电商合规快速筛查工具

5 分钟自查店铺合规风险，给出可立即执行的操作建议。

## 适用人群

电商平台上的中小商家、品牌方、个体店铺老板。**不需要法务背景，跟着问题回答就行。**

## 检查模块

| 模块 | 检查项 | 用时 |
|------|--------|:----:|
| 商品上架 | 极限词、资质、描述真实性 | ~1 分钟 |
| 消费者权益 | 退货、自动续费、投诉处理 | ~1.5 分钟 |
| 客户信息保护 | 数据共享、隐私面单、数据清理 | ~1.5 分钟 |
| 营销合规 | 直播话术、促销价格、短信营销 | ~1 分钟 |

## 快速使用

```bash
# 全量交互式检查（推荐）
python3 scripts/shop-compliance-check.py --interactive

# 只想查商品上架
python3 scripts/shop-compliance-check.py -s listing --interactive

# 保存报告
python3 scripts/shop-compliance-check.py -o my-report.html -f html
```

## 免费版 + Pro 版

本工具为免费版，覆盖 12 项核心检查。四个 Pro 版（即将推出）提供对应模块的深度检查。

## 免责声明

本工具仅供参考，不构成法律意见。请咨询专业律师确认合规状态。

## 许可证

MIT © 2026 Wei Wu (wwumit)
