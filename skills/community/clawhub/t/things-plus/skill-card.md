## Description: <br>
Personal task manager powered by Things 3 that lets an agent capture, review, organize, reprioritize, search, and manage tasks in the local Things database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sars666](https://clawhub.ai/user/sars666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage Things 3 tasks through the local `things` CLI, including task capture, scheduling, duplicate checks, updates, deletes, and daily logbook summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a real personal Things 3 database from broad everyday planning language without requiring confirmation. <br>
Mitigation: Require confirmation for inferred captures, deletes, bulk edits, and test cleanup runs when deploying in a sensitive personal or shared environment. <br>
Risk: The skill depends on a third-party Things CLI and may require local database access or a Things auth token. <br>
Mitigation: Review the third-party CLI before installation, keep THINGS_AUTH_TOKEN in the environment rather than chat, and grant Full Disk Access only when necessary. <br>


## Reference(s): <br>
- [Things Plus Delete-Focused Test Report](artifact/references/report.md) <br>
- [Things Plus Integrated Test Prompt](artifact/references/test_prompt.md) <br>
- [ClawHub skill page](https://clawhub.ai/sars666/things-plus) <br>
- [Publisher profile](https://clawhub.ai/user/sars666) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise task-management summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and modify a local Things 3 database through the `things` CLI; requires the `things` binary and may require THINGS_AUTH_TOKEN for some operations.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
