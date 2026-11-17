## Description:

Convert SVG content, Chinese character stroke order, province/country maps (Chinese, English or pinyin names like Anhui/China/USA/Japan), or SVG URLs into editable PowerPoint (.pptx) via the handbooks.cn SVG-to-PPT service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glandon](https://clawhub.ai/user/glandon)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and presentation authors use this skill to convert SVG content, SVG URLs, Chinese character stroke-order requests, and province or country map requests into editable PowerPoint files through the Handbooks service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SVG content, SVG URLs, map or character requests, and the user's Handbooks API key are sent to handbooks.cn for conversion.

Mitigation: Install only when this data sharing is acceptable; avoid sensitive SVGs and prefer the web UI or stdin/secret-handling patterns over placing API keys directly in shell commands.

Risk: API keys can be exposed if pasted into shared logs, shell history, or command transcripts.

Mitigation: Ask users to provide keys only when direct conversion is requested, avoid echoing keys in responses, and prefer input methods that do not persist secrets.

## Reference(s):

- [Handbooks SVG to PPT tool](https://www.handbooks.cn/svg2ppt.html)
- [Handbooks homepage](https://www.handbooks.cn/)
- [ClawHub skill page](https://clawhub.ai/glandon/skills/svg2ppt-handbooks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a PPTX download link from the Handbooks service when the user supplies an API key.]

## Skill Version(s):

1.0.10 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
