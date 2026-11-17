## Description:

閱讀筆記精靈可從書名、PDF 或 EPUB 產生章節摘要、精華語錄、讀書心得與知識點卡片，並匯出 Markdown、Anki、PDF 或 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn book titles, PDFs, or EPUB files into structured reading notes, review cards, and exportable reports. It supports AI-assisted summaries with OpenAI, Anthropic, or local model providers, with an offline rule-based fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Book titles and extracted PDF or EPUB text may be sent to the selected model provider or to an unvalidated model endpoint configured through the environment.

Mitigation: Use --provider offline for sensitive documents, and set LOCAL_MODEL_URL only to a trusted local endpoint, preferably localhost.

Risk: Unpinned dependencies may change behavior before production use.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuan905/skills/reading-notes-genie)
- [Python](https://python.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown and JSON reading notes, Anki card exports, PDF reports, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call configured OpenAI, Anthropic, or local model providers; offline mode produces simpler rule-based summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
