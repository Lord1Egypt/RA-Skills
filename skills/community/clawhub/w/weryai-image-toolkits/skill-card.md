## Description:

Use when the user needs WeryAI image tools to analyze and transform existing images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route existing image editing requests to WeryAI tools for prompt extraction, background changes, canvas expansion, face swap, reframe, repair, text erasure, translation, and upscaling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary classifies the skill as suspicious because file upload and API-host handling are broad for default installation.

Mitigation: Install only when WeryAI is trusted, keep use tightly controlled, and review the security guidance before use.

Risk: Local file paths can be uploaded to WeryAI during real processing.

Mitigation: Prefer public HTTPS image URLs and pass local paths only when the exact file is intended for upload.

Risk: WERYAI_BASE_URL can redirect API and upload traffic to another host.

Mitigation: Do not set WERYAI_BASE_URL unless the host is fully trusted.

Risk: Real submit and wait commands can consume WeryAI credits.

Mitigation: Use dry-run validation before paid processing and confirm ambiguous or expensive requests.

## Reference(s):

- [WeryAI Image Tools Matrix](artifact/references/image-tools-matrix.md)
- [WeryAI documentation index](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/weryai-developer/skills/weryai-image-toolkits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and JSON CLI results with image links, prompt text, task status, or error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and WeryAI credits for paid processing.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
