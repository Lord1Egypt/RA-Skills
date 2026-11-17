# AI辅助接口

## AI行业搜索

接口：`industryReasoning`

输入行业关键词，返回行业编码候选。适用于补充或校验普通搜索的 `industryCode`，不是项目搜索接口。

```text
行业名称 -> industryReasoning -> 行业编码 -> 普通搜索
```

## 招中标分类推理

接口：`categoryReasoning`

输入项目标题和正文，推理招中标 14 类信息分类。结果是 AI 推断，用于分类补充、质量校验或历史数据处理，不能覆盖官方 `projectClassID` 而不留痕。

## LLM项目结构化

接口：`ztbAiStructureInfo`

输入消息，适用于官方结构化详情缺失或需要从正文抽取更多字段的情况，例如金额统一转人民币元、座机补全区号、提取评标专家职业和专业方向。

必须区分：

```text
官方结构化数据 != AI推理结构化数据
```

## AI专用搜索

接口：`SearchProjectForAI`

适合简单自然语言快速搜索。复杂查询仍优先采用 `aiSearchSubmitPolling` 完成条件编译后调用普通搜索。
