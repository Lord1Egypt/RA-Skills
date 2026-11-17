## Description:

Audit the skills OpenClaw loads and get a measured plan to cut their per-step token cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyuchen5110](https://clawhub.ai/user/wangyuchen5110)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to inspect loaded skills, identify token costs and configuration issues, and review a plan for reversible cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied instructions are reviewed, but the external npm package's executable behavior is unverified; optional MCP installation also changes persistent configuration.

Mitigation: Prefer a reviewed, pinned package version. Review `fix --dry-run` and confirm the affected skills before applying changes; review the MCP configuration change before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyuchen5110/skills/skills-doctor)
- [Project homepage](https://github.com/wangyuchen5110/openclaw-skills-doctor)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands]

**Output Format:** [Markdown reports and guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional JSON or HTML reports; directory and token budget can be configured.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
