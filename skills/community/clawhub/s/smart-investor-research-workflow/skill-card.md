## Description:

智能投资研究工作流 coordinates multi-source investment research, sentiment analysis, portfolio risk metrics, and PDF report generation for structured investment research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Investment managers, analysts, fund researchers, and individual investors use this workflow to gather public research, assess market sentiment, calculate portfolio risk metrics, and produce client-ready PDF investment reports. Outputs are for research support and do not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may query public web, news, and social sources through dependent skills.

Mitigation: Do not provide confidential client data, private holdings, or nonpublic investment theses unless the dependent skills' data handling has been reviewed.

Risk: Investment research outputs may be incomplete, stale, or mistaken for investment advice.

Mitigation: Use the reports as research support only, verify material claims against authoritative sources, and make investment decisions independently.

Risk: PDF report generation depends on the runtime environment, including Chinese font support.

Mitigation: Validate PDF rendering in the target environment before relying on generated reports for external delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/smart-investor-research-workflow)
- [ClawHub publisher profile](https://clawhub.ai/user/zlszhonglongshen)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Structured Markdown research content and generated PDF investment reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public-source citations, sentiment scores, portfolio risk metrics, position guidance, and a PDF download link.]

## Skill Version(s):

1.0.0 (source: workflow.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
