## Description: <br>
Token经济学家(专业版) guides agents through token-cost optimization with semantic caching, cost estimation, budget controls, team cost analysis, context compression, and model-routing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, team leads, and agent operators use this skill to configure token usage reports, semantic cache strategies, budget alerts, team cost analysis, and model-routing guidance for AI agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared cross-session or team prompt/response caching may expose sensitive content across users or contexts. <br>
Mitigation: Disable sharedCache by default for team use unless administrators enforce user isolation, redaction, retention, deletion, and access controls. <br>
Risk: Outbound alerts or callbacks can disclose budget, usage, or prompt-adjacent metadata if sent to untrusted endpoints. <br>
Mitigation: Use approved destinations only, avoid sending secrets or raw prompt content, and require administrator review for alert and callback configuration. <br>
Risk: The model-routing sample needs correction before it is used for important work. <br>
Mitigation: Review and test routing logic before relying on automatic model selection for production or high-impact tasks. <br>


## Reference(s): <br>
- [ClawHub skill release: token-economist-pro](https://clawhub.ai/thcjp/skills/token-economist-pro) <br>
- [ClawHub publisher profile: thcjp](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, Python, bash, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cost estimates, budget summaries, cache-analysis guidance, model-routing recommendations, and configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
