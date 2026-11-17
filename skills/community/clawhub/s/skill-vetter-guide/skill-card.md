## Description:

Guide for vetting third-party OpenClaw skills before installation using the Skill Vetter security protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vibesparkingai](https://clawhub.ai/user/vibesparkingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review third-party OpenClaw skills before installation, produce standardized vetting reports, and audit installed skills for security concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to add persistent AGENTS.md policy text without enough local scoping.

Mitigation: Review the proposed AGENTS.md diff before applying it and document how to remove or revise the policy.

Risk: The skill may lead agents to create recurring audit jobs without enough rollback or retention guidance.

Mitigation: Approve cron or scheduled-task changes explicitly, choose a report retention location, and record the disable or removal command.

Risk: The server security verdict is suspicious due to persistent policy and scheduled-task behavior.

Mitigation: Pin the exact released source version and review the generated vetting report before installation or operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vibesparkingai/skills/skill-vetter-guide)
- [Audit Report Template](references/audit-template.md)
- [Prompt Templates](references/prompt-templates.md)
- [Vetting Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown with checklist guidance, report templates, prompt templates, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent policy text and scheduled audit setup that require user review before applying.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
