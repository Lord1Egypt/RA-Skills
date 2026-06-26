## Description: <br>
Rumor Scanner finds early market signals including M&A rumors, insider activity, analyst upgrades and downgrades, social whispers, and SEC or regulatory activity via the AIsa API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan recent market information for early stock-rumor signals, rank the top findings by impact, and optionally emit a compact JSON summary. The output is informational and requires independent verification before any investment decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AISA_API_KEY and can send prompts to the configured AIsa-compatible endpoint. <br>
Mitigation: Use a revocable key, restrict access to trusted users, and keep AISA_BASE_URL pointed at a trusted endpoint. <br>
Risk: Stock rumors and early market signals may be unconfirmed, incomplete, or misleading. <br>
Mitigation: Treat results as informational only and independently verify sources before making investment decisions. <br>
Risk: User prompts or context could disclose private trading strategies or nonpublic financial information to the API provider. <br>
Mitigation: Do not include private trading strategies, confidential holdings, or nonpublic financial information in requests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Markdown, JSON] <br>
**Output Format:** [Markdown-style market signal report, with optional compact JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top five signals ranked by impact score; focus filters include all, M&A, insider, analyst, and social signals.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
