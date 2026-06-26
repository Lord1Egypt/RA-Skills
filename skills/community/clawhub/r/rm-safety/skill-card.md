## Description: <br>
Intercepts risky rm commands to assess impact, confirm user intent, and suggest safer alternatives before execution to prevent accidental data loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caesaryp](https://clawhub.ai/user/caesaryp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and CLI users use this skill to add a confirmation layer around file deletion commands, inspect deletion impact, and choose safer alternatives such as trash or backup before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may approve deletion of the wrong path or an important user folder. <br>
Mitigation: Check the absolute target path, file counts, and whether the target is inside a critical folder before approving execution. <br>
Risk: Permanent rm deletion may be difficult to recover. <br>
Mitigation: Prefer the trash option when recoverability matters, or choose backup before executing the original deletion command. <br>
Risk: Creating a backup can place a temporary local copy under /tmp. <br>
Mitigation: Review whether the files are sensitive before choosing backup and remove temporary copies when they are no longer needed. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/caesaryp/rm-safety) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with confirmation prompts and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese guidance; confirmation options include execute, cancel, backup, and trash.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
