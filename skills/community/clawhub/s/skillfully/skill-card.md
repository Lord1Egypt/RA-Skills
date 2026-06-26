## Description: <br>
Use Skillfully APIs from an AI runtime to authenticate, create a tracked skill, and retrieve feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erensunerr](https://clawhub.ai/user/erensunerr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to connect an AI runtime to Skillfully, create a tracked skill, and retrieve user feedback for that skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles email verification codes and bearer tokens for Skillfully's hosted API. <br>
Mitigation: Use an account you control, treat codes and bearer tokens as secrets, and avoid exposing them in prompts or logs. <br>
Risk: The skill sends requests to Skillfully's hosted service. <br>
Mitigation: Install only if you intend to use Skillfully's hosted service and verify the domain before sending requests. <br>
Risk: The API can return a feedback snippet intended for insertion into another skill. <br>
Mitigation: Review the generated snippet before adding it to another skill and scan the updated skill before deployment. <br>


## Reference(s): <br>
- [ClawHub Skillfully release](https://clawhub.ai/erensunerr/skillfully) <br>
- [Skillfully service](https://www.skillfully.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable email address, an email verification code, and bearer-token handling for authenticated requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
