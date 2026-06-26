## Description: <br>
Fetch and inspect market data from Sina Finance public webpage resources across multiple market types. Use when a user wants A-share quotes, Hong Kong stock quotes, domestic futures quotes, futures page metadata, Chinese futures name to contract-code detection, contract/month discovery, code validation, or a unified Sina-based market lookup workflow involving symbols such as 600519, 000001, 00700, AG0, AU0, SC0, PG2607, EB2607, MA2605, or Chinese inputs such as 甲醇2605, 白银2606, 沥青2606. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yonglongjinhao-max](https://clawhub.ai/user/yonglongjinhao-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to detect Sina-supported market symbols, fetch A-share, Hong Kong stock, and domestic futures quotes, and fall back to futures page metadata when direct quote fields are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sina Finance public webpage resources can change, return incomplete fields, or omit unsupported and inactive symbols. <br>
Mitigation: Treat results as market-data lookups from public webpage resources and verify important financial decisions against authoritative market sources. <br>
Risk: Running the included Python scripts contacts Sina Finance public endpoints from a third-party publisher artifact. <br>
Mitigation: Review the scripts before deployment and run them only in environments where outbound requests to Sina Finance are expected. <br>


## Reference(s): <br>
- [Sina Futures Normalized Fields](references/fields.md) <br>
- [Chinese Futures Mapping](references/chinese_futures_mapping.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON or table market-data outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include normalized quote fields, fallback status, raw fields for debugging, and market-data caveats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
