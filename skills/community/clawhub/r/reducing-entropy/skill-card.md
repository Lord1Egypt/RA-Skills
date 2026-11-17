## Description:

Minimize total codebase size through ruthless simplification. Measure success by final code amount, not effort. Bias toward deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill during refactoring, feature work, pull request review, and technical debt cleanup to challenge unnecessary complexity and reduce the final size of a codebase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deletion-focused guidance may encourage removing security checks, audit logs, compliance code, or tests that still protect active behavior.

Mitigation: Treat deletion recommendations as review prompts, preserve required safeguards, and run the relevant test suite before accepting changes.

Risk: Installing a third-party skill without review may introduce untrusted instructions into an agent workflow.

Mitigation: Install only from trusted sources, prefer pinned versions or reviewed commits, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/reducing-entropy)
- [Simplicity vs Easy](references/simplicity-vs-easy.md)
- [Composition Over Construction](references/design-is-taking-apart.md)
- [Data-Oriented Design](references/data-over-abstractions.md)
- [PAGNI: Probably Are Gonna Need It](references/expensive-to-add-later.md)
- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/)
- [The Grug Brained Developer](https://grugbrain.dev/)
- [Out of the Tar Pit](https://curtclifton.net/papers/MosesleyMarks06a.pdf)
- [The Value of Values](https://www.infoq.com/presentations/Value-Values/)
- [Data-Oriented Design](https://www.dataorienteddesign.com/dodbook/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown text with optional code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill itself requires no external credentials or tool integrations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
