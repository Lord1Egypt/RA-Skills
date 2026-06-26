## Description: <br>
Generates earnings-review analysis for listed companies and stocks across supported China A-share, Beijing, Hong Kong, and U.S. markets using Eastmoney/Miaoxiang data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to identify a public company, choose an available reporting period, and generate an earnings review with analysis text, attachment paths, provenance notes, and a share link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires EM_API_KEY for the Eastmoney/Miaoxiang API integration. <br>
Mitigation: Store the key only in the environment, confirm the key source and scope before use, and avoid exposing it in prompts, logs, or outputs. <br>
Risk: Generated report attachments and optional debug JSON can remain on local disk. <br>
Mitigation: Keep debug mode off unless troubleshooting and review or clean the configured output directory after use. <br>
Risk: Earnings commentary depends on the selected company and reporting period. <br>
Mitigation: Stop on entity or report-period validation errors, and make any fallback or approximate report-period selection explicit to the user. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/financial-ai-analyst/stock-earnings-review) <br>
- [Publisher Profile](https://clawhub.ai/user/financial-ai-analyst) <br>
- [Business Logic](BUSINESS_LOGIC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, guidance] <br>
**Output Format:** [Markdown response with structured text, share link, local attachment paths, and optional JSON debug artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated PDF, Word, and spreadsheet attachments locally; debug mode may also save intermediate JSON logs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
