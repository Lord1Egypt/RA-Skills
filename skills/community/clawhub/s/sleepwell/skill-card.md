## Description: <br>
Track sleep-related habits and local productivity notes with commands for logging, reviewing, searching, and exporting entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to log sleep or productivity entries locally, review recent history and statistics, search notes, and export records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is marketed as a sleep tracker but includes broad local productivity logging with persistent, searchable, exportable notes. <br>
Mitigation: Treat it as a local productivity logger; avoid entering secrets, credentials, sensitive work details, or private health notes. <br>
Risk: Local data may be stored in both ~/.local/share/sleepwell and ~/.sleep. <br>
Mitigation: Review and manage both storage paths before and after use, and add deletion or privacy controls before broader deployment. <br>
Risk: The sleep diary script has Python argument handling concerns identified by the security evidence. <br>
Mitigation: Review and fix the sleep_diary.sh argument handling before relying on those commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/sleepwell) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text command output with generated JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores persistent local logs under ~/.local/share/sleepwell and ~/.sleep.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
