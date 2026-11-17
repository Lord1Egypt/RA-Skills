## Description:

Reduces token usage across multi-skill agent workflows (search, coding, debugging, testing, docs) using budgets, gating, progressive disclosure, and deduped evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderangerx](https://clawhub.ai/user/coderangerx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use TokenKiller to keep multi-step search, coding, debugging, testing, and documentation workflows concise while preserving enough evidence for useful decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may over-compress ordinary debugging, large-repo, cost, or multi-step requests and omit details needed for diagnosis or review.

Mitigation: Ask explicitly for full logs, full files, or more detail when completeness matters; use the documented L3 pull triggers for exact code, configuration, or stack-trace context.

Risk: Budget gates may narrow exploration too early on complex tasks.

Mitigation: Treat the budgets as a starting point and allow the soft warning extension path when the task is incomplete.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with concise summaries, evidence references, diffs, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses task-complexity budgets, progressive disclosure levels, and soft warnings when token budgets are nearly exhausted.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
