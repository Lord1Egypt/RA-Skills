---
name: tianshu-xhs-note
description: >
  把素材整理成小红书笔记结构：标题建议、正文分段、字数统计、话题标签草稿、合规小提示。
  Use when: 用户要写小红书、排版笔记、加话题标签、控制字数；用户说「小红书文案」「笔记结构」「XHS」。
  NOT for: 自动生成需深度创意的全文代写（可配合模型润色后再用本 skill 结构化）。
metadata:
  openclaw:
    primaryEnv: ""
---

# 小红书笔记结构化 (tianshu-xhs-note)

将已有文案或要点**整理成**符合小红书发布习惯的格式：标题备选、正文分段、话题标签建议、基础字数与格式检查（本地规则，不联网）。

## When to Run

- 用户说「小红书笔记」「XHS」「帮我排一下笔记结构」「加话题标签」
- 已有草稿或长段文字，需要按小红书习惯分段、控制长度、输出 `#话题` 草稿

## Workflow

1. 确认用户有可用的正文（或让模型先生成初稿）
2. 将正文写入临时文件，或直接用 `--text`（注意 shell 转义）
3. 执行：
   ```bash
   node ~/.openclaw/skills/tianshu-xhs-note/scripts/pack_note.js --file /path/to/draft.txt
   ```
   或：
   ```bash
   node scripts/pack_note.js --text "你的正文……"
   ```
4. 把脚本输出的 Markdown 交给用户；需要配图时继续调用 `tianshu-image` / `tianshu-qiniu-upload` 等

## 参数说明

| 参数 | 说明 |
|------|------|
| `--file` / `-f` | 正文文件路径（UTF-8） |
| `--text` / `-t` | 直接传入正文（较短时用） |
| `--max-body` | 正文建议最大字数，默认 `900`（预留标题与标签空间） |

## Output

脚本向 stdout 打印一整段 Markdown：**标题备选**、**正文**、**话题标签建议**、**发布前自检清单**。
