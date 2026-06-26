## Description: <br>
Smart LLM Router routes each query to the cheapest capable model, supports 17 models across Anthropic, OpenAI, Google, DeepSeek, and xAI, uses a pre-trained ML classifier, and requires no extra API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayray1218](https://clawhub.ai/user/rayray1218) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to classify prompts into BASIC, BALANCED, or ELITE LLM tiers and select a lower-cost capable model before making model calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routed prompts may be retained locally in plaintext query history. <br>
Mitigation: Disable or remove query logging for sensitive workflows, avoid routing secrets or customer data, and clear query_history.json after use. <br>
Risk: Unpinned dependencies may change behavior or introduce security exposure over time. <br>
Mitigation: Pin and review dependencies before deployment, especially in environments handling private prompts or internal code. <br>
Risk: Routing classifications can select a model tier that is too weak or more expensive than intended. <br>
Mitigation: Review recommendations for high-impact prompts and use the skill's runtime model or tier override controls when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rayray1218/semantic-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON-like Python dictionaries, CLI text reports, and Markdown documentation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routing output includes the selected tier, model identifier, confidence, method, cost metrics, and a human-readable report.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
