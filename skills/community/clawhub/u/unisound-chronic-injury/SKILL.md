---
name: med-chronic-injury-review
description: 理赔陈旧伤审核。由调用方传入完整题干（常见为影像报告 + 指定部位 + 输出格式），经内部医疗大模型判断伤情类别；仅含 scripts/run.py，无 _shared 依赖。
metadata:
  {
    "openclaw":
      {
        "emoji": "🦴"
      }
  }
---

# 陈旧伤审核

## 概述

面向**理赔材料中的影像/检查报告文字**（可由 OCR 或人工整理），在调用方给定的分类体系下（常见为 **陈旧伤 / 新伤 / 无伤 / 未提及**），对**指定解剖部位**做出伤情类别判断，并按题干要求的**固定行格式**输出。

本 skill **不接院内 PACS**，题干由上游拼装；与慢病/大病审核（走后端业务接口）不同，本包**直连公司内部医疗大模型**，接口与参数约定同 `medbench` 类评测脚本。

## 数据与合规

- 送入模型前应对姓名、证件号、影像号等做**脱敏**（由调用方完成）；本脚本不落盘用户内容（除非使用 `--output` 显式保存结果）。
- 输出为辅助审核意见，**不构成**法医鉴定或最终理赔决定。

## 题目输入（三选一）

1. **`--question`**：完整题干字符串。  
2. **`--input PATH`**：  
   - `.json` / `.jsonl`：根为**对象**，或**仅含 1 个对象的 JSON 数组**；对象须含非空 **`input`** 或 **`question`**。  
   - 其他扩展名：整文件 UTF-8 纯文本作为题干。  
   - 传 `-` 时从 stdin 读。  
3. **stdin**（未传 `--question` / `--input`、且非 TTY）：规则同 `-`。

可选字段 **`meta`** / **`other`**：任意 JSON 对象，原样进入运行结果中的 `meta`。

## 题干与输出格式（由调用方约定）

典型题干中会包含：

- 影像检查报告摘录（影像描述 / 影像诊断等）  
- 指定检查部位与所见依据  
- 待选类别列表  
- 严格输出模板（例如两行：`伤情类别：…` / `判断依据：…`）

模型须**完全遵守**题干中的格式与类别用词；默认系统提示词与上述约束对齐。

## 运行结果（stdout）

默认可解析 JSON：`skill` 为 `陈旧伤审核`，`status` 为 `ok`，`answer` 为模型文本，`question` 为本次用户消息全文，`meta` 等为透传/溯源字段（含义同 `doctor/icd-drg/drg-grouping` 等脚本）。

## 用法示例

```bash
python3 scripts/run.py --input case.json --appkey YOUR_KEY
python3 scripts/run.py --input case.json --text-only --appkey YOUR_KEY
```

## 参数

- `--question` / `--input`：与 stdin 三选一（二者不可同时）。  
- `--appkey STRING`：**必填**（`--dry-run` 除外）。  
- `--index`、`--match-id`、`--batch`：仅 `.jsonl`。  
- `--dry-run`、`--model`、`--api-url`、`--temperature`、`--timeout`、`--system-prompt`、`--output`、`--text-only`：同仓库内其他直连大模型脚本。

## 模型

- 默认 `u1-insuremed`，`https://maas-api.hivoice.cn/v1/chat/completions`。
