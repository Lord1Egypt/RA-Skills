## Description:

Audits whether agent behavior stays within a defined minimum necessary behavior set, detects redundant or missing constraints, and produces source data for ETHIC constitutional clauses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and governance reviewers use this skill to audit agent logs and behavior policies for redundant, missing, or drifting behavior constraints. The audit output can inform candidate ETHIC constitutional clauses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit payloads may contain sensitive prompts, logs, credentials, personal information, internal endpoints, or confidential operational evidence sent to an unverified external service.

Mitigation: Review the skill before use, redact sensitive data, require explicit approval before transmission, and use only a trusted operator with clear retention and deletion terms or a verified local or first-party endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyanfeng1234/skills/v19-sparse-policy-auditor)
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)
- [V19 Trust Engine](https://clawhub.com/skills/v19-trust-engine)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external governance audit service and return structured audit findings for policy review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
