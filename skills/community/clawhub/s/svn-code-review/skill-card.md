## Description:

Use when completing tasks, implementing major features, or before merging to verify work meets requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzy-creator](https://clawhub.ai/user/zhouzy-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to request focused reviews of SVN revision ranges before continuing development or merging changes. It helps structure review prompts around requirements, implementation details, code quality, testing, and production readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review workflow may send more implementation context or diff content to a code-review subagent than necessary.

Mitigation: Pass only the diffs, requirements, and summary needed for the review, and review the returned findings before acting on them.

## Reference(s):

- [Source repository](https://github.com/zhouzy-creator/svn_code_review)
- [ClawHub skill page](https://clawhub.ai/zhouzy-creator/skills/svn-code-review)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown review guidance with SVN diff shell commands and structured review output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts a code-review subagent with a bounded SVN revision range and implementation context.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
