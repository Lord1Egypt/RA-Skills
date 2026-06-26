## Description: <br>
Professional AI-powered platform that generates personalized career guidance based on user assessment data, skills, goals, and preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to generate personalized career recommendations, career pathways, skill gap analysis, and learning resource suggestions from structured assessment data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Career, workplace, and compensation details submitted to the API may be personal or sensitive data. <br>
Mitigation: Use pseudonymous session IDs, omit userId when it is not needed, and avoid sharing exact compensation or highly sensitive workplace details unless the provider's privacy, retention, and deletion practices have been reviewed. <br>
Risk: Generated career recommendations may be incomplete, generic, or inappropriate for a user's specific workplace context. <br>
Mitigation: Treat the output as planning support, review recommendations before acting on them, and validate important career or compensation decisions with trusted human guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-elevate-your-profile-at-work) <br>
- [Career guidance API docs](https://api.mkkpro.com:8083/docs) <br>
- [Career guidance API route](https://api.mkkpro.com/career/elevate-your-profile-at-work) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, JSON] <br>
**Output Format:** [JSON API response containing a guidance summary, recommendations, career pathways, skill gaps, resource recommendations, session ID, and generated timestamp.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated from session, timestamp, background, skills, goals, and preference fields supplied in the request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
