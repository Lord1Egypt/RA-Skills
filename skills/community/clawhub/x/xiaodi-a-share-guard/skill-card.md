## Description: <br>
A-Share Guard is a finance-focused stock risk diagnosis skill for A-share equities that combines quantitative indicators, recent sentiment, and consensus logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mx6315909](https://clawhub.ai/user/mx6315909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan A-share stock symbols for financial, technical, and sentiment risk signals. It produces a structured risk rating and advisory notes for review, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce incomplete or misleading stock-risk reports if public finance data, web results, or bundled scripts are incomplete. <br>
Mitigation: Review outputs against primary financial disclosures and do not use generated ratings as the sole basis for trading decisions. <br>
Risk: The skill runs bundled Python scripts and fetches public finance websites, and artifact configuration references a private browserless/CDP URL. <br>
Mitigation: Inspect the scripts before execution and replace or remove the private browserless/CDP URL unless it points to an isolated browser instance you control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mx6315909/xiaodi-a-share-guard) <br>
- [Radar indicators reference](references/radar-indicators.md) <br>
- [Configuration template](references/config-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown report with structured risk ratings and JSON-compatible analysis fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from public finance website data, bundled Python scripts, and web search results when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
