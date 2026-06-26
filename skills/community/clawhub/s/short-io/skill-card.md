## Description: <br>
Use this skill to manage Short.io branded short links via their REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godsboy](https://clawhub.ai/user/godsboy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, marketers, and site operators use this skill to create, list, inspect, archive, delete, and analyze Short.io branded short links from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Short.io secret API key. <br>
Mitigation: Use a revocable Short.io API key, store it in a private secrets file, and keep the secrets file permissions restricted. <br>
Risk: Delete and archive operations can modify or remove Short.io links. <br>
Mitigation: Verify link IDs before destructive operations and require explicit human confirmation before delete or archive commands. <br>
Risk: The server security summary reports a URL-handling bug in the find command that can run local code with untrusted URLs. <br>
Mitigation: Avoid the find command with untrusted URLs until the URL encoding bug is fixed. <br>


## Reference(s): <br>
- [Short.io Skill Page](https://clawhub.ai/godsboy/short-io) <br>
- [Publisher Profile](https://clawhub.ai/user/godsboy) <br>
- [Short.io](https://short.io) <br>
- [Short.io API Reference](references/api.md) <br>
- [Short.io Main API](https://api.short.io) <br>
- [Short.io Statistics API](https://statistics.short.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHORT_IO_API_KEY and local tools: curl, jq, python3, and column.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
