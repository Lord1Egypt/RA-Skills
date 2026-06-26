## Description: <br>
Theta Trading System provides scripts and configuration for A-share stock data collection, model training, scoring, and trading-research recommendations. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[wihy](https://clawhub.ai/user/wihy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers can use this skill to experiment with A-share data collection, model training, stock scoring, and recommendation workflows. Outputs should be independently validated and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial performance claims are overstated or inconsistent with the included code. <br>
Mitigation: Treat outputs as experimental research signals only; independently validate model performance, data quality, and recommendations before any real-world financial decision. <br>
Risk: Scripts include hard-coded workspace paths and can write local databases, logs, and model files. <br>
Mitigation: Run in an isolated environment, inspect or change file paths before execution, and review generated files before reusing them. <br>
Risk: Market-data freshness and external data-source availability can affect recommendations. <br>
Mitigation: Verify dependencies, data-source availability, and data timestamps before relying on generated scores or recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wihy/theta-trading-system) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Theta configuration](artifact/theta_config.json) <br>
- [Model results](artifact/models/results.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets, plus JSON configuration and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may create or update SQLite databases, trained model artifacts, logs, and recommendation tables when executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, SKILL.md frontmatter, clawhub.json, theta_config.json, and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
