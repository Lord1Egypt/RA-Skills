## Description: <br>
Integrates ZoomEye network-space search so agents can query user quota, discover host assets, search web applications, and summarize resource statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and authorized operations teams use this skill to run ZoomEye-backed asset discovery, web application search, quota checks, and aggregate resource analysis for approved security or threat-intelligence work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ZoomEye searches are external, account-linked reconnaissance activity that can expose sensitive investigation intent through query terms. <br>
Mitigation: Use the skill only for authorized assets or investigations, keep queries scoped, and avoid submitting confidential data as search terms. <br>
Risk: The skill requires a ZoomEye API key and can consume account quota while making requests. <br>
Mitigation: Use a dedicated or revocable API key, monitor quota usage, and rotate or revoke the key when access is no longer needed. <br>


## Reference(s): <br>
- [ZoomEye Query Syntax Reference](references/query_syntax.md) <br>
- [ZoomEye API](https://api.zoomeye.org) <br>
- [ZoomEye API Key Setup](https://www.zoomeye.org/pricing?aff=INVITE-4KZ6-640E) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZOOMEYE_API_KEY and sends user-provided queries to ZoomEye.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
