## Description: <br>
Automatically analyzes Word template structure, style, content patterns, images, tables, and metrics, then generates formal documents from knowledge-base, document, CSV, relational, or SQL-result inputs that match the template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmmqqqq](https://clawhub.ai/user/zmmqqqq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and document authors use this skill to convert an existing Word report template plus supporting data into a new formal report. It is suited for monthly, quarterly, annual, regulatory, monitoring, and other template-driven reports that combine prose with structured metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Templates, reports, CSVs, SQL results, or knowledge-base content may contain confidential or regulated information that is processed with a cloud model. <br>
Mitigation: Use only data approved for the selected OpenClaw environment and glm-5 provider; avoid confidential, regulated, or internal-only inputs without organizational approval. <br>
Risk: Generated formal reports may contain incorrect summaries, formatting mismatches, or unsupported metrics. <br>
Mitigation: Manually review the generated document against the source template and input data before distribution or operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmmqqqq/templatebased-writing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown sections containing template analysis, data summaries, chart/table suggestions, and Word-ready document text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include intermediate analysis and suggested chart or table placeholders when source data is incomplete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
