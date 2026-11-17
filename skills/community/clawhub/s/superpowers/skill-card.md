## Description:

Spec-first, TDD, subagent-driven software development workflow for planning, implementing, debugging, and finishing coding tasks with tests, reviews, commits, and user gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlshlad85](https://clawhub.ai/user/wlshlad85)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to structure feature work, debugging, and branch completion through brainstormed designs, detailed plans, TDD, subagent reviews, test verification, and explicit user choices for merge or PR actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can run project tests, git commands, create commits, and guide branch merge, push, PR, or discard actions.

Mitigation: Review higher-impact branch prompts carefully before approving them, keep work on a branch, and require passing tests before merge or PR actions.

Risk: The structured planning and subagent loops can be heavyweight for very small coding changes.

Mitigation: Use it for non-trivial feature, debugging, and branch-completion work; handle one-line fixes, code reading, and non-code tasks directly.

Risk: Generated plans, implementation steps, or subagent outputs could contain incorrect or incomplete technical guidance.

Mitigation: Require failing tests first, spec review, code-quality review, and full test verification before accepting or merging changes.

## Reference(s):

- [Superpowers Dev Workflow on ClawHub](https://clawhub.ai/wlshlad85/skills/superpowers)
- [Publisher profile](https://clawhub.ai/user/wlshlad85)
- [Brainstorming Reference](references/brainstorming.md)
- [Writing Plans Reference](references/writing-plans.md)
- [Subagent-Driven Development Reference](references/subagent-development.md)
- [Systematic Debugging Reference](references/systematic-debugging.md)
- [Test-Driven Development Reference](references/tdd.md)
- [Finishing a Development Branch Reference](references/finishing-branch.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create planning documents, tests, commits, branch actions, and subagent prompts when the host agent has the required tools and user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
