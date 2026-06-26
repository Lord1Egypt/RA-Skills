## Description: <br>
Professional Backend Development Career Roadmap Platform that generates personalized learning paths based on experience, skills, and career goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to call an external roadmap API that turns backend experience, current skills, and career goals into a structured learning plan with phases, milestones, and recommended resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests may send career history, current skills, goals, session identifiers, and optional user IDs to an external provider API. <br>
Mitigation: Use pseudonymous session values and avoid sensitive employer, compensation, or private project details unless the provider's privacy and retention terms are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-backend-developer) <br>
- [Backend Developer Roadmap API route](https://api.mkkpro.com/career/backend-developer) <br>
- [Backend Developer Roadmap API docs](https://api.mkkpro.com:8085/docs) <br>
- [OpenAPI specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON roadmap data with phases, milestones, and recommended resources] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires session and timestamp values; optional user identifiers and career assessment details may be included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
