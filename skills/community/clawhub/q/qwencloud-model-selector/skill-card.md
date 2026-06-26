## Description: <br>
[QwenCloud] Recommend the best Qwen model and parameters for model choice, pricing comparison, capability lookup, usage or billing checks, cost history review, and model selection by execution skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose QwenCloud models, compare model capabilities and pricing, and resolve model-selection decisions for QwenCloud execution workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use the QwenCloud CLI and local CLI session to retrieve live model, pricing, usage, and quota data. <br>
Mitigation: Install and use it only when that local CLI access is acceptable, and review CLI commands before execution. <br>
Risk: Authentication flows may open a browser verification URL or rely on an existing local CLI session. <br>
Mitigation: Ask the agent to show the login URL instead of opening it automatically, and keep API keys separate from CLI session authentication. <br>
Risk: Global npm installation and persistent agent registration edits can affect the local environment beyond a single answer. <br>
Mitigation: Review the global npm install command and approve CLAUDE.md or AGENTS.md registration changes only when persistent skill discovery is desired. <br>
Risk: Model pricing, quotas, and availability can change, and stale snapshot data could mislead cost-sensitive decisions. <br>
Mitigation: Use the QwenCloud CLI or official console links for latest values, include the documented cost disclaimer for cost answers, and avoid assuming free quota is available. <br>


## Reference(s): <br>
- [QwenCloud model selector skill](https://clawhub.ai/cuixiaoyang123/qwencloud-model-selector) <br>
- [CLI Usage Guide](references/cli-usage.md) <br>
- [CLI Error Handling](references/error-handling.md) <br>
- [Recommendation Matrix](references/recommendation-matrix.md) <br>
- [Pricing Guidance and Cost Estimation Disclaimer](references/pricing-disclaimer.md) <br>
- [QwenCloud Model Pricing](references/pricing.md) <br>
- [Bailian Model List](references/model-list.md) <br>
- [Official Documentation URLs](references/sources.md) <br>
- [Agent Compatibility](references/agent-compatibility.md) <br>
- [QwenCloud model list](https://www.qwencloud.com/models) <br>
- [QwenCloud pricing](https://docs.qwencloud.com/developer-guides/getting-started/pricing) <br>
- [QwenCloud documentation](https://docs.qwencloud.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to use QwenCloud CLI JSON output for current model, pricing, quota, and usage data.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
