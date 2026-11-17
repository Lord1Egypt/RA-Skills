## Description:

Scans token contract security risk and returns a structured summary including score, tax, holder concentration, and LP lock status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certik-ai](https://clawhub.ai/user/certik-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and external users use this skill to request a token contract risk summary for a supported chain and contract address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user-provided chain name and contract address to CertiK's public token-scan API.

Mitigation: Use it only with chain and contract values the user is comfortable sharing with CertiK.

Risk: Token scan results are third-party security signals, not guaranteed financial advice or a complete audit.

Mitigation: Present findings as risk signals and recommend independent review before investment, deployment, or custody decisions.

Risk: A scan can be in progress or return an upstream error, so results may be unavailable or incomplete.

Mitigation: Report scan status clearly and avoid summarizing unfinished or failed scans as final results.

## Reference(s):

- [Token Scan skill page](https://clawhub.ai/certik-ai/skills/token-scan)
- [certik-ai publisher profile](https://clawhub.ai/user/certik-ai)
- [CertiK token-scan API](https://open.api.certik.com/token-scan)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown summary with optional raw JSON from the API wrapper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes score, alert count, highest severity, top alerts, tax signals, holder concentration, LP lock status, and scan status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
