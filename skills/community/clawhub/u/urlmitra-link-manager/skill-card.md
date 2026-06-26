## Description: <br>
Manage branded redirects, audit traffic analytics, and execute semantic link queries using URLMitra. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urlmitra](https://clawhub.ai/user/urlmitra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and operations teams use this skill to create branded shortlinks, check redirect health, review click performance, and search URLMitra workspace resources from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a URLMitra workspace API key for link management, health checks, analytics, and search. <br>
Mitigation: Use a scoped or revocable API key when available and store it only in the agent's approved secret environment. <br>
Risk: Semantic-search queries and link metadata may include confidential project names, customer data, or unreleased campaign details. <br>
Mitigation: Avoid sending sensitive details unless URLMitra's data handling is acceptable for that workspace. <br>


## Reference(s): <br>
- [URLMitra Link Manager on ClawHub](https://clawhub.ai/urlmitra/urlmitra-link-manager) <br>
- [URLMitra Publisher Profile](https://clawhub.ai/user/urlmitra) <br>
- [Create branded shortlink endpoint](https://api.urlmitra.com/api/v1/links) <br>
- [Redirect health summary endpoint](https://api.urlmitra.com/api/v1/health/summary) <br>
- [Semantic resource search endpoint](https://api.urlmitra.com/api/v1/mitra/search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and URLMITRA_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
