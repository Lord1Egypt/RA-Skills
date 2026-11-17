## Description:

A Chinese-language advisory skill that helps restaurant founders evaluate locations, estimate payback periods, and assess whether opening a restaurant is feasible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwek](https://clawhub.ai/user/wwek)

### License/Terms of Use:


## Use Case:

External restaurant founders and their agents use this skill to collect site and startup inputs, score restaurant locations, calculate payback feasibility, identify common restaurant startup risks, and produce opening recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides advisory business recommendations that may be wrong for a specific restaurant, location, market, or operator.

Mitigation: Treat outputs as decision support only and verify assumptions with local research, professional advice, and manual review before investing or signing a lease.

Risk: The documented example writes user input to a fixed /tmp/eval_input.json path, which can expose or collide with data on shared systems.

Mitigation: Use a private temporary directory, stdin, or another user-controlled path with restrictive permissions for evaluation input.

## Reference(s):

- [勇哥餐饮创业自测表参考文档](references/yongge-self-assessment.md)
- [ClawHub skill page](https://clawhub.ai/wwek/skills/restaurant-evaluator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell command snippets, Chinese-language text reports, and JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local Python evaluator accepts JSON input and can return both a human-readable report and structured JSON results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
