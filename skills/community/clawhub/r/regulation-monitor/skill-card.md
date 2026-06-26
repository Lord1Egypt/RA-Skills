## Description: <br>
Monitors public Chinese financial regulator websites for recent policies, administrative penalties, notices, and risk alerts from NFRA, CSRC, and PBOC, then summarizes the findings with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gentleming](https://clawhub.ai/user/gentleming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and compliance, legal, and financial services teams use this skill to check recent public regulatory updates from Chinese financial authorities and receive concise summaries with source and attachment links. <br>

### Deployment Geography for Use: <br>
Global; content scope is Chinese financial regulatory publications. <br>

## Known Risks and Mitigations: <br>
Risk: Public regulator pages may change, block requests, or omit recent items. <br>
Mitigation: Review the returned source links and rerun or adjust the regulator and lookback-day scope when completeness matters. <br>
Risk: Summaries of regulatory publications may miss nuance or overstate an overall trend. <br>
Mitigation: Use the summaries for triage and confirm important interpretations against the original regulator publications before acting. <br>
Risk: The skill is scoped to public Chinese financial regulatory updates and may be unsuitable for unrelated monitoring or private-document review. <br>
Mitigation: Keep use within the stated public-source scope unless the monitoring target and data-handling expectations are made explicit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gentleming/regulation-monitor) <br>
- [National Financial Regulatory Administration](https://www.nfra.gov.cn) <br>
- [China Securities Regulatory Commission](https://www.csrc.gov.cn) <br>
- [People's Bank of China](https://www.pbc.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown summaries with source and attachment links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports regulator and lookback-day parameters; final summaries include a brief trend assessment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
