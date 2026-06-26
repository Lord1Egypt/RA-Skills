## Description: <br>
swagger-skill helps agents inspect Swagger/OpenAPI specifications, search for matching endpoints, and call APIs from natural-language instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MinusGod](https://clawhub.ai/user/MinusGod) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and API testers use this skill to load Swagger or OpenAPI specs, find endpoint details, inspect schemas, and make authenticated API calls or file uploads from natural-language or CLI prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install npm dependencies when imported. <br>
Mitigation: Use it in a trusted workspace and review generated package or dependency changes before relying on the environment. <br>
Risk: The skill can make authenticated, state-changing API calls and upload local files. <br>
Mitigation: Use trusted Swagger hosts, prefer test or least-privilege credentials, review the matched endpoint and HTTP method before calls, and pass only file paths intended for upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MinusGod/swagger-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Plain text and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live HTTP response data, endpoint details, and file upload results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
