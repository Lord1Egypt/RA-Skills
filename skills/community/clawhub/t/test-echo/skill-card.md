## Description: <br>
A test echo skill for testing OpenClaw skill system with parameter passing. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[pplx1104](https://clawhub.ai/user/pplx1104) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill reviewers use Test Echo to verify OpenClaw parameter passing by returning a greeting that includes the provided name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill echoes the supplied name value in its output. <br>
Mitigation: Avoid entering sensitive text as the name when the reflected output should not contain it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pplx1104/test-echo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON string with status, message, and echoed input fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Echoes the provided name value in the response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
