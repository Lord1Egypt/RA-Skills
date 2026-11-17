## Description:

Analyzes legally obtained Amazon, Shopify, and TikTok Shop buyer reviews to identify sentiment themes, complaint causes, improvement actions, praises, and draft reply templates as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, operators, and support teams use this skill to turn review text they are allowed to process into VOC summaries, prioritized product or service improvements, and human-reviewed response drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API tokens and review text to an arbitrary configured endpoint.

Mitigation: Use only a trusted HTTPS TOKENAPI_BASE_URL and treat TOKENAPI_KEY as a revocable secret.

Risk: Review content may contain personal, confidential, or sensitive customer information before cloud processing.

Mitigation: Remove PII and confidential content before submission unless the user accepts the cloud-processing risk.

Risk: Generated reply templates could be sent without checking platform policy or customer-specific facts.

Mitigation: Require human review before using reply drafts with buyers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/metahuan/skills/yufluent-clawhub-publish-yufluentcn-review-intel)
- [Yufluent Homepage](https://claw.changzhiai.com)
- [OpenClaw Integration](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON containing sentiment, themes, top complaints, top praises, action items, and draft reply templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires legally obtained review text; draft reply templates should be reviewed by a human before use.]

## Skill Version(s):

1.1.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
