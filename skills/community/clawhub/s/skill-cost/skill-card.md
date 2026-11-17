## Description:

Track per-skill token usage and costs from OpenClaw session logs, with model and daily breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzwalker](https://clawhub.ai/user/dzwalker)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to identify which installed skills consume the most tokens and cost, filter usage by date or agent, and compare skill-level spending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local session logs may reveal workflow patterns, installed skill usage, model usage, and cost data.

Mitigation: Run the skill only in environments where reading ~/.openclaw/agents is acceptable, and treat exported JSON, terminal output, and screenshots as sensitive.

Risk: Skill attribution and fallback cost calculations can be incomplete when session entries lack direct cost fields or recognizable skill call paths.

Mitigation: Review reports before using them for budgeting decisions, and prefer sessions that include explicit cost totals when accuracy matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dzwalker/skills/skill-cost)
- [ClawHub Publisher Profile](https://clawhub.ai/user/dzwalker)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with bash commands, plus text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include skill name, calls, token counts, model breakdowns, daily breakdowns, session counts, and cost totals.]

## Skill Version(s):

0.1.0 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
