## Description: <br>
SellerSprite Skills helps agents run Amazon marketplace product, keyword, competitor, listing, traffic, pricing, review, advertising, and opportunity research workflows using SellerSprite data tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opensellersprite](https://clawhub.ai/user/opensellersprite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and agents use this skill pack to research Amazon marketplaces, compare competitors, find product opportunities, optimize listings, and produce structured decision reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel SellerSprite tool calls may consume API quota unexpectedly. <br>
Mitigation: Confirm the intended workflow and expected call volume before running broad scans or multi-ASIN analyses. <br>
Risk: Marketplace or language assumptions may produce results for the wrong Amazon locale. <br>
Mitigation: Confirm the target marketplace and language before executing research workflows. <br>
Risk: Review analysis may expose reviewer names or other personal review details. <br>
Mitigation: Avoid publishing personal review details unless they are necessary; prefer aggregated pain points and sentiment summaries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/opensellersprite/sellersprite-skills) <br>
- [Skill index](artifact/README.md) <br>
- [Agent instructions and SellerSprite tool list](artifact/agent-instructions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured lists, tables, tool-call parameters, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Amazon marketplace metrics, SellerSprite MCP tool calls, comparative analysis, scoring, and operational recommendations.] <br>

## Skill Version(s): <br>
0.1.16 (source: server release metadata; artifact frontmatter reports 0.1.17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
