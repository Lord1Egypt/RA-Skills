## Description:

Universal PDF Vision Parser extracts multilingual document content and language learning notes from PDFs by converting pages into high-resolution images and using Qwen-VL-Max vision to produce structured Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingensiie](https://clawhub.ai/user/mingensiie)

### License/Terms of Use:


## Use Case:

Developers, educators, and language learners use this skill to convert multilingual PDFs, language notes, and complex document layouts into readable Markdown when standard OCR is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF pages are converted to images and sent to DashScope/Qwen for processing.

Mitigation: Avoid sensitive PDFs unless external processing by DashScope/Qwen is acceptable for the intended use case.

Risk: API keys can be exposed if supplied directly on the command line.

Mitigation: Use DASHSCOPE_API_KEY or a secret manager, and install the skill only in a controlled Python environment.

Risk: The output path can overwrite an existing file.

Mitigation: Choose a dedicated output path and review generated Markdown before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingensiie/skills/universal-pdf-vision-parse)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown file generated from PDF page images, with shell commands for invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to processing two pages; can process all pages with --max-pages -1. Requires DashScope/Qwen-VL-Max access.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact SKILL.md states 0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
