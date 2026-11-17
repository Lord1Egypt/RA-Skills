## Description:

Theta Trading System helps an agent work with an A-share stock selection workflow that fetches market data, trains scoring models, and generates ranked stock recommendations with risk-control guidance.

This skill is for research and development only.

## Publisher:

[wihy](https://clawhub.ai/user/wihy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and analysts can use this skill to operate a research-oriented quantitative stock-selection workflow for A-share limit-up data, model training, scoring, and recommendation review. The packaged evidence warns that outputs are for reference only and are not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes strong performance and recommendation claims that may be misleading for financial decisions.

Mitigation: Treat outputs as research signals only, independently validate model performance, and do not use recommendations as real trading advice.

Risk: Scripts write data, logs, and model artifacts to fixed root workspace paths.

Mitigation: Run in an isolated environment and review or change storage paths before execution.

Risk: The packaged workflow depends on live market data packages and unpinned runtime dependencies.

Mitigation: Use a reviewed lockfile or pinned dependency set before installing or running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wihy/skills/theta-trading-system)
- [Skill instructions](SKILL.md)
- [User guide](README.md)
- [Release changelog](CHANGELOG.md)
- [Theta configuration](theta_config.json)
- [Packaged model results](models/results.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples plus JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include stock scores, ranked recommendations, model-training summaries, and risk-control guidance.]

## Skill Version(s):

1.2.0 (source: server evidence, frontmatter, clawhub.json, theta_config.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
