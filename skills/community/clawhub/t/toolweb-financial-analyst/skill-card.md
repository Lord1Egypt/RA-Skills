## Description: <br>
Professional career roadmap platform that generates personalized learning paths and specialization recommendations for aspiring financial analysts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and career platforms use this skill to call a financial analyst roadmap API that generates personalized career phases, milestones, specializations, and learning resources from user assessment data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call a paid or rate-limited external API. <br>
Mitigation: Review the pricing tiers and expected request volume before using the API in automated workflows. <br>
Risk: Roadmap recommendations may be incomplete, outdated, or mismatched to a user's career goals. <br>
Mitigation: Treat generated roadmaps as planning guidance and review recommendations before relying on them for career or training decisions. <br>
Risk: External API calls may expose submitted assessment data to the API provider. <br>
Mitigation: Avoid sending unnecessary personal data and confirm that intended use aligns with the provider's data-handling terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-financial-analyst) <br>
- [Financial Analyst Roadmap API route](https://api.mkkpro.com/career/financial-analyst) <br>
- [Financial Analyst Roadmap API docs](https://api.mkkpro.com:8187/docs) <br>
- [OpenAPI specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses with career roadmap phases, milestones, specializations, and learning resources] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses depend on supplied assessment data, session identifiers, optional user identifiers, and the availability of the external API service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
