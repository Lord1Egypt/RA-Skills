## Description: <br>
Fetch, export, analyze, and visualize WHOOP wearable health data, including recovery, HRV, sleep, strain, workout, profile, and body-measurement data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JarviYin](https://clawhub.ai/user/JarviYin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to authenticate a WHOOP account, fetch wearable health datasets, export JSON or CSV, and ask an agent to analyze trends such as recovery, sleep, strain, and HRV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores WHOOP OAuth tokens locally and uses them to retrieve sensitive health data. <br>
Mitigation: Keep ~/.whoop_tokens.json private, use file permissions that restrict access, and run the documented revoke command when access is no longer needed. <br>
Risk: Exported JSON or CSV files may contain health, profile, or body-measurement data. <br>
Mitigation: Export only the data types needed for the task and store exported files in a secure location. <br>
Risk: The OAuth consent flow requests multiple read scopes for WHOOP health and profile data. <br>
Mitigation: Review the requested WHOOP read scopes during consent and install the skill only when connecting a WHOOP account is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JarviYin/whoop-health) <br>
- [WHOOP API Endpoints Reference](references/api_endpoints.md) <br>
- [WHOOP Developer Portal](https://developer.whoop.com) <br>
- [WHOOP Developer API Base URL](https://api.prod.whoop.com/developer/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON, CSV] <br>
**Output Format:** [Markdown guidance with shell commands; scripts can emit JSON files, CSV files, or terminal status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided WHOOP OAuth client credentials and stores local OAuth tokens for subsequent API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
