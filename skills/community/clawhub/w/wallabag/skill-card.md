## Description: <br>
Manage Wallabag bookmarks through the Wallabag Developer API with OAuth2 authentication, including creating, reading, updating, deleting, searching, and tag management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fbrandel](https://clawhub.ai/user/fbrandel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to connect to a Wallabag instance, save links, retrieve entries, search bookmarks, update metadata, manage tags, and delete entries through deterministic shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted bookmark, search, or tag text may cause unintended local command execution in the bundled shell script. <br>
Mitigation: Patch scripts/wallabag.sh to remove eval-based argument construction before deployment, or install only after trusting and reviewing the publisher's release. <br>
Risk: OAuth password grant uses full Wallabag account credentials, and auth --show-token can expose access tokens in logs or terminal history. <br>
Mitigation: Use a trusted HTTPS Wallabag instance, prefer a dedicated low-privilege account, keep credentials in environment variables, and avoid auth --show-token in logged sessions. <br>
Risk: Delete operations can permanently remove Wallabag entries. <br>
Mitigation: Require clear user confirmation before running delete commands. <br>


## Reference(s): <br>
- [Wallabag API Notes Used By This Skill](references/wallabag-api.md) <br>
- [Wallabag OAuth docs](https://doc.wallabag.org/developer/api/oauth/) <br>
- [Wallabag API docs](https://app.wallabag.it/api/doc/) <br>
- [Wallabag project](https://www.wallabag.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Wallabag credentials in environment variables; tag add and tag remove require jq.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
