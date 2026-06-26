## Description: <br>
Timeblock helps users plan a day hour-by-hour with intentional time blocking for blocking sessions, checking plans, analyzing allocation, and generating agendas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Timeblock to log planned and actual schedule blocks, check adherence, analyze time allocation, search history, and export local time-block records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Time-block notes are stored locally and may include sensitive personal, location, or work details. <br>
Mitigation: Use the skill only on a trusted local account, avoid entering highly sensitive information, and periodically review or delete logs under ~/.local/share/timeblock. <br>
Risk: The skill runs a shell script that creates and updates files in the user's home directory. <br>
Mitigation: Review the script before installation and confirm the local data path is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Timeblock listing](https://clawhub.ai/xueyetianya/timeblock) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and local log or export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local logs and export files under ~/.local/share/timeblock/.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
