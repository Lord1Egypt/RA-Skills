## Description: <br>
Tests API endpoints by sending requests, validating responses, measuring performance, handling authentication, and generating detailed health reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[underbench2-gif](https://clawhub.ai/user/underbench2-gif) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and API operators use this skill to check endpoint availability, validate expected responses, measure latency, and produce health reports for API services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API checks can send authenticated requests to real services. <br>
Mitigation: Use only endpoints intended for testing and prefer least-privilege or temporary credentials. <br>
Risk: POST, PUT, or DELETE checks may change target API state. <br>
Mitigation: Prefer read-only checks, staging environments, or explicit confirmation before running mutating requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/underbench2-gif/ub2-api-health-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown health report with endpoint summaries, measurements, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include status codes, response times, pass/fail results, performance metrics, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
