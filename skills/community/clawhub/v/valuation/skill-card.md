## Description:

Build DCF models and run comparable analysis for company valuation. Use when modeling cash flows, benchmarking peers, projecting growth, or pitching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents can use this skill to record valuation runs, checks, assumptions, comparisons, reports, and exports. Treat it as a local activity log and export utility rather than an automated valuation model builder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive valuation inputs may be stored in local plaintext logs and exported files.

Mitigation: Avoid entering confidential forecasts, deal notes, board assumptions, or client data unless local storage, retention, and cleanup controls are acceptable.

Risk: The skill is marketed for valuation modeling but primarily behaves as a logging, search, and export utility.

Mitigation: Use it to track valuation-related activity and audit trails; rely on separate reviewed models or tools for financial calculations and valuation conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/valuation)
- [Publisher Profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Plain text command output with JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/valuation by default; VALUATION_DIR can override the data directory.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
