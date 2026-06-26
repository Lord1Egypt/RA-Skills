## Description: <br>
Workspace Documentation and Tree Database Manager. SQLite-based indexing for all documentation, files, and directory structures with CSV/JSON export capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to create and query local SQLite indexes for workspace documentation, skills, symlinks, and directory tree metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may broadly catalog workspace documentation and file-tree metadata. <br>
Mitigation: Before running referenced scripts, verify the scanned paths and add exclusions for private or sensitive directories. <br>
Risk: The skill relies on missing or external scripts and mentions an optional scheduled updater. <br>
Mitigation: Verify script sources, schedules, logging, and uninstall steps before enabling automation such as a cron maintainer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kikikari/workspace-db) <br>
- [README.md](README.md) <br>
- [INSTALL.md](INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and SQL command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to create local SQLite databases and CSV or JSON exports in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
