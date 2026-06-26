## Description: <br>
Generate personalized entrepreneurship career roadmaps based on user assessment data, skills, experience, and professional goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, career coaches, educational institutions, training programs, and accelerators use this skill to request structured entrepreneurship roadmaps, specializations, and learning paths from the provider API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends entrepreneurship assessment details, including experience, skills, goals, session IDs, and optional user IDs, to an external provider API. <br>
Mitigation: Omit userId when possible, use pseudonymous session identifiers, avoid secrets and highly sensitive personal information, and confirm the provider's privacy and retention terms before use with real users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-entrepreneurship) <br>
- [Entrepreneurship API route](https://api.mkkpro.com/career/entrepreneurship) <br>
- [Entrepreneurship API docs](https://api.mkkpro.com:8191/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [JSON responses containing roadmap phases, milestones, skill gaps, specializations, and learning paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses depend on user-provided assessment data and the provider API availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and openapi.json info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
