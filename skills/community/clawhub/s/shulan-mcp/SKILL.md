---
name: shulan-data
description: 商业数据调研与报告生成。当用户需要行业数据、达人清单、招标汇总、企业洞察、招聘信号、舆情趋势，或需要把问题拆解为可执行的数据任务时使用。通过数懒（ShuLan）MCP 工具调用 AI 数据中台。
---

# 数懒数据调研（ShuLan Data Research）

使用数懒 AI 数据中台完成商业数据调研，并产出可执行的报告（达人清单、招标汇总、企业洞察、招聘信号、舆情监测）。

## 前置条件

- 已配置数懒 MCP Server（`shulan-mcp`），并在 https://shulan.io 开放平台生成 `sl_` 前缀 API Key
- 环境变量：`SHULAN_API_KEY`、`SHULAN_BASE_URL`（托管环境为 `https://shulan.io`）

## 可用工具

- `shulan_health` — 检查服务状态
- `shulan_create_task` — 创建数据调研任务（自动扣费，多退少不补）
- `shulan_get_task` — 查询任务状态与报告
- `shulan_market` — 查询报告市集
- `shulan_get_report` — 获取报告详情

## 工作流

1. **澄清需求**：确认地域、对象、时间窗口、期望交付物（清单/横评/ROI 模型）。
2. **拆解问题**：把一句话需求拆成「主题 + 范围 + 指标 + 时间」四要素。
3. **创建任务**：调用 `shulan_create_task`，传入 question 与可选 dataSources/cost。
4. **轮询结果**：调用 `shulan_get_task`，状态 `done` 后获取 `html_url`。
5. **解读交付**：向用户说明关键结论、置信度与数据来源；提醒 AI 生成内容标识与「多退少不补」结算规则。

## 注意事项

- 任务按实际成本结算，预估点数仅作参考；提示用户可在网页端查看明细。
- 数据来源以报告内「数据来源核验凭证」为准；演示构造模式会明确标注。
- 不承诺不存在的实时数据能力；涉及平台会员数据时使用聚合分析口径。

## Examples

```
Example usage or prompts
```

## Notes

- Additional notes or caveats
