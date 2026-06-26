## Description: <br>
Analyzes social media post titles and engagement metrics from uploaded data or account lookups to identify features associated with stronger content performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyobject](https://clawhub.ai/user/yyobject) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content strategists, marketers, and analysts use this skill to compare high- and low-performing social media titles, define candidate title features, quantitatively verify those features against engagement metrics, and generate a shareable report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dynamic expression evaluation in the compute workflow can produce unintended results when formulas are not fully controlled by the user. <br>
Mitigation: Avoid the compute expression feature unless the formula is reviewed and fully controlled by the user. <br>
Risk: Account lookup can use an outbound data path that may be unclear to users handling sensitive content strategy data. <br>
Mitigation: Prefer uploaded local files over account API lookup, do not pass cookies or credentials, and review outbound requests before use. <br>
Risk: Generated run directories may retain uploaded or pasted social media performance data. <br>
Mitigation: Delete the generated runs directory after processing sensitive data. <br>
Risk: The setup command installs Python packages into system Python when run as written. <br>
Mitigation: Use a virtual environment instead of system Python for installation and execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yyobject/social-media-title-insight) <br>
- [Publisher profile](https://clawhub.ai/user/yyobject) <br>
- [Social media account data endpoint](https://vms-service.tezign.com/datacenter/ai-insight/public/account-data) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, HTML, Shell commands, Guidance] <br>
**Output Format:** [HTML report, JSON feature and verification artifacts, and concise Markdown or shell-command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-run files under ./runs/<timestamp>/, including cached data, feature definitions, verification results, auto-detection metadata, and report.html.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
