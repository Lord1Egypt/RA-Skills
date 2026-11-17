## Description:

Reads reviewer comments, advisor notes, or evaluation feedback from the clipboard and helps produce point-by-point response suggestions, a revision plan, and priority guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and project teams use this skill to turn copied review or feedback text into organized issue summaries, draft responses, revision tasks, priorities, and risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads whatever text is currently on the macOS clipboard, which may include sensitive or unrelated content.

Mitigation: Before invoking it, copy only the reviewer comments or feedback intended for analysis.

Risk: Copied feedback can contain instruction-like text that should not control the agent.

Mitigation: Treat clipboard contents as quoted source material and review generated responses before using them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/reviewer-rebuttal-coach)
- [ClawHub publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with structured bullets and clipboard-reader command output when invoked]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and macOS pbpaste; reads the current clipboard text.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
