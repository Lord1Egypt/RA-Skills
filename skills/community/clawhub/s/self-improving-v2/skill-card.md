## Description: <br>
Helps an agent run scheduled self-reflection, save conversations and media, and organize long-term memory for ongoing improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent persistent memory, scheduled reflection routines, and memory organization habits across ongoing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent retention of chats, images, code, decisions, and user preferences can expose sensitive information. <br>
Mitigation: Install only where long-term retention is intended, and regularly review or delete saved memory and media files. <br>
Risk: Unattended scheduled reflection and cleanup jobs may process or remove data without direct review. <br>
Mitigation: Verify cron or scheduled job definitions before enabling them, and keep scheduled jobs disabled until they have been reviewed. <br>
Risk: The release evidence lists documentation and package metadata but not the scripts or cron definitions described by the artifact. <br>
Mitigation: Confirm required scripts and job configuration exist in the installed package before relying on automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/davidme6/self-improving-v2) <br>
- [Publisher profile](https://clawhub.ai/user/davidme6) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory files, media directories, and scheduled job configuration when implemented by the agent.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact package.json and changelog agree) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
