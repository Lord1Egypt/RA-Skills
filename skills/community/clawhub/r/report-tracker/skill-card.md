## Description: <br>
Report Tracker analyzes Chinese-language investment research reports, maps findings to a fixed local stock pool, appends tracking records, updates cumulative indicators, and returns a structured analysis receipt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcchris1995](https://clawhub.ai/user/pcchris1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors and analysts use this skill to process research reports, compare the findings against a predefined local stock pool, and maintain a markdown tracking archive with follow-up indicators and valuation-impact notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can append research-report analysis to local investment tracking files. <br>
Mitigation: Review the target paths and ask the agent to confirm before writing when using the skill outside the documented tracking workflow. <br>
Risk: Report analysis may affect valuation or PE tracking notes. <br>
Mitigation: Review generated archive entries, especially any profitability forecast or PE changes, before relying on them for investment decisions. <br>


## Reference(s): <br>
- [Report Tracker on ClawHub](https://clawhub.ai/pcchris1995/report-tracker) <br>
- [Research Report Tracking Template](references/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis receipt and appended markdown tracking records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads report inputs and updates local investment tracking files when the workflow is triggered.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
