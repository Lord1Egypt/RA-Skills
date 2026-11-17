## Description:

Tvs Inksnow Arch helps agents turn architecture refactor goals into an approved RFC and then generate Cursor rules that encode the approved architecture boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inksnowhailong](https://clawhub.ai/user/inksnowhailong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill when they need an agent to structure architecture refactor decisions, capture them in docs/architecture-refactor-rfc.md, and generate persistent .cursor/rules/*.mdc rules after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated alwaysApply Cursor rules can steer later agent edits beyond the immediate architecture planning session.

Mitigation: Review the generated RFC before approval and inspect generated .cursor/rules/*.mdc files before relying on them for later coding work.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown documents and Cursor .mdc rule files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval of the RFC before generating persistent Cursor rules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
