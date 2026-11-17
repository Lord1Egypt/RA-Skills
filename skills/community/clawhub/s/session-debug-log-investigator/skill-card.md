## Description:

Use when diagnosing a failing or confusing Claude Code session by enabling debug logging, tailing recent logs, and explaining warnings or errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect recent Claude Code session debug logs, separate configuration issues from runtime problems, and produce specific reproduction or follow-up steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session debug logs can contain sensitive details such as secrets, personal data, tokens, paths, or prompt contents.

Mitigation: Avoid sharing raw logs broadly and redact sensitive material before disclosure.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic summary with optional shell commands and configuration checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on recent log tails rather than full log ingestion.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
