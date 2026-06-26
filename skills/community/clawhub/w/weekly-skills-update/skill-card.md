## Description: <br>
Automatically updates installed skills when triggered, runs `clawhub update --all`, updates `SKILLS_INDEX.md` when the skill list changes, and returns an update summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ken0122](https://clawhub.ai/user/ken0122) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run periodic ClawHub skill updates, maintain a skills index, and receive a concise status summary after the update attempt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A simple trigger can bulk-update all installed skills and change the agent environment without a clear confirmation or rollback step. <br>
Mitigation: Run the update manually with review, keep backups or a rollback path, and approve any destination that receives update summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ken0122/weekly-skills-update) <br>
- [Publisher profile](https://clawhub.ai/user/ken0122) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown summary with shell commands and file update notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update installed skills, SKILLS_INDEX.md, and dated update log files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
