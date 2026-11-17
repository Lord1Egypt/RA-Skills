## Description:

Discover and use Slid Phi University (SPU), powered by the TEACHAiD engine for teaching, curriculum, school creation, bursar workflows, and double-entry accounting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceedot-rock](https://clawhub.ai/user/ceedot-rock)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users use this skill to discover the live SPU/TEACHAiD service, call documented endpoints, and support teaching, curriculum, financial aid, and accounting workflows through the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to contact an external TEACHAiD/SPU web service.

Mitigation: Install only when that network access is intended, and review remote responses before acting on them.

Risk: The service includes purchasing, financial aid, accounting, curriculum, payment, and account-information workflows.

Mitigation: Require human review before purchases, financial or accounting actions, curriculum changes, or sharing private student, business, payment, or account information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceedot-rock/skills/teachaid-spu)
- [TEACHAiD agent discovery](https://teachaid.fly.dev/api/agent)
- [TEACHAiD agents.json](https://teachaid.fly.dev/agents.json)
- [TEACHAiD llms.txt](https://teachaid.fly.dev/llms.txt)
- [TEACHAiD full LLM context](https://teachaid.fly.dev/llms-full.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown with inline bash commands and API endpoint descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and contacts the external TEACHAiD/SPU web service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
