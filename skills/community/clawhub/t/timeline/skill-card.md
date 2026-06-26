## Description: <br>
Log dated events and facts to a queryable personal timeline for remembering events, medical notes, family moments, and milestones without cluttering a calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levineam](https://clawhub.ai/user/levineam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agent users use this skill to log personal events, milestones, medical notes, and other dated facts into a local Markdown timeline, then search or list those entries later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timeline entries are saved as plaintext in the user's local vault and may include sensitive personal, family, or medical details. <br>
Mitigation: Set VAULT_PATH to the intended private vault location and avoid logging sensitive details unless the user wants them retained and searchable by local tools, backups, or other users with access. <br>


## Reference(s): <br>
- [Timeline Skill on ClawHub](https://clawhub.ai/levineam/timeline) <br>
- [Publisher profile](https://clawhub.ai/user/levineam) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown timeline entries and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated entries to a local Timeline.md file under VAULT_PATH or the script default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
