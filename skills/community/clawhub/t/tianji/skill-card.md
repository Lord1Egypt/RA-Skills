## Description: <br>
Query website analytics, monitor uptime, survey results, telemetry data, feed events, application stats, and related Tianji platform data through read-only OpenAPI endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moonrailgun](https://clawhub.ai/user/moonrailgun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to query and summarize Tianji workspace analytics, uptime monitoring, survey, telemetry, feed, billing, worker, and audit-log data without using write endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Read-only Tianji API access can still expose sensitive workspace data, including survey respondent details, member information, webhook signatures, audit records, worker source code, billing data, feed channel configuration, and AI gateway settings. <br>
Mitigation: Use the narrowest read-only API key available, avoid broad prompts, and review outputs for secrets or personal data before sharing. <br>
Risk: Some API responses may include secrets or credentials such as API keys, tokens, passwords, credential fields, model API keys, or custom model base URLs. <br>
Mitigation: Redact or omit sensitive fields when presenting results, and surface only non-sensitive metadata for member lists and audit logs unless full detail is explicitly required. <br>


## Reference(s): <br>
- [Tianji API Endpoints (GET-only)](references/api-endpoints.md) <br>
- [Tianji OpenAPI (Read-Only)](references/openapi-readonly.json) <br>
- [Tianji Repository](https://github.com/msgbyte/tianji) <br>
- [ClawHub Skill Page](https://clawhub.ai/moonrailgun/tianji) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown summaries with optional curl commands and JSON-derived analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only GET requests; responses should be summarized with sensitive fields redacted or omitted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
