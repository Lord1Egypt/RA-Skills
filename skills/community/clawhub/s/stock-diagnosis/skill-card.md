## Description: <br>
Provides single-stock diagnosis for Shanghai, Shenzhen, and Beijing A-shares by sending a natural-language stock question to Eastmoney and returning a structured Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request a broad, single-stock A-share diagnosis for questions about overall outlook, holding decisions, and risks. It is intended for one stock at a time and returns the service-provided Markdown report rather than a rewritten summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock questions to Eastmoney's service and requires EM_API_KEY for authentication. <br>
Mitigation: Keep EM_API_KEY private, use a revocable key where possible, and submit only questions appropriate for Eastmoney's service. <br>
Risk: Successful reports may be saved locally by default. <br>
Mitigation: Use --no-save for queries that should not be retained and manage generated .md files according to local data-handling rules. <br>
Risk: Stock diagnosis output may be mistaken for investment advice. <br>
Mitigation: Treat the report as reference material, preserve the returned Markdown body, include a risk notice, and do not fabricate conclusions when the service returns an error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/stock-diagnosis) <br>
- [Eastmoney Miaoxiang service](https://ai.eastmoney.com/mxClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files] <br>
**Output Format:** [Markdown report, optionally saved as a local .md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY; each run analyzes one A-share stock question and can use --no-save to avoid writing a report file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
