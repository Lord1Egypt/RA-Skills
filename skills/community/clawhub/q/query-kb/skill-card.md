## Description:

Answer questions from personal and team knowledge bases with strict source grounding, no-answer behavior when the knowledge base lacks evidence, answer validation, and query logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace agents use Query Kb to answer personal, team, project, and cross-knowledge-base questions from stored knowledge pages. The skill is intended to return source-grounded answers, explicit no-answer responses, or insufficient-evidence responses with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Gitea administrator access can read, write, and log sensitive repository data.

Mitigation: Replace the administrator token with least-privilege credentials, enforce HTTPS, and add per-operation authorization checks before deployment.

Risk: Raw query logging can preserve sensitive user questions and hit metadata in repository history.

Mitigation: Decide whether query logging is acceptable for the workspace, then apply retention, redaction, and access controls for logs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown answers with source citations, plus inline shell commands and JSON helper-script outputs during execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers must include a sources section and should be validated against pages read for the query.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
