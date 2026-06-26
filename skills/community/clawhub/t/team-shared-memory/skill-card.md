## Description: <br>
Synchronizes shared project and reference memories across OpenClaw agents or workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amd5](https://clawhub.ai/user/amd5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to keep project and reference memory files synchronized across OpenClaw agents or workspaces while leaving user and feedback memories private. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared memory sync can overwrite project or reference memory files during conflict resolution. <br>
Mitigation: Keep backups of important memory files and review synchronization results after conflict-heavy runs. <br>
Risk: Secrets, regulated data, or private notes may be copied into shared memory if users place them in shared folders. <br>
Mitigation: Avoid storing sensitive data in shared memory folders and run the included secret scan before synchronization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amd5/team-shared-memory) <br>
- [Publisher profile](https://clawhub.ai/user/amd5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and command-line status text; synchronization writes Markdown memory files and JSON sync state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >=18.0.0 and local access to the OpenClaw workspace memory directories.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
