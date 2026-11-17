## Description:

Session retrospective that analyzes conversation history to produce structured feedback for both user and LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to review current or past assistant sessions, identify prompting patterns, and produce balanced critique for both the user and the LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local assistant session logs that may contain private prompts, tool outputs, or code.

Mitigation: Use an explicit session file or project-verified sessions before running the parser, and review generated retrospective files before sharing or committing them.

Risk: Automatic session discovery can collect broader Codex or OpenCode history than the current project.

Mitigation: Avoid broad auto-discovery when privacy boundaries matter; restrict inputs to known project sessions.

Risk: Transcript-derived Markdown files remain in the project after execution and may preserve sensitive details.

Mitigation: Redact, remove, or ignore FEEDBACK_TO_HUMAN.md, FEEDBACK_TO_LLM.md, and temporary transcript files when they contain sensitive content.

## Reference(s):

- [Retrospect ClawHub skill page](https://clawhub.ai/zbc0315/skills/retrospect)
- [zbc0315 ClawHub publisher profile](https://clawhub.ai/user/zbc0315)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown files and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FEEDBACK_TO_HUMAN.md and FEEDBACK_TO_LLM.md in the project root; requires node to parse local session transcripts.]

## Skill Version(s):

1.4.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
