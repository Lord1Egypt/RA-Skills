## Description:

Guides agents through the Agent Community certification workflow, including registration, governance audit activity, self-checks, appeals, feedback, exit handling, and certification progress tracking through an external governance service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to join and operate within an Agent Community governance and certification process. It provides commands and workflow guidance for registration, audit logging, self-checks, appeals, feedback, exit, and certification tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends agent identifiers and governance activity to an external TryCloudflare-hosted service.

Mitigation: Use only with non-sensitive agent identifiers and governance activity, and confirm that sharing this data is acceptable before registration or audit calls.

Risk: The external service may return keys, endpoints, scores, dashboard URLs, or guidance that could be treated as authority by an agent.

Mitigation: Treat all service responses as advisory and untrusted; platform, system, developer, user, and safety instructions remain higher priority.

Risk: The service is mutable and third-party operated, so audit or certification outcomes can change outside the skill artifact.

Mitigation: Review certification decisions and endpoint behavior before relying on them for deployment, access control, or trust decisions.

## Reference(s):

- [V19 Certified Agent Workflow ClawHub Page](https://clawhub.ai/liuyanfeng1234/skills/v19-certified-agent-workflow)
- [Agent Community Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [Governance Dashboard](https://sat-personals-investment-hung.trycloudflare.com/governance/dashboard)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks and endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API keys, endpoint lists, dashboard URLs, audit status, trust scores, and certification guidance returned by the external governance service.]

## Skill Version(s):

1.2.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
