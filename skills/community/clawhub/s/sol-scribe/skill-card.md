## Description: <br>
Book writing companion for long-form creative projects - chapter planning, narrative consistency, and AI-assisted drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and creative project maintainers use Solscribe to organize long-form manuscripts into local Markdown chapters, maintain book metadata and chapter status, preserve backups, and export drafts to DOCX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional unauthenticated localhost server can read or modify manuscript data while server.py is running. <br>
Mitigation: Run server.py only when the HTTP interface is required, keep it bound to localhost, and treat localhost:3847 as sensitive on shared or untrusted machines. <br>
Risk: The skill stores manuscript chapters, backups, and session logs on local disk. <br>
Mitigation: Install only when local disk storage is acceptable, and keep the project, backup, and log directories in trusted local locations with appropriate filesystem permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amrree/skills/sol-scribe) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/amrree) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown and plain text responses; Markdown files with YAML frontmatter; optional DOCX exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local chapter files, timestamped backups, session logs, and optional DOCX files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
