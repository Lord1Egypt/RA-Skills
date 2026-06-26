---
name: recognize_intent
slug: recognize_intent
version: 1.0.2
description: 识别自然语言的意图类别并解析其中的语义，包括指标和维度，例如："今天的缤果店的业绩如何 " ,将提取指标：订单成交额（业绩） ，维度：年月日-今天（2026-03-10） ，店铺-缤果店 ...
metadata: {"clawdbot":{"emoji":"🐬"}}
---
# Skill: recognize_intent
- Description: 识别意图类别及初步实体。
- Inputs: [rewritten_query]（从 `skills/.workflow/rewrite_output.json` 读取）
- Outputs: [intent, indicator_metric, metric_info]（写入 `skills/.workflow/intent_output.json`）

- ID: recognize_intent

- Role: 意图路由网关
    - 功能描述：对重写后的问题进行语义分类，识别任务类型并初步提取核心维度信息。
    - 输入参数：
      - rewritten_query (string): 来自 rewrite_output.json 的 final_query。
    - 输出结果：
      - intent (enum): handle_data_query | handle_metadata_query | attribution_analysis | other。
      - indicator_metric (list): 指标 + 维度数据。
      - mode (string): single | multi。
    - 执行策略：若 confidence < 0.7，强制触发 clarify_workflow（澄清流程）。

## 注入服务（通过 `.env` 配置）

| 服务类 | 作用 | .env 关键配置 |
|--------|------|---------------|
| `_RealIndicatorSearcher` | 指标别名向量搜索（Milvus `indicator_alias`） | `MILVUS_*`, `EMBEDDING_*`, `INDICATOR_ALIAS_COLLECTION_NAME` |
| `_RealMetricConfigLoader` | 指标维度配置（MySQL `indicator_metric`） | `INTENT_MYSQL_*` 或 `MYSQL_*` |
| `_RealDictValueReplacer` | 字典值替换（Milvus `sys_dict`） | `SYS_DICT_COLLECTION_NAME`（默认 `sys_dict`）, `DICT_REPLACE_MIN_SCORE`（默认 `0.50`） |
| `_RealSemanticConceptExtractor` | L1 语义概念抽取 + semantic_logic_dict 向量增强 | `SEMANTIC_LOGIC_COLLECTION`（默认 `semantic_logic_dict`）, `SEMANTIC_LOGIC_MIN_SCORE`（默认 `0.80`） |

所有服务连接失败时均自动降级为 `None`，主流程继续运行（仅跳过对应增强步骤）：
- `_RealDictValueReplacer` 失败 → 跳过中文值替换
- `_RealSemanticConceptExtractor` 失败 → 跳过 L1/L2 候选融合，直接使用 L2 槽位结果

## 独立运行说明

```bash
# 前置：先运行 rewrite_question.py 生成 rewrite_output.json
python ../rewrite-question/rewrite_question.py --query "今天汉河店的成交额"

# 运行意图识别（从 .workflow/rewrite_output.json 自动读取）
python recognize_intent.py

# 带清理（清除本步及后续输出，防止旧数据污染）
python recognize_intent.py --clean
```

### 下一步
```bash
python ../mult-call/multi_call.py
```
