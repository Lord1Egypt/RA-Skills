## Description: <br>
Query Umami Cloud and self-hosted Umami analytics data via a read-only API helper using a user-provided API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hfichter](https://clawhub.ai/user/hfichter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and analytics users use this skill to fetch website traffic, page, event, session, realtime, report, and attribution data from Umami for analysis, planning, experiments, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided Umami API key to query analytics data. <br>
Mitigation: Use the narrowest API key available, avoid admin-scoped keys unless needed, and keep UMAMI_BASE_URL pointed only at Umami Cloud or a trusted self-hosted instance. <br>
Risk: Broad or ambiguous analytics requests can return unintended website scopes or time ranges. <br>
Mitigation: Ask for explicit website IDs and time ranges before requesting data. <br>


## Reference(s): <br>
- [Umami read endpoints](references/read-endpoints.md) <br>
- [Umami API documentation](https://v2.umami.is/docs/api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only GET requests using UMAMI_API_KEY and optional base URL, website ID, deployment mode, path variables, query parameters, and time presets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
