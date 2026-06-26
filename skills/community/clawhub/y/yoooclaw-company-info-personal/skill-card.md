## Description: <br>
Employee-facing company intelligence lookup skill that calls a company API for B2B sales research reports, opportunity signals, and optional deeper opportunity insight. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, especially B2B sales users, use this skill to query a company name and receive a company intelligence report with business context, recent activity, and opportunity signals from the configured company service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and silently refreshes employee access tokens in a persistent local cache. <br>
Mitigation: Install only in trusted workspaces, protect the token cache with local file permissions, and rotate or revoke tokens when access changes. <br>
Risk: Broad company-name triggers may send company queries to the configured remote service unexpectedly. <br>
Mitigation: Use narrower trigger rules or require confirmation for ambiguous company-name matches before calling the company API. <br>
Risk: Employee identity and company lookup data are sent to the configured company API. <br>
Mitigation: Use the skill only with a trusted publisher and trusted company API configuration, and prefer HTTPS endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/yoooclaw-company-info-personal) <br>
- [Publisher profile](https://clawhub.ai/user/vivalavida-say-hi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and python3 on Linux or macOS; uses a configured company API and local token cache.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
