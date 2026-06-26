---
name: med-doctor-drg-grouping
description: 医生端 ICD/DRG — 据出院文书与 DRG 候选项，由内部医疗大模型单选最可能入组；仅含 scripts/run.py，无 _shared 依赖。
metadata:
  {
    "openclaw":
      {
        "emoji": "📊"
      }
  }
---

# DRG 分组（候选单选）

## 概述

由调用方传入**完整自然语言题干**（通常含出院文书要点与若干 DRG 候选项），模型在候选项中**单选**最可能入组结果，并按约定格式输出**一行**。

与病案首页结构化审核类 skill 不同：本包**不接院内首页接口**，题干由上游拼装；适合评测集（`task` + `input` + `meta`）或与真实分组引擎对照前的模型基线。

## 题目输入（三选一）

1. **`--question`**：完整题干字符串。  
2. **`--input PATH`**：  
   - `.json` / `.jsonl`：对象须含非空 **`input`** 或 **`question`**（评测 JSON 优先用 `input`）；  
   - 其他扩展名：整文件 UTF-8 纯文本作为题干。  
   - 传 `-` 时从 stdin 读一条 JSON 或纯文本。  
3. **stdin**（未传 `--question` / `--input`、且非 TTY）：规则同 `-`。

可选字段 **`meta`**：任意 JSON 对象，原样进入运行结果中的 `meta`，便于透传 `gold`、`case_features` 等（不参与模型拼接，除非写入 `input`）。

## 输出格式（模型）

题干中应明确要求模型只输出一行，例如：

`drgsCode（drgsName）`

其中括号为**中文全角**括号，名称与候选项列表完全一致。脚本默认系统提示词与上述约束对齐；若题干另有更严格式，以题干为准。

## 运行结果（脚本 stdout）

默认可解析 JSON，字段包括：

- `skill`：固定为 `DRG分组`  
- `status`：`ok`  
- `answer`：模型原始输出文本  
- `question`：本次送入模型的用户消息全文  
- `meta`：来自输入的 `meta`（无则为 `{}`）  
- `record_index`、`model`、`input_mode`、`input_path` 等（含义同 medbench 类脚本）

## 用法示例

```bash
python3 scripts/run.py --input case.json --appkey YOUR_KEY
python3 scripts/run.py --question "……【DRG 候选】……" --appkey YOUR_KEY
python3 scripts/run.py --input case.jsonl --index 0 --batch 3 --appkey YOUR_KEY
```

## 参数

- `--question` / `--input`：与 stdin 三选一（`--question` 与 `--input` 不可同时使用）。  
- `--appkey STRING`：**必填**（`--dry-run` 除外）。内部医疗大模型鉴权 key。  
- `--index`、`--match-id`、`--batch`：仅对 `.jsonl` 生效（`--match-id` 匹配 `meta.id` 或 `other.id`）。  
- `--dry-run`：不调用模型，仅输出解析后的题目 JSON。  
- `--model`、`--api-url`、`--temperature`、`--timeout`、`--system-prompt`：调模型参数。  
- `--output PATH`：另存完整 JSON（批量为 NDJSON）。  
- `--text-only`：标准输出仅打印 `answer` 文本。

## 模型

- 默认 `u1-insuremed`，接口 `https://maas-api.hivoice.cn/v1/chat/completions`。

## 合规说明

输出为分组辅助推断，**不构成**正式医保结算或院内分组结论；涉及真实患者数据须先脱敏并遵守院内流程。
