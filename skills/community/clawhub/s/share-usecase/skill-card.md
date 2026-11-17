## Description:

Share your OpenClaw use case to clawusecase.com. Analyzes your recent work and creates a submission for the community.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephl37](https://clawhub.ai/user/josephl37)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to turn recent chat context into a reviewed, structured public use case submission for clawusecase.com, with optional anonymous or OAuth-attributed publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent conversation context may contain sensitive project details that could be included in a public use case draft.

Mitigation: Review and edit the draft before submission, and omit secrets, internal URLs, private customer information, and sensitive implementation details.

Risk: OAuth attribution can place raw credential responses in command output or tool logs.

Mitigation: Submit anonymously when attribution is unnecessary; when attribution is used, limit visible output and retained logs to allowlisted public profile fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephl37/skills/share-usecase)
- [clawusecase.com](https://clawusecase.com)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown preview text, command-line arguments, and JSON responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts public submission fields including title, hook, problem, solution, category, tools, requirements, and optional attribution.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
