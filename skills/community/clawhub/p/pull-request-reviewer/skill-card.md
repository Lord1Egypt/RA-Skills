## Description:

Reviews pull requests and code diffs across languages to identify logic bugs, security risks, missing tests, breaking API changes, and style issues before merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnguyen1996](https://clawhub.ai/user/lnguyen1996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review pull requests, pasted diffs, or accessible PR URLs and receive prioritized findings for merge-blocking defects, release warnings, suggestions, approvals, and summary judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as "code review" may activate the PR-oriented review format for requests that need debugging help or explanation instead.

Mitigation: Ask explicitly for a different review style, explanation, or debugging workflow when a PR review report is not desired.

Risk: Review findings are guidance and may miss context-dependent defects or recommend changes that do not fit the repository's constraints.

Mitigation: Validate findings against the full codebase, tests, CI results, and maintainer judgment before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnguyen1996/skills/pull-request-reviewer)
- [ClawHub publisher profile](https://clawhub.ai/user/lnguyen1996)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown report with prioritized review sections and optional corrected code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include block-merge issues, warnings, suggestions, approvals, summary, and recurring issue patterns after repeated reviews.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
