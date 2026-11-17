## Description:

Skill HR helps agents turn user tasks into job descriptions, match or recruit skills, prepare delegation handoffs, and log performance, probation, or termination outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkitpossible](https://clawhub.ai/user/thinkitpossible)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skill HR to manage an agent skill workforce: turn requests into job descriptions, select installed skills, produce recruitment briefs when no match exists, delegate work, and record outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill routing and recruitment can influence which third-party skills are installed or delegated.

Mitigation: Review match and recruitment recommendations before acting, require explicit approval for installs, and keep newly recruited skills on probation until a documented success.

Risk: Optional benchmark scripts can send prompts, benchmark content, and API credentials to configurable OpenAI-compatible endpoints.

Mitigation: Use trusted HTTPS endpoints and scoped API keys, avoid sensitive benchmark cases, and prefer dry-run or local validation when possible.

Risk: Registry and incident artifacts can capture task details that may be sensitive.

Mitigation: Do not put secrets, credentials, or private content in incidents, registries, or benchmark cases, and review generated artifacts before committing them.

Risk: Broad update, uninstall, or deletion steps can alter local skill directories.

Mitigation: Require explicit user confirmation and a path audit before destructive filesystem actions; prefer registry status changes for pool removal by default.

## Reference(s):

- [Skill HR package overview](SKILL.md)
- [Job description specification](references/02-jd-spec.md)
- [Matching rubric](references/03-matching-rubric.md)
- [Market recruitment](references/04-market-recruitment.md)
- [Performance, probation, and termination](references/05-performance-and-termination.md)
- [State and artifacts](references/06-state-and-artifacts.md)
- [Framework evaluation plan](references/08-framework-evaluation.md)
- [P02 output schema](schemas/p02-output.schema.json)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [Claude Code documentation](https://docs.anthropic.com/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON artifacts, and shell command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project-local registry and incident records, plus JSONL benchmark outputs when evaluation scripts are used.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
