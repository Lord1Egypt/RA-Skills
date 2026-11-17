## Description:

Super Agent coordinates a six-stage agent loop for sensing, planning, executing, verifying, reflecting, and memorizing progress on long-horizon goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to coordinate multi-step autonomous work across planning, tool use, verification, reflection, and memory. It is intended for long-horizon goals where the agent should save state, produce structured progress reports, and adapt future runs from prior outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run other local skill scripts as part of an agent loop.

Mitigation: Review the installed scripts and run the skill only in a controlled workspace with the minimum permissions needed for the task.

Risk: The skill can persist goals, state, and run history across sessions.

Mitigation: Do not provide secrets, credentials, regulated data, customer data, or sensitive business plans; review and delete generated memory and state files after use.

Risk: Server security evidence marks the release as suspicious due to broad authority and weak scoping.

Mitigation: Install only after manual review and monitor generated reports and next actions before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/super-agent)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON reports with plain-text status and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create run_report.json, state.json, and agent_memory.jsonl when run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
