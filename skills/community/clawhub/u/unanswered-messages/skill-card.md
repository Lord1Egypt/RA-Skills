## Description: <br>
Track and find unanswered messages using a local file-based inbox with no database required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to log incoming messages that need replies, find recent unanswered messages, mark replies as answered, and clean up old answered entries in a local inbox file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The inbox file can contain personal message content and contact details. <br>
Mitigation: Store the file in an access-controlled workspace and limit logged message bodies to the short previews needed for follow-up. <br>
Risk: The skill writes directly to a local JSON file, so concurrent edits or malformed entries could corrupt tracking state. <br>
Mitigation: Review generated file operations before use, keep backups for the inbox file, and validate the JSON structure after updates. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python code snippets and message report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local file paths, JSON inbox fields, message previews, and heartbeat check guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
