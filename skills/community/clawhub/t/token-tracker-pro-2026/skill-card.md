## Description:

Records and tracks OpenClaw session token usage with daily, weekly, and cumulative statistics plus token-saving suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longziruo-max](https://clawhub.ai/user/longziruo-max)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to inspect token consumption trends, view period-based usage totals, launch a dashboard, and get suggestions for reducing token usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to perform a global npm installation and install a ClawHub package.

Mitigation: Install only from trusted ClawHub and npm sources, prefer pinned versions, and use an isolated environment when evaluating the package.

Risk: The artifact does not document what local token data the installed tracker reads or where it stores statistics.

Mitigation: Review the installed package behavior and storage locations before using it with sensitive OpenClaw session data.

## Reference(s):

- [Token Tracker Pro ClawHub skill page](https://clawhub.ai/longziruo-max/skills/token-tracker-pro-2026)
- [longziruo-max ClawHub publisher profile](https://clawhub.ai/user/longziruo-max)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides users to run token-tracker commands for token statistics, recommendations, and dashboard access.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
