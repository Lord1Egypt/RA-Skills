## Description: <br>
Scans token contract security risk with CertiK's API and returns a structured summary of score, alerts, tax, holder concentration, and LP lock status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certik-ai](https://clawhub.ai/user/certik-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and security reviewers use this skill to request token contract risk analysis for supported chains and receive a concise summary of risk score, alert severity, tax signals, holder concentration, and LP lock status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a user-provided token chain and contract address to CertiK's public API. <br>
Mitigation: Use only when outbound HTTPS to open.api.certik.com is permitted and the user is comfortable sharing the token identifier with CertiK. <br>
Risk: The returned analysis is third-party risk data, not a guaranteed security audit or investment recommendation. <br>
Mitigation: Present results as supporting risk signals and advise users to perform additional review before making security or financial decisions. <br>


## Reference(s): <br>
- [CertiK Token Scan API](https://open.api.certik.com/token-scan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional shell command or JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should include score, alert count, highest severity, up to 8 prioritized alerts, tax interpretation, holder concentration, LP lock status, and scan status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
