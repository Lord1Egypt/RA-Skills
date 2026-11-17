## Description:

Guides AI agents through StarryNotes services for audio metadata, OCR, PDF and image conversion, bill compilation, data queries, and account and payment tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starrynotes](https://clawhub.ai/user/starrynotes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose and call StarryNotes services for media and document processing, data lookups, account setup, usage checks, and paid requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested remote updater can change the installed skill outside normal review.

Mitigation: Do not run the updater unless you independently verify and trust it; ordinary API use does not require it.

Risk: Service calls can send selected files, credentials, and payment-related requests to an external hosted API.

Mitigation: Review uploads and payment requests, use service-scoped API keys, and keep API keys and JWTs out of shared logs, repositories, and long-lived shell history.

## Reference(s):

- [StarryNotes skill release on ClawHub](https://clawhub.ai/starrynotes/skills/zerotech-platform)
- [StarryNotes service platform](https://pay.starrynan.art/nanyu)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with API and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Service responses and generated files come from the external StarryNotes API.]

## Skill Version(s):

1.4.6 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
