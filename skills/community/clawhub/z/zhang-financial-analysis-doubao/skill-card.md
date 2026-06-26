## Description: <br>
Guides an agent through a Chinese-language financial statement analysis workflow for checking profit quality, bargaining position, financial risk signals, management efficiency, and potential reporting red flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiyouwolegequ](https://clawhub.ai/user/aiyouwolegequ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and finance-focused agents use this skill to turn company financial statements into a structured risk review without requiring deep accounting background. It is intended to surface issues such as low cash conversion, weak industry position, goodwill impairment exposure, inventory pressure, and earnings-quality concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may attempt to retrieve public company financial data from unspecified sources when the user does not provide data. <br>
Mitigation: Provide the relevant financial statements directly in restricted environments and verify any externally retrieved data before relying on the analysis. <br>
Risk: Financial and investment conclusions may be misleading if based on incomplete, stale, confidential, or non-public reports. <br>
Mitigation: Avoid submitting confidential or non-public reports unless the environment is approved, and independently verify conclusions with qualified review before acting on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown or JSON-style analysis with conclusions, sub-skill results, risk assessments, and final suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on user-provided financial statements or public financial data; conclusions should be independently verified before financial or investment decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
