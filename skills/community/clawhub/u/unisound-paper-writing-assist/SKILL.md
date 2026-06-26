---
name: med-doctor-paper-writing-assist
description: 医生端临床科研 — 论文写作辅助，按 IMRaD 等结构将要点扩写为学术中文/英文段落草稿。
metadata:
  {
    "openclaw":
      {
        "emoji": "✍️"
      }
  }
---

# 论文写作辅助

## 概述

根据作者提供的**章节类型**与**要点列表**（可含已测主要结局、样本量、统计方法名等），由内部医疗大模型生成 **IMRaD 风格段落草稿**（引言 / 方法 / 结果 / 讨论 / 摘要等），并附带**报告规范意识**层面的检查清单式提示（如 CONSORT / STROBE 等仅为写作提醒，不做合规认证）。

> 本 skill **不代写未披露数据**，不生成伪造统计结果；数值须由作者在 `notes` 中显式给出，模型只做语言组织与逻辑衔接。

## 业界脉络（写法参考，非功能承诺）

医学期刊写作长期以 **IMRaD** 结构为主流；观察性与干预性研究分别有 **STROBE、CONSORT** 等报告规范用于提高可重复性。生成式辅助写作的常见产品形态为「大纲 → 段落 → 术语一致性润色」流水线。本 skill 将「章节 + 要点」映射为该流水线的最小可调用单元，便于与编辑器或投稿前校验工具组合。

## 快速开始

```bash
python3 scripts/run.py --input input.json --output output.json --appkey YOUR_KEY
```

## 输入字段（JSON）

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `section` | 是 | 如 `abstract`、`introduction`、`methods`、`results`、`discussion` |
| `notes` | 是 | 字符串数组：每点一条事实或待写要点 |
| `language` | 否 | `zh`（默认）或 `en` |
| `journal_style_hint` | 否 | 目标期刊或字数上限等自由文本 |

## 输出约定

```json
{
  "skill": "论文写作辅助",
  "status": "ok",
  "data": { },
  "text": "Markdown：段落草稿 + 规范提醒"
}
```

## 参数

- `--input PATH`：**必填**。
- `--output PATH`：可选。
- `--appkey STRING`：**必填**。

## 模型配置

- `https://maas-api.hivoice.cn/v1/chat/completions` · `u1-insuremed`

## 边界

草稿须由作者修改、署名并对科学内容负责；**禁止**将模型输出作为未经验证的结论直接投稿。
