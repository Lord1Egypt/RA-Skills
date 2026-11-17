## Description:

LogicArt-backed code analysis that helps find bugs, security issues, complexity concerns, suggestions, and logic-flow information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to submit code snippets or files to LogicArt for review and receive bug, security, complexity, suggestion, and logic-flow analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code snippets or file contents can be sent to the external LogicArt API.

Mitigation: Use only with code approved for external submission, and avoid proprietary repositories, secrets, credentials, regulated data, or unreviewed sensitive files.

Risk: The security evidence notes no runtime consent check or tight activation scope before external analysis.

Mitigation: Require explicit user confirmation and a clearly scoped file or code snippet before running the analysis script or API call.

## Reference(s):

- [LogicArt](https://logic.art)
- [LogicArt Analyze API](https://logic.art/api/agent/analyze)
- [Validate Repo](https://validate-repo.replit.app)
- [ClawHub Skill Page](https://clawhub.ai/jpaulgrayson/skills/quack-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance for users and JSON responses from the analysis script or API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bugs, security issues, complexity score, prioritized suggestions, and logic-flow information when provided by LogicArt.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
