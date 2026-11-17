## Description:

Save a trade or signal event to local memory log file (trades.jsonl). Use when a trade signal is confirmed and needs to be recorded, saved, or logged for future reference and history tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newbienodes](https://clawhub.ai/user/newbienodes)

### License/Terms of Use:


## Use Case:

External users, developers, and trading agents use this skill to record confirmed trade signals or executed trades in a persistent local JSONL history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled trade JSON is shown as shell-interpolated input.

Mitigation: Pass trade JSON through a safe argument array or stdin, and review the command before execution.

Risk: The save script is referenced from a local path outside the reviewed artifact.

Mitigation: Install only after confirming the referenced save.py is trusted, or bundle the reviewed save script with the skill.

Risk: The skill appends persistent trading records on the local machine.

Mitigation: Confirm the log file location and retain append-only behavior so existing trade history is not overwritten.

## Reference(s):

- [Trade Memory ClawHub skill page](https://clawhub.ai/newbienodes/skills/trade-memory)
- [newbienodes ClawHub publisher profile](https://clawhub.ai/user/newbienodes)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON input/output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and writes append-only local JSONL trade records when the referenced save script is available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
