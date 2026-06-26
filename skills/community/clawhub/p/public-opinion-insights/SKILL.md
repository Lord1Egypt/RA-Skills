---
name: public-opinion-insights
description: 调用 Midu 舆情分析接口，针对指定主体进行指定维度的舆情分析。分析维度包括：['事件概况', '事件进程', '信息总量', '传播速度', '热搜情况', '跨平台传播', '媒体报道情况', 'KOL参与情况', '传播层级', '热门信息', '情绪烈度', '媒体观点分析', 'KOL观点分析', '网民观点分析', '行业专家观点分析', 'AI虚假信息识别', '已认定谣言传播', '研判建议', '活跃作者', '地域分布图', '关键词云', '信息来源分布', '全网信息走势图', '敏感信息占比', '事件盘点', '网民反馈情况', '分职能信息传播情况', '分区域信息传播情况', '总量', '环比', '占比/分布', '同比', '舆论诉求分析', '观点指向分析', '观点倾向指向分析', '同类案例', '关键传播节点', '溯源分析', '应对效果评估', '热度指数', '热度指数排行', '关键词方案'] Call the Midu public opinion insights API for public-opinion analysis.
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"], "env": ["MIDU_API_KEY"] }, "primaryEnv": "MIDU_API_KEY" } }
---

# Public Opinion Insights

调用内部舆情分析服务，返回针对用户问题的**结构化洞察结论**（通常为 Markdown 等文本）。本技能聚焦于 **[references/analysis_dimension.md](references/analysis_dimension.md)** 中列出的分析维度，而非撰写完整「舆情报告」长文档。

## Prerequisites

### API Key Configuration

本技能需要在 OpenClaw 中配置 **MIDU_API_KEY**。

若尚未获取 Key，请访问：

**http://intra-znjs-yqt-agent-wx-beta.midu.cc/apiKey**

详细配置说明见：

[references/apikey-fetch.md](references/apikey-fetch.md)

## Usage

```bash
python3 skills/public-opinion-insights/scripts/insights.py '<JSON>'
```

### Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| message | str | yes | - | 分析需求描述：须说明对象（事件/话题/主体等），并指明要查看的维度（可参考 [analysis_dimension.md](references/analysis_dimension.md)） |

### 与 public-opinion-report 的关系

- **相同**：服务根地址、`/api/chat` 调用方式、鉴权与环境变量、`MIDU_API_KEY` 配置方式。
- **不同**：本技能用于**按需拆维度做洞察**；`public-opinion-report` 用于**生成整篇舆情分析报告**。用户要「长报告」时用 report；要「某一类指标/模块结论」时用本技能。

### Examples

```bash
# 单个维度
python3 skills/public-opinion-insights/scripts/insights.py '{"message":"就「某某事件」分析网民观点"}'

```


### ⚠️ Important: Timeout Configuration

- 接口响应时间因任务复杂度而异，复杂分析可能需要较长时间。脚本已对 `/api/chat` 使用较长超时，使用者侧代理/网关也需预留足够等待时间。

## 可分析维度（清单）

完整维度列表见 **[references/analysis_dimension.md](references/analysis_dimension.md)**；API Key 配置见 **[references/apikey-fetch.md](references/apikey-fetch.md)**。向 `message` 中写入自然语言即可，无需与清单字面完全一致，但**点名维度**有助于返回更聚焦的结果。

## ⚠️ Critical Notes

- **单请求原则**：发送请求后，在响应返回前不要重复发送测试或并发请求。
- **等待时长**：分析可能需要数分钟量级，请勿过早中断。
