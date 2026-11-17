## Description:

Generates earnings review commentary for listed companies and stocks across Shanghai, Shenzhen, Beijing, Hong Kong, and U.S. markets using Eastmoney data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial analysis agents use this skill to validate a company or stock, select a disclosed reporting period, and produce an earnings review with analysis text, a share link, and saved report attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user queries and stock or report identifiers to Eastmoney APIs.

Mitigation: Use only with data appropriate for that external service and provide an EM_API_KEY from a trusted, scoped source.

Risk: The skill saves returned PDF, Word, or spreadsheet attachments locally and may write debug logs when debug mode is enabled.

Mitigation: Review the output directory, avoid debug mode for sensitive workflows unless needed, and handle saved files according to local data-retention requirements.

Risk: Generated links and saved attachments are external content returned by the API service.

Mitigation: Review generated links and attachments before sharing or relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/stock-earnings-review)
- [Publisher profile](https://clawhub.ai/user/financial-ai-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, configuration, guidance]

**Output Format:** [Markdown response with generated earnings commentary, share link, and local attachment paths; scripts return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save PDF, Word, and spreadsheet attachments locally; debug mode may write intermediate JSON logs.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
