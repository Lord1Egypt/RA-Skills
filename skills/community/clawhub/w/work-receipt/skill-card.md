## Description:

Generates structured coding-session receipts that summarize files changed, problems solved, decisions made, technical debt, and next steps for standups, handoffs, and PR preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineers use Work Receipt at the end of a coding session to summarize accomplishments, changed files, decisions, tests, remaining work, and technical debt for standups, handoffs, and PR descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated receipts may expose local repository activity, diffs, TODOs, tests, confidential paths, terminal context, secrets, or credentials.

Mitigation: Use the skill intentionally, scope inputs to relevant session artifacts, and redact sensitive or unrelated details before sharing receipts.

Risk: Receipts may be incomplete or misleading when local git history, test results, or command context are stale or incomplete.

Mitigation: Review generated receipts against commits, diffs, test output, and current worktree state before using them for standups, handoffs, or PR descriptions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with structured receipt sections and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Zero external dependencies and no API calls according to the artifact metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
