## Description:

Openclaw Skill provides paid API-backed workplace and daily-life helpers for rental contract review, deposit calculation, resale listings, resume optimization, work reports, AI tool recommendations, and content compliance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jie868](https://clawhub.ai/user/jie868)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, consumers, and content operators use this skill to route rental, resale, workplace, and content-compliance requests to one of 20 paid helper endpoints and present the returned guidance in a readable form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send resumes, rental contracts, complaints, addresses, phone numbers, salary details, signatures, or third-party personal information to an external API.

Mitigation: Use only after reviewing the publisher's privacy, retention, and deletion terms; redact sensitive personal data before submitting text.

Risk: The skill uses a paid per-call flow through Alipay AI collection.

Mitigation: Confirm the charge and payment flow before invoking endpoints, especially when retrying after HTTP 402 payment-required responses.

Risk: Rental contract, complaint, pricing, and compliance outputs are AI-generated guidance and may be incomplete or unsuitable for a specific legal or business decision.

Mitigation: Treat outputs as informational drafts and have qualified reviewers verify legal, compliance, financial, or marketplace decisions before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jie868/skills/workplace-life-helper)
- [OpenClaw API endpoint](https://w4h8ghmxcv.coze.site)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown text with JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid per-call API wrapper; API responses may include generated content, compliance reports, payment-required responses, credits used, and disclaimers.]

## Skill Version(s):

1.3.0 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
