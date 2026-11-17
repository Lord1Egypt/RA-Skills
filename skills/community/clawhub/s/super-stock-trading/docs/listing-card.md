## Description: <br>
A Chinese-language A-share stock research and trading-support skill that coordinates pre-market analysis, intraday decision support, post-market review, stock screening, portfolio checks, and risk-control workflows. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[yjkj999999](https://clawhub.ai/user/yjkj999999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize A-share market research, generate trading-plan and review reports, evaluate holdings, and apply documented risk gates before any user-confirmed trading decision. It is documented for learning and research use and does not provide direct broker execution. <br>

### Deployment Geography for Use: <br>
China A-share market; review local securities regulations before use in other jurisdictions <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide trading decisions, and the security summary identifies high-impact trading-execution ambiguity. <br>
Mitigation: Treat all trading outputs as research support only, require manual broker-side confirmation, and do not rely on the skill as investment advice. <br>
Risk: The installer can add third-party skills and dependencies to the local agent environment. <br>
Mitigation: Review the listed repositories and dependency installation behavior before running the installer; skip optional installer steps unless needed. <br>
Risk: API keys may be requested for market data integrations. <br>
Mitigation: Avoid storing real API keys in config.json or shell startup files; prefer environment-specific secret handling and keep credentials out of public repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yjkj999999/skills/super-stock-trading) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yjkj999999) <br>
- [Daily workflow](references/daily_workflow.md) <br>
- [Risk rules](references/risk_rules.md) <br>
- [Skills registry](references/skills_registry.json) <br>
- [Experts registry](references/experts_registry.json) <br>
- [Wealth reports index](references/wealth_reports/README.md) <br>
- [Agent Skills specification](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON configuration, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include financial analysis and trading workflow guidance; trading decisions require explicit manual confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
