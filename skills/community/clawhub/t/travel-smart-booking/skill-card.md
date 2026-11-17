## Description:

酒店聚合助手，整合分贝通、携程、美团、同程、华住会、锦江等多个酒店数据源，提供统一的酒店搜索、房型查询、预订服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search hotel options across several Chinese travel and hotel platforms, compare prices, and present source-labeled hotel results. Developers can adapt the included Python interfaces when adding real provider integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included provider search methods are placeholders, so the skill may return no real hotel inventory until integrations are completed.

Mitigation: Treat the release as a prototype and verify each provider integration before relying on search or booking results.

Risk: Future real API integrations may send hotel search details to third-party travel providers.

Mitigation: Confirm user consent, provider data-sharing terms, credential handling, and any booking or payment flow before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/travel-smart-booking)
- [Publisher profile](https://clawhub.ai/user/ryan-zry)
- [分贝通 API endpoint](https://openapiv2.fenbeitong.com)
- [携程 API endpoint](https://api.ctrip.com)
- [美团 API endpoint](https://api.meituan.com)
- [同程 API endpoint](https://api.tongcheng.com)
- [华住会 API endpoint](https://api.huazhu.com)
- [锦江 API endpoint](https://api.jinjiang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, JSON-compatible function results, Python code, and concise setup or integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hotel results should preserve provider source labels and avoid fabricated prices, inventory, or booking details.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
