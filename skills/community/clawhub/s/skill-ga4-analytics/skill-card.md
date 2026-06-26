## Description: <br>
GA4 Analytics Toolkit helps agents analyze Google Analytics 4 traffic, Search Console SEO performance, real-time visitors, and indexing workflows for verified websites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site operators, and analytics teams use this skill to retrieve GA4 and Search Console data, compare date ranges, inspect SEO performance, and prepare markdown summaries from saved analytics results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Indexing API actions can request re-indexing or removal for URLs. <br>
Mitigation: Grant Indexing API access only when needed, require manual approval for every request, and restrict URLs to owned verified properties. <br>
Risk: Saved analytics results may contain sensitive business analytics. <br>
Mitigation: Regularly review or delete the local results directory and limit sharing of generated outputs. <br>
Risk: The skill requires Google service account credentials. <br>
Mitigation: Use a dedicated least-privilege service account and keep private keys out of committed files and shared outputs. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, TypeScript usage examples, shell commands, and JSON result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are saved as timestamped JSON files under results/ and may be summarized as markdown.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
