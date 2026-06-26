---
name: med-pre-existing-review
description: 理赔既往症审核。由调用方传入完整题干（病历/材料 + 关系类型与报销结论格式），经内部医疗大模型判断其他诊断与主诊断关系及是否报销；仅含 scripts/run.py，无 _shared 依赖。
metadata:
  {
    "openclaw":
      {
        "emoji": "📋"
      }
  }
---

# 既往症审核

## 概述

面向理赔材料中的**病历叙述或 OCR 文书**，在调用方给定的分类下，判断**其他诊断与主诊断的关系**（常见为 **并发症 / 疑似既往症 / 无关疾病**）并给出**是否报销**（**报销 / 不报销**），按题干规定的**固定行格式**输出。

本 skill **直连公司内部医疗大模型**，输入输出约定与 `insurance/claims-review/chronic-injury` 等脚本一致；不替代承保条款与人工核赔结论。

## 数据与合规

- 姓名、证件号、账户等须在调用方侧**脱敏**后再组题干；本脚本默认不落盘输入（除非 `--output`）。
- 输出为辅助审核意见，**不构成**法律或最终理赔决定。

## 题目输入（三选一）

1. **`--question`**：完整题干。  
2. **`--input PATH`**：`.json` / `.jsonl` 为对象或**单元素对象数组**；须含 **`input`** 或 **`question`**。纯文本文件则整段作为题干。`-` 表示 stdin。  
3. **stdin**：非 TTY 时同 `-`。

可选 **`meta`** / **`other`**：透传至结果 JSON 的 `meta` 字段。

## 典型题干结构（由调用方拼装）

- 病历或材料摘录（可含 OCR 噪声）  
- 关系类型与是否报销的**枚举说明**  
- 严格输出模板（三行：`关系类型：` / `是否报销：` / `判断依据：`）

## 运行结果

默认可解析 JSON：`skill` 为 `既往症审核`，`status` 为 `ok`，`answer` 为模型文本，`question` 为本次用户消息全文。

## 用法

```bash
python3 scripts/run.py --input case.json --appkey YOUR_KEY
```

## 参数

与 `chronic-injury` 相同：`--question`、`--input`、`--appkey`、`--dry-run`、`--index`、`--match-id`、`--batch`、`--model`、`--api-url`、`--temperature`、`--timeout`、`--system-prompt`、`--output`、`--text-only`。

## 模型

默认 `u1-insuremed`，`https://maas-api.hivoice.cn/v1/chat/completions`。
