## Description: <br>
Sign up for and log into services using a Ravi identity, including onboarding, form filling, 2FA, OTP handling, and credential storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent onboard to Ravi, sign up for services, log in with stored credentials, and complete SMS or email verification for an active workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and retrieve login credentials and read Ravi SMS or email verification messages for the active workflow. <br>
Mitigation: Use it only for intended signup or login workflows, protect ~/.ravi/config.json, and avoid running it on shared or poorly secured machines. <br>
Risk: Using this skill as a general inbox reader or email sender could expose unrelated messages or exceed the intended scope. <br>
Mitigation: Use the dedicated Ravi inbox or email skills for standalone inbox reading or email sending. <br>


## Reference(s): <br>
- [Device Auth API schema](https://ravi.id/docs/schema/device-auth.json) <br>
- [Auth and Keys API schema](https://ravi.id/docs/schema/auth.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve Ravi CLI commands that retrieve identity details, create or retrieve passwords, and read SMS or email verification messages.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
