## Description:

Guides an AI-assisted workflow for WorldQuant BRAIN Challenge participation, including account setup, field and operator discovery, alpha factor generation, Sharpe/Fitness/self-correlation checks, and a human-confirmed daily submission loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dfkai](https://clawhub.ai/user/dfkai)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run an AI-assisted quantitative research workflow for the WorldQuant BRAIN Challenge. It helps generate, test, rank, and selectively submit candidate alpha factors while preserving human approval for account-affecting actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles primary WorldQuant BRAIN account credentials.

Mitigation: Use environment variables or a secure OS credential store, and do not store passwords in plaintext project files.

Risk: Submission scripts can affect the user's WorldQuant BRAIN account and challenge record.

Mitigation: Verify that every submit action requires explicit human confirmation before proceeding.

Risk: Generated workspace data can contain account-specific alpha IDs, candidate pools, and research results.

Mitigation: Run the scripts in a dedicated private workspace and keep wq_workspace private.

Risk: Challenge rules, scoring behavior, and platform limits may change over time.

Mitigation: Confirm current rules and API behavior against official WorldQuant BRAIN materials before relying on the workflow.

## Reference(s):

- [WorldQuant BRAIN platform](https://platform.worldquantbrain.com/)
- [WorldQuant BRAIN API](https://api.worldquantbrain.com)
- [QuantML wq-alpha-research inspiration](https://github.com/QuantML-Research/wq-alpha-research)
- [ClawHub skill page](https://clawhub.ai/dfkai/skills/wq-challenge-gold-week)
- [第①章 WorldQuant Challenge 参赛与规则](references/01-rules-and-scoring.md)
- [第②章 数据与算子](references/02-arsenal-probing.md)
- [第③章 因子构造](references/03-factor-construction.md)
- [第④章 提交规则与快速拿分](references/04-submission-harvest.md)
- [第⑤章 AI 循环研究法](references/05-research-loop.md)
- [第⑥章 5天速通计划 + 避坑](references/06-five-day-plan.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and Python workflow scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workspace files for recipes, candidate pools, score checks, and submission logs when its scripts are run.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
