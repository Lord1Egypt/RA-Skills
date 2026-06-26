## Description: <br>
This skill helps agents manage Umeng custom event definitions through umeng-cli calls to Umeng OpenAPI endpoints for App and Mini Program event creation, batch creation, listing, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analytics operators use this skill to create, batch-create, list, and verify Umeng custom event definitions for App, Mini Program, H5, and Mini Game properties. It is intended for workflows that require careful parameter validation, duplicate checks, and user confirmation before write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that the skill instructs agents to send extra telemetry containing the user's AppKey. <br>
Mitigation: Review before installing and remove or disable umeng-cli trace steps that report AppKey values unless the organization has explicitly approved that telemetry. <br>
Risk: The skill requires Umeng CLI login and local credential caching. <br>
Mitigation: Use the skill only in trusted environments, protect cached credentials, and verify the CLI login state and storage behavior before use. <br>
Risk: The write operations create event definitions that the artifact describes as not deletable, renameable, or editable through the available Umeng OpenAPI. <br>
Mitigation: Validate event names and display names, check for duplicates, and obtain explicit user confirmation before each write operation. <br>


## Reference(s): <br>
- [Skill definition](SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/squall0925/uapp-event-manage) <br>
- [Umeng CLI project](https://github.com/umeng/umeng-cli) <br>
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline umeng-cli shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include validation results, confirmation prompts for write operations, API response summaries, and verification guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
