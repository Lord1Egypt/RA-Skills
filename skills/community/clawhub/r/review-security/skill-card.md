## Description:

Review code changes with Security Review subagent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a security review subagent against branch or uncommitted code changes and receive concise, severity-sorted findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review workflow can read repository diffs, which may include sensitive code or local changes.

Mitigation: Use it only in repositories where sending diffs to the configured security-review subagent is acceptable.

Risk: When explicitly asked to review a PR or branch, the workflow may switch branches after checking for blockers.

Mitigation: Keep local work committed or stashed intentionally; the skill asks before stashing when checkout is blocked by local changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/review-security)
- [Publisher profile](https://clawhub.ai/user/eohmig)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary and findings table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are summarized in a compact markdown table sorted by severity; the skill does not fix findings unless separately requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
