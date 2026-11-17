## Description:

Run a bounded review-and-fix loop with fresh, read-only reviewer subagents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a bounded code review loop, verify reviewer findings, apply accepted fixes, rerun relevant tests, and summarize remaining risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may change project files after review findings are accepted and verified.

Mitigation: Review final diffs and test results before relying on the changes.

Risk: Reviewer findings can be incorrect, low value, or outside the requested review boundary.

Mitigation: Verify each finding before accepting it and record rejected findings with reasons.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown summary with review findings, decisions, fixes, verification results, and residual risks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include code edits and test commands when accepted review findings require changes.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
