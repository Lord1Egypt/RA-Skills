## Description:

Review the session at its end, log workflow issues as structured JSONL signals; recurrence escalates priority, and one phrase enters fix mode to close the loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumingtao](https://clawhub.ai/user/yumingtao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to record real workflow issues from a completed session as structured feedback, then review confirmed fix proposals from that log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that one referenced validator script was only partially inspected.

Mitigation: Review the validator script before running it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yumingtao/skills/session-retrospective)
- [Retrospective example](references/retrospective-example.en.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Append-only JSONL feedback entries and a Markdown summary with fix proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Feedback entries use fixed field values; each proposed fix requires confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
