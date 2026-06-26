## Description: <br>
Calculates a user's retirement time and retirement age under China's gradual retirement policy from birth year, birth month, and role. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ACFFF](https://clawhub.ai/user/ACFFF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to calculate retirement month and retirement age for China policy scenarios using a birth year, birth month, and one of the supported role categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The command echoes birth year, birth month, and role before the JSON result, which may expose personal data in logs or break automation that expects clean JSON. <br>
Mitigation: Avoid logging command output with real user data, and remove or suppress the status print before using the script in strict JSON pipelines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ACFFF/retire-age) <br>
- [Publisher profile](https://clawhub.ai/user/ACFFF) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Command-line text with a JSON result object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and Python >=3.10; accepts birth year, birth month, and role.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
