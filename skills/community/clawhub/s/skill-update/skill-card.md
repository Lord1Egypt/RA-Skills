## Description: <br>
Safely update skills with preview, migration support, and user validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to preview, explain, approve, back up, apply, verify, migrate, and roll back skill updates while keeping user-controlled workflows intact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to change local skill files, including moves or deletions during updates. <br>
Mitigation: Review the preview and migration plan, approve only the intended skill and version, and confirm a backup exists before allowing file changes. <br>
Risk: Incomplete review of update differences could lead to broken workflows or data loss. <br>
Mitigation: Use the documented check, preview, explain, confirm, backup, update, and verify flow before applying an update. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skill-update) <br>
- [Preview Changes](preview.md) <br>
- [Migration Strategies](migrate.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only skill; no executable code files are included in the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
