## Description:

Generates professional multi-page PPTX presentations from text or URLs using YAML content and customizable HTML templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyuanfang](https://clawhub.ai/user/iyuanfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and presentation authors use this skill to turn text, URLs, or structured YAML/JSON into editable PPTX decks and companion HTML for proposals, reports, pitch decks, and product presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted slide YAML, JSON, or web-derived content may execute inside Chromium during presentation conversion.

Mitigation: Render only trusted inputs until text escaping, content validation, and browser execution controls are reviewed.

Risk: Image, logo, or URL inputs may trigger unintended browser network requests during conversion.

Mitigation: Prefer reviewed local files or data URLs and block browser network access for conversion runs where feasible.

Risk: The authoritative scan verdict is suspicious because the renderer needs stronger handling for untrusted content.

Mitigation: Treat the skill as requiring security review before deployment in workflows that accept external or user-supplied deck content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iyuanfang/skills/yuanfang-html-ppt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [YAML or JSON content, Markdown guidance, shell commands, editable PPTX files, and companion HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports user-selected themes, brand color overrides, logo choices, and iterative deck revisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
