---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '84577f89-be35-4781-a162-02ff8568eb98'
  PropagateID: '84577f89-be35-4781-a162-02ff8568eb98'
  ReservedCode1: 'e78554d4-aa78-4868-a98e-071d7de0b4c4'
  ReservedCode2: 'e78554d4-aa78-4868-a98e-071d7de0b4c4'
---

# Report Format

Use this Markdown structure for the final report. Keep timestamps when available. If the transcript lacks timestamps, say so and use topic sections.

```markdown
# 视频字幕知识要点报告

## 基本信息

- 视频/课程：{title}
- 来源：{source}
- 时长：{duration}
- 处理时间：{processed_at}

## 来源与限制

- 来源链接：{source_url}
- 字幕获取方式：{acquisition_method}
- 预计处理耗时：{estimated_time}
- 估时依据：{estimation_basis}
- 主要不确定因素：{estimation_risks}
- 内容完整性：{complete|partial|unknown}
- 已知限制：{limitations}
- 准确性说明：本报告基于可提取的字幕/transcript 整理生成；若字幕不完整、自动生成字幕存在识别误差或缺少视觉画面信息，可能存在遗漏或误识别。本技能不进行音频转写。

## 一句话总结

{one_sentence_summary}

## 核心要点

1. {point}
2. {point}
3. {point}

## 分段笔记

### {start_time}-{end_time} {section_title}

**本段主题：** {topic}

**知识点：**
- {knowledge_point}

**关键概念：**
- `{term}`：{definition}

**重要结论：**
- {conclusion}

## 方法与流程

- {step_or_framework}

## 术语表

| 术语 | 解释 |
|---|---|
| {term} | {definition} |

## 行动清单

- [ ] {action}

## 待确认问题

- {question}
```

## Optional Post-Report Export

After the Markdown report is saved, the workflow must ask the user whether to export to another format. Reported supported targets:

- **Word（.docx）** — produce a formatted Word document.
- **PDF（.pdf）** — produce a polished PDF.
- **HTML（.html）** — produce a browser-openable web page.
- **无需，Markdown 已够用** — skip export and finish.

When the user picks a format, generate the exported file alongside the Markdown report and announce the new path. Only one extra format per user choice unless the user requests more.

## Quality Rules

- Do not invent timestamps.
- Do not claim full coverage when only partial subtitle content was processed.
- Mark unclear terms, noisy auto-generated captions, missing visual context, or inaccessible sections as limitations.
- Separate factual summary from inferred recommendations.
- Prefer concise bullet points over long paragraphs.
- Explicitly state in the report that the skill is subtitle-only and did not perform audio transcription.