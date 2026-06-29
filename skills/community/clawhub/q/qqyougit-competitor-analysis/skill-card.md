## Description: <br>
Guides an agent through public competitor research to produce a structured Chinese report covering positioning, features, pricing, user sentiment, SWOT strategy, and an action roadmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, marketing, and strategy teams use this skill to compare competitors and identify opportunities for differentiation using public information. It is suited for market research, product comparison, pricing analysis, SWOT analysis, and ongoing competitor monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad market-research triggers may activate the skill for adjacent business-analysis requests. <br>
Mitigation: Confirm that the user wants a competitor-analysis workflow before producing the full report. <br>
Risk: The workflow can incorporate confidential internal strategy if the user includes it in the prompt. <br>
Mitigation: Use public competitor information by default and avoid supplying confidential strategy unless it is intentionally part of the analysis. <br>
Risk: Competitor pricing, product features, and user sentiment can become stale. <br>
Mitigation: Verify current public sources, cite them in the report, and include a data cutoff date. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/qqyougitcom/qqyougit-competitor-analysis) <br>
- [competitor-analysis detailed reference](artifact/references/details.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Chinese Markdown competitor-analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes competitor scope, comparison tables, positioning map, SWOT cross-strategy matrix, opportunity analysis, roadmap, monitoring metrics, source notes, and data cutoff date.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
