## Description:

Create, edit, format, and publish WeChat Official Account articles through the official WeChat API, including image uploads, draft management, publishing, and mobile-oriented HTML checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slientrain-new](https://clawhub.ai/user/slientrain-new)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to prepare WeChat Official Account articles, upload media, create or update drafts, validate formatting, and submit content for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live WeChat Official Account drafts and submit content for publication.

Mitigation: Require explicit user confirmation before draft submission or publication, then perform API return-code and readback validation before treating the content as ready.

Risk: Access tokens passed on the command line or through shared temporary files can be exposed.

Mitigation: Use protected local secret storage or environment handling, avoid shell history exposure, and remove temporary payloads that contain credentials or publication data.

Risk: The workflow mandates a fixed brand footer for \u5de1\u68a6\u4eba.

Mitigation: Install and use the skill only for accounts where that branding is intended, or review and adapt the template before deployment.

Risk: Generated article claims may contain incorrect product attribution or stale facts.

Mitigation: Follow the bundled editorial checklist: confirm entities, verify factual claims, grep for excluded residual terms, and review mobile output before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slientrain-new/skills/wechat-mp-editor)
- [Layout template](references/templates.md)
- [Editorial review checklist](references/review-checklist.md)
- [Prompt examples](references/prompt-examples.md)
- [Image generation helper](scripts/generate_images.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose, inline HTML/CSS, JSON payloads, and shell or Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WeChat API draft IDs, uploaded media URLs or media IDs, and preflight validation results.]

## Skill Version(s):

1.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
