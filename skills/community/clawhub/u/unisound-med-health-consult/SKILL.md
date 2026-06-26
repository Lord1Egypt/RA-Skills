---
name: med-llm-health-consult
description: 健康咨询、体检解读与智能导诊挂号科室推荐。通过 --task 区分咨询与导诊场景；仅含 `scripts/run.py`，可独立拷贝部署。
metadata:
  {
    "openclaw":
      {
        "emoji": "🩺"
      }
  }
---

# 健康咨询与导诊

## 概述

面向大众健康咨询与就医路径引导，由医疗大模型结合场景提示词作答。

具体场景通过 **`--task`** 切换系统提示词（见下表），能力依赖内部医疗大模型；集成方也可通过 `--system-prompt` 完全自定义。

| `--task` | 能力 |
| --- | --- |
| `hc` | 健康咨询与体检解读问答 |
| `hg` | 智能导诊与挂号科室推荐 |

本能力与具体业务请求解耦：平台或调用方如何组织用户输入由集成方决定；此处只约定**如何把题目交给脚本**（见下）。

## 题目输入（三选一）

1. **`--question`**：直接传入完整题干字符串。  
2. **`--input PATH`**：  
   - `.jsonl`：每行一个 JSON 对象，须含非空字符串字段 `question`；可用 `--index` / `--batch` / `--match-id` 选取记录；  
   - `.json`：单个对象，须含 `question`；  
   - 其他扩展名：按 UTF-8 纯文本整文件作为题干。  
   - 传 `-` 时从 **stdin** 读取一条 JSON（含 `question`）或纯文本。  
3. **stdin**（且未传 `--question` / `--input`、且 stdin 非 TTY）：读入 JSON 对象或纯文本，规则同 `-`。

可在 JSON 的 `other.task` 中指定任务类型（与 `--task` 等价；命令行 `--task` 优先）。

## 模型

- 默认 `u1-insuremed`，接口 `https://maas-api.hivoice.cn/v1/chat/completions`（可通过参数覆盖）。

## 用法示例

```bash
# 指定任务类型与题干
python3 scripts/run.py --task hc --question "题干……" --appkey YOUR_KEY

# 从 jsonl 取题（other.task 可省略若命令行已传 --task）
python3 scripts/run.py --task hc --input /path/to/items.jsonl --index 0 --appkey YOUR_KEY
```

## 参数

- `--task`：**必填**（除非 `other.task` 已给出）。见上表。
- `--question` / `--input`：见上，与 stdin 三选一（`--question` 与 `--input` 不可同时使用）。
- `--appkey STRING`：**必填**（`--dry-run` 时除外）。内部医疗大模型鉴权 key。
- `--index`、`--match-id`、`--batch`：仅对 `.jsonl` 生效。
- `--dry-run`：不调用模型，仅输出解析后的题目 JSON。
- `--model`、`--api-url`、`--temperature`、`--timeout`、`--system-prompt`：调模型参数。
- `--output PATH`：另存完整 JSON（批量为 NDJSON）。
- `--text-only`：标准输出仅打印模型答案文本。

## 输出

默认可解析 JSON：含 `status`、`task`、`task_title`、`question`、`answer`、`record_index`、`meta`、`model`、`input_mode`、`input_path` 等；`skill` 为本 skill 标题。

## 合规说明

输出为模型辅助信息，不构成正式诊疗决策；涉及真实患者数据须先脱敏并遵守院内流程。
