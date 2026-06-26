## Description: <br>
Manage and track gym workouts, routines, nutrition, and progress using the wger API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjaspreet](https://clawhub.ai/user/0xjaspreet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to view, create, update, and report fitness, workout, nutrition, and progress data in a wger account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad read and write access to sensitive fitness and nutrition records. <br>
Mitigation: Install only when the agent should access the user's wger account, keep WGER_TOKEN private, and require explicit confirmation before create, update, or sync actions. <br>
Risk: The self-host example uses local-test defaults such as a simple database password and an unpinned Docker image. <br>
Mitigation: Change the Docker password, pin the image version, and use private networking such as a VPN before using the self-host setup beyond local testing. <br>


## Reference(s): <br>
- [wger API documentation](https://wger.readthedocs.io/en/latest/api.html) <br>
- [wger API endpoints reference](references/api_endpoints.md) <br>
- [Self-host wger](references/selfhost.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python script usage, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the wger API with the user's WGER_TOKEN and may read or write account fitness data when the agent executes the suggested commands.] <br>

## Skill Version(s): <br>
1.3.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
