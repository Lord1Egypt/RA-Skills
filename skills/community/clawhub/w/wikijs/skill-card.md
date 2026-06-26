## Description: <br>
Command-line tool to manage Wiki.js content, pages, assets, templates, and backups via its GraphQL API with search, update, sync, and analysis functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hopyky](https://clawhub.ai/user/hopyky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content operators use this skill to let an agent manage Wiki.js pages, assets, backups, templates, search, synchronization, and content quality checks through a CLI backed by the Wiki.js GraphQL API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, restore, replace, and bulk-modify Wiki.js content and assets. <br>
Mitigation: Use a least-privilege Wiki.js API token and review destructive, restore, replace, and bulk commands before approval. <br>
Risk: The skill stores Wiki.js connection details and API credentials in a local configuration file. <br>
Mitigation: Protect ~/.config/wikijs.json and avoid sharing logs or files that contain API tokens. <br>
Risk: The skill can upload local files to Wiki.js. <br>
Mitigation: Approve uploads only for files intentionally meant to be published or stored in the Wiki.js instance. <br>


## Reference(s): <br>
- [ClawHub Wiki.js CLI release](https://clawhub.ai/hopyky/wikijs) <br>
- [Wiki.js](https://js.wiki/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON configuration examples, and machine-readable command output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a Wiki.js instance, read local configuration, write local backup or sync files, and modify wiki pages or assets when the user approves commands.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata, CHANGELOG, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
