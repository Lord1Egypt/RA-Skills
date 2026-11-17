## Description:

Research public Rednote content, accounts, keywords, and performance data with SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to discover and analyze public Rednote notes, creators, and discussions through SocQ, with cost estimates, task tracking, and pagination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and public-data results are sent to SocQ using an API key.

Mitigation: Use only public data and keep SOCQ_API_KEY in the environment, out of prompts, URLs, and saved commands.

Risk: Unpinned CLI installation can introduce supply-chain changes.

Mitigation: Prefer a pinned or preinstalled socq CLI over unpinned npx.

Risk: Large or multi-endpoint runs can incur unexpected credit charges.

Mitigation: Check current pricing and balance, limit the scope, and confirm costs before submitting large paid runs.

## Reference(s):

- [SocQ Rednote API documentation](https://docs.socq.ai/api-manual/rednote)
- [SocQ integrations overview](https://docs.socq.ai/integrations/overview)
- [SocQ Agent Skill guide](https://docs.socq.ai/integrations/skill)
- [SocQ developer tools](https://github.com/SocQAPI/socq-devtools)
- [Rednote endpoints and examples](references/platform.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown findings and workflow guidance, with optional raw JSONL export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, filters, credit usage, task status, result counts, and coverage limits when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
