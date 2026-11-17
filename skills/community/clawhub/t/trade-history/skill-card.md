## Description:

Read and display recent trade history from local JSONL log file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newbienodes](https://clawhub.ai/user/newbienodes)

### License/Terms of Use:


## Use Case:

External users and trading workflow operators use this skill to review recorded trade events, filter recent trades by symbol, and recap stored signals from a local trade-history log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separate local Python script that was not included in the reviewed artifact.

Mitigation: Verify the installed read.py script comes from a trusted source before enabling the skill.

Risk: The skill reads a local trade-history log that may contain sensitive trading activity.

Mitigation: Use it only in workspaces where the agent is allowed to read the local trades.jsonl file and share summarized trade records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/newbienodes/skills/trade-history)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [JSON from the local script, presented to the user as concise Markdown or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports an optional limit and symbol filter; defaults to 20 newest records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
