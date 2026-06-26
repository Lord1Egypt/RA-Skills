## Description: <br>
Complete Qlik Cloud analytics platform integration with 37 tools for health checks, search, app management, reloads, natural language queries, automations, AutoML, Qlik Answers AI, data alerts, spaces, users, licenses, data files, and lineage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fianabates1](https://clawhub.ai/user/fianabates1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, analysts, and developers use this skill to inspect Qlik Cloud tenants, manage apps and reloads, query business data with natural language, and operate Qlik Cloud features from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the configured Qlik Cloud API key for broad read and write actions in the tenant. <br>
Mitigation: Use a least-privilege, revocable API key and limit installation to tenants where agent access is approved. <br>
Risk: Incorrect tenant configuration could send authorized requests to the wrong Qlik Cloud domain. <br>
Mitigation: Verify QLIK_TENANT is the exact HTTPS Qlik Cloud tenant domain before running scripts. <br>
Risk: Production-impacting actions include app deletion, reload cancellation, automation runs, and alert triggers. <br>
Mitigation: Require human confirmation before destructive or operational actions and review target IDs before execution. <br>
Risk: API keys may be exposed if stored in committed files or shared transcripts. <br>
Mitigation: Store credentials outside committed files, rotate keys if exposed, and avoid logging secret values. <br>


## Reference(s): <br>
- [Qlik skill page on ClawHub](https://clawhub.ai/fianabates1/qlik) <br>
- [Publisher profile on ClawHub](https://clawhub.ai/user/fianabates1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QLIK_TENANT and QLIK_API_KEY; scripts return success or error objects with timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
