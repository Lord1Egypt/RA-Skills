## Description: <br>
Use when user wants benchmark rankings, pricing, token limits, or IDE compatibility info for top 20 agentic coding models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waiyannyeinnaing](https://clawhub.ai/user/waiyannyeinnaing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to compare agentic coding models by live benchmark ranking, pricing, token limits, tool support, and IDE compatibility. It helps choose models for coding agents and OpenRouter-compatible workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live network requests to BenchLM and OpenRouter when run. <br>
Mitigation: Use it only in environments where that egress is acceptable, or restrict outbound access to benchlm.ai and openrouter.ai. <br>
Risk: Model rankings, prices, token limits, and compatibility details can change between runs because the skill uses live API data. <br>
Mitigation: Review the generated table before acting on recommendations, especially for budget or procurement decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waiyannyeinnaing/top-coding-models) <br>
- [BenchLM coding leaderboard API](https://benchlm.ai/api/data/leaderboard?category=coding) <br>
- [OpenRouter models API](https://openrouter.ai/api/v1/models) <br>
- [OpenRouter API base](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance, Code snippets] <br>
**Output Format:** [Markdown table and guidance by default; optional JSON when run with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output covers the top 20 coding models; --top changes the number of ranked models returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
