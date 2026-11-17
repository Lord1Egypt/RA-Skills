## Description:

[QwenCloud] Recommend the best Qwen model and parameters for model choice, pricing comparison, capability review, usage or billing checks, cost history, and cross-skill model selection advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this advisory skill to select QwenCloud models, compare capabilities and cost posture, and choose CLI-backed or snapshot-backed data sources for Qwen model questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to install or run the external QwenCloud CLI and to modify persistent agent configuration.

Mitigation: Install only trusted QwenCloud tooling, ask to review exact commands and configuration diffs before approval, and avoid global unpinned installs where possible.

Risk: Untrusted model names or search text could be mishandled if inserted directly into shell commands.

Mitigation: Treat user-provided model IDs and search text as data, quote or escape shell arguments, and prefer structured CLI JSON output over ad hoc command construction.

Risk: The skill relies on QwenCloud account, pricing, quota, and model availability data that can change or require authentication.

Mitigation: Use QwenCloud CLI or official documentation for current details, label offline snapshots as fallback data, and do not infer account balance, remaining quota, or exact prices.

## Reference(s):

- [QwenCloud Model Selector Skill](https://clawhub.ai/cuixiaoyang123/skills/qwencloud-model-selector)
- [CLI Usage Guide](references/cli-usage.md)
- [CLI Error Handling](references/error-handling.md)
- [Recommendation Matrix](references/recommendation-matrix.md)
- [Pricing Guidance and Cost Estimation Disclaimer](references/pricing-disclaimer.md)
- [QwenCloud Model Pricing Snapshot](references/pricing.md)
- [QwenCloud Model List Snapshot](references/model-list.md)
- [Official Documentation URLs](references/sources.md)
- [Agent Compatibility](references/agent-compatibility.md)
- [QwenCloud Documentation](https://docs.qwencloud.com/)
- [QwenCloud Model Catalog](https://www.qwencloud.com/models)
- [QwenCloud Model Pricing](https://docs.qwencloud.com/developer-guides/getting-started/pricing)
- [QwenCloud Model Selection](https://docs.qwencloud.com/developer-guides/getting-started/model-selection)
- [QwenCloud Batch API](https://docs.qwencloud.com/api-reference/toolkitframework/openai-compatible/overview#batch-api)
- [QwenCloud Context Cache](https://docs.qwencloud.com/developer-guides/text-generation/context-cache)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise recommendations, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to use QwenCloud CLI JSON output for current model, pricing, quota, and usage data; offline snapshots are fallback material with stale-data caveats.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
