## Description: <br>
Queries Zeecu electric vehicle lists, live status, location, battery and mileage data, and recent trip history using a user-provided API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antgroup](https://clawhub.ai/user/antgroup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve a user's bound Zeecu electric vehicles, live status, location, battery and mileage data, and recent trip history after the user supplies an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles precise vehicle location, trip history, and identifying vehicle details. <br>
Mitigation: Install only if you are comfortable granting access to that data, and run it only in contexts where the returned vehicle information is appropriate to share. <br>
Risk: The query script may save the API key to a local plaintext config.json file. <br>
Mitigation: Prefer a temporary API_KEY environment variable, inspect or delete config.json after use, and rotate the API key if it may have been stored or exposed unintentionally. <br>


## Reference(s): <br>
- [API specification](references/api-spec.md) <br>
- [Usage guide](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/antgroup/skills/zeecu-device-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; query script returns JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY; trip queries default to 7 days and support up to 30 days.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
