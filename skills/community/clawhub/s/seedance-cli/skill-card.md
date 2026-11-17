## Description:

This skill helps an agent use the Dreamina（即梦） CLI for image and video generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1angjy](https://clawhub.ai/user/l1angjy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to inspect Dreamina CLI help, manage login or credit checks, submit image and video generation tasks, and query asynchronous results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's install path asks the user or agent to run an unverified remote shell script.

Mitigation: Install only if the Dreamina CLI distribution endpoint is trusted; prefer downloading and inspecting the installer first, use a pinned or signed release if available, and avoid elevated shells.

Risk: Generation commands may consume Dreamina account credits.

Mitigation: Review commands before submitting generation jobs and warn the user before running paid actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/l1angjy/skills/seedance-cli)
- [Dreamina CLI installation endpoint](https://jimeng.jianying.com/cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include warnings before commands that can consume Dreamina account credits.]

## Skill Version(s):

2026.4.10-1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
