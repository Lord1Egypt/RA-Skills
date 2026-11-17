## Description:

One-click AI product video generator for Chinese e-commerce, with modes for classic product videos, single-image starts, batch variants, and natural-language revisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hubtiger123](https://clawhub.ai/user/hubtiger123)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce sellers, marketers, and their agents use this skill to gather product, platform, template, voice, and optional image inputs, then generate or revise short Chinese e-commerce product videos through Q-star services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports unsafe shell curl templates that could allow crafted user input to run local commands in an agent environment.

Mitigation: Review before installing; replace shell command templates with a structured HTTP client or safely serialized JSON before trusting the skill where local commands can execute.

Risk: The skill sends product descriptions, optional public product image URLs, platform-linked user IDs, and optional contact information to Q-star services, and may initiate a payment QR flow.

Mitigation: Disclose this data transfer to users, avoid internal-only image URLs, and confirm payment and quota boundaries before use.

## Reference(s):

- [Q-star homepage](https://guanma.top)
- [ClawHub skill page](https://clawhub.ai/hubtiger123/skills/qstar-video-ecom)
- [Template library](artifact/TEMPLATES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown with API command examples and structured generation briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return video delivery links, payment QR flow details, quota status, or fallback guidance depending on Q-star API responses.]

## Skill Version(s):

1.3.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
