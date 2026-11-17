## Description:

Record and replay terminal sessions for debugging, documentation, or sharing procedures with teammates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to record terminal workflows, replay them with timing, and export session transcripts as markdown for debugging, documentation, or team handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal recordings and markdown exports can include passwords, tokens, private customer data, or confidential command output.

Mitigation: Avoid recording sensitive terminal activity and review recordings before exporting or sharing markdown.

Risk: Recordings are saved locally and the tool does not enforce restrictive file permissions.

Mitigation: On shared systems, verify permissions for ~/.terminal-sessions and exported files before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derick001/skills/terminal-session-replay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Terminal session recordings, JSON status responses, and Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local .typescript, .timing, and .meta.json files under ~/.terminal-sessions by default.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
