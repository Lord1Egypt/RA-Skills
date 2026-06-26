## Description: <br>
True Seeing reviews verifiable factual claims in AI-generated articles, checks them with web search, reports discrepancies, and applies user-approved corrections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[francisk](https://clawhub.ai/user/francisk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agents use this skill to extract concrete facts from an article, verify them against web sources, and generate a correction report before making user-approved replacements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article content may contain confidential drafts or sensitive personal or business information that could be exposed through web searches. <br>
Mitigation: Use the skill only with content that is appropriate for web-based fact checking, and avoid confidential or sensitive material unless that search exposure is acceptable. <br>
Risk: Search results and proposed corrections may still be incomplete, outdated, or misleading. <br>
Mitigation: Review cited sources and approve only the replacements that are supported by reliable evidence. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Fact extraction rules](fact-extraction-rules.md) <br>
- [Search query templates](search-query-templates.md) <br>
- [Verification criteria](verification-criteria.md) <br>
- [Evaluation cases](eval-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Text, Guidance] <br>
**Output Format:** [JSON fact lists and verification reports, Markdown discrepancy reports, and corrected article text with citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full mode pauses for user approval before replacing disputed facts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
