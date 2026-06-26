## Description: <br>
Workflow Automation Cn helps agents turn natural-language automation requests into OpenClaw heartbeat scripts, schedule configuration, and usage guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create, update, list, and operate scheduled automation tasks such as notifications, data monitoring, content publishing, API calls, and multi-step workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated automation scripts may make API calls, publish content, send notifications, or keep running on a heartbeat schedule. <br>
Mitigation: Inspect and test every generated script before enabling it, confirm API endpoints and publishing actions, and remove heartbeat tasks when they should stop running. <br>
Risk: Automation templates may need tokens, chat IDs, or other secrets to call external services. <br>
Mitigation: Keep real credentials in environment variables or a secret store, and do not hard-code production secrets into generated scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/workflow-automation-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python, Bash, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and node according to the skill metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
