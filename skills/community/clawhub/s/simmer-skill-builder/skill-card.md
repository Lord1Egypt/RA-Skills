## Description: <br>
Simmer Skill Builder generates complete, installable OpenClaw trading skills from natural-language strategy descriptions, including SKILL.md, Python trading code, and configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-skill builders use this skill to turn prediction-market strategy ideas, campaign briefs, or pasted strategy posts into reviewable OpenClaw/Simmer skill folders with dry-run defaults and validation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills can automate live-money prediction-market trading. <br>
Mitigation: Review generated code and configuration, keep dry-run defaults, and use live trading only after accepting venue, position, and bankroll risk. <br>
Risk: Generated work may be published publicly before the strategy, attribution, or safeguards are fully reviewed. <br>
Mitigation: Inspect the generated SKILL.md, script, clawhub.json, attribution, and validation results before publishing to ClawHub. <br>
Risk: Simmer API access and trading credentials can expose accounts or funds if handled carelessly. <br>
Mitigation: Store API keys securely and provide wallet or private-key credentials only when the venue and secret-handling model are understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/simmer/simmer-skill-builder) <br>
- [Simmer Skill Builder Source](SKILL.md) <br>
- [Simmer SDK API Reference](references/simmer-api.md) <br>
- [Simmer Skill Template](references/skill-template.md) <br>
- [LLM Probability Oracle Example](references/example-llm-oracle.md) <br>
- [Weather Trader Example](references/example-weather-trader.md) <br>
- [Mert Sniper Example](references/example-mert-sniper.md) <br>
- [AgentSkills Standard](https://agentskills.io) <br>
- [Simmer Bring Your Own Data Guide](https://docs.simmer.markets/skills/byo-data-source) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated skill files such as SKILL.md, Python scripts, clawhub.json, and command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review generated skills before running or publishing; keep trading scripts in dry-run mode unless live trading risk is intentionally accepted.] <br>

## Skill Version(s): <br>
1.3.9 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
