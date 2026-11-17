## Description:

Track and control token consumption across OpenClaw cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to monitor token usage for OpenClaw cron jobs, enforce daily and per-job budgets, and identify lower-cost model alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented cron integration uses shell command string concatenation, which could execute unintended commands if attacker-influenced values reach job names, token counts, or model identifiers.

Mitigation: Use execFile() or spawn() with argument arrays and validate job names, token counts, and model identifiers before invoking the tracker.

Risk: The tracker persists local per-job usage and model data under ~/.openclaw/workspace/outputs.

Mitigation: Confirm that storing usage logs at that path is acceptable for the workflow and restrict filesystem access as needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the tracking script is used, it writes local token usage state to ~/.openclaw/workspace/outputs/token-usage.json.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
