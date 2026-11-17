## Description:

Session Compactor compresses older long-session history into structured summaries while preserving recent messages, tool-call context, and selected facts to reduce token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangbb-coder](https://clawhub.ai/user/fangbb-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to reduce token pressure in long conversations by replacing older messages with a structured summary while retaining recent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session compaction can weaken instruction boundaries if user-derived summaries are promoted to system authority.

Mitigation: Keep trusted system instructions separate from generated summaries, and review the compaction behavior before using the skill in security-sensitive sessions.

Risk: The artifact includes an unrelated GitHub publishing script.

Mitigation: Remove or ignore deploy.sh before installation unless repository publishing is explicitly intended.

Risk: Compaction is irreversible and may lose early-session details.

Mitigation: Use conservative token thresholds, keep recent messages intact, and back up important sessions before automatic compaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangbb-coder/skills/session-compactor)
- [Session Compactor architecture](references/architecture.md)
- [claw-code project design reference](https://github.com/instructkr/claw-code)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON result containing compression status, saved-token estimates, compressed messages, and a Markdown session summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; token counts are heuristic estimates and compaction is irreversible.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog; artifact package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
