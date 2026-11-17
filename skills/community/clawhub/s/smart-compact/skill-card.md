## Description:

Smart context compaction for OpenClaw agents that scans tool outputs, extracts important details into memory files, and generates a pre-compact checklist before /compact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill before context compaction to preserve important conversation details, decisions, configuration values, errors, and task progress in append-only memory notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save broad conversation and tool-output details to persistent memory without strong safeguards against storing secrets.

Mitigation: Use only in sessions where persistent memory is appropriate; avoid sessions containing passwords, API keys, cookies, private keys, or sensitive personal or business data unless entries are reviewed, redacted, and deletable.

## Reference(s):

- [Smart Compact on ClawHub](https://clawhub.ai/wavmson/skills/smart-compact)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown checklist and append-only memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write selected conversation and tool-output details to memory/YYYY-MM-DD.md.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
