## Description: <br>
Provides multilingual querying and analysis of U.S. market policies, regulations, and investment environment using configurable data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and agents use this skill to query U.S. policy categories and generate investment-environment analysis in Simplified Chinese or U.S. English. Use it as research assistance, not as final financial, legal, or policy advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy, investment, or regulatory outputs could be mistaken for authoritative financial, legal, or policy advice. <br>
Mitigation: Treat outputs as research assistance and verify material conclusions against official sources or qualified advisors before acting. <br>
Risk: Configured data sources or API keys may expose sensitive business or personal information. <br>
Mitigation: Use environment variables, least-privilege credentials, and bounded prompts; avoid embedding secrets in code or shared prompts. <br>
Risk: Placeholder or stale data sources can produce incomplete or misleading policy analysis. <br>
Mitigation: Configure trusted current data sources and review returned analysis before using it in business decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/yezhaowang888-stack/usa-market-policy-2026) <br>
- [DeepSeek](https://deepseek.com) <br>
- [Huimai documentation](https://docs.huimai.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, analysis, configuration guidance] <br>
**Output Format:** [Markdown or structured JavaScript objects depending on invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Simplified Chinese and U.S. English, configurable policy data sources, and cached query results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
