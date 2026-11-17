## Description:

Venus Project PM coordinates a Feishu-based ERP project-management workflow for tracking module milestones, launch readiness, daily reporting, and morning/evening project follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers and developers use this skill to coordinate Venus ERP progress reporting, compare script output with planning files, identify blocked modules, and keep the launch timeline visible in Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutating commands can change a shared Feishu group, Base, roster, planning state, or migration state.

Mitigation: Verify the local venus-bitable-sync.py script, confirm the exact target group/Base, and require explicit user approval before setup, sync, seed, collect, track, or migration steps.

Risk: Project tracking changes may be difficult to undo if applied directly to production data.

Mitigation: Back up the Base or test changes on a copy before running mutating workflow commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spikesubingrui-design/skills/venus-project-pm)
- [Project homepage](https://github.com/spikesubingrui-design/venus-project-pm)
- [Publisher profile](https://clawhub.ai/user/spikesubingrui-design)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline shell commands and project-management recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run mutating Feishu/Base workflow commands when the user approves the target workspace and local script.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
