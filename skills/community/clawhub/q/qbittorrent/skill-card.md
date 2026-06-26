## Description: <br>
Manage torrents with qBittorrent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmagar](https://clawhub.ai/user/jmagar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage qBittorrent torrents through the WebUI API, including listing, adding, pausing, resuming, deleting, rechecking, tagging, and speed-limit operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete torrents and, with the files option, remove downloaded data. <br>
Mitigation: Require explicit user confirmation before delete operations, especially delete with files or broad all-target actions. <br>
Risk: The qBittorrent WebUI session cookie may be stored in a predictable temporary path. <br>
Mitigation: Set QBIT_COOKIE to a private path with 0600 permissions and protect the credentials configuration file. <br>
Risk: The agent can control a qBittorrent WebUI instance. <br>
Mitigation: Use strong non-default WebUI credentials and prefer localhost or HTTPS access. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses qBittorrent WebUI credentials from a local configuration file or environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
