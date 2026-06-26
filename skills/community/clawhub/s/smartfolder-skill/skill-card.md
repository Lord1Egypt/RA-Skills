## Description: <br>
SmartFolder helps an agent organize local folders, find duplicate files, and analyze disk usage through a Python command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zaosusu](https://clawhub.ai/user/Zaosusu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to preview and run local folder organization, duplicate discovery, and disk usage analysis for explicitly chosen paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move files in local folders by default. <br>
Mitigation: Use explicit target paths, run dry-run previews first, avoid home-root or system directories, and keep backups for important folders. <br>
Risk: The documentation advertises confirmation, trash, and undo protections that the security evidence says are not implemented in the script. <br>
Mitigation: Do not rely on those protections; review planned operations manually and avoid destructive cleanup assumptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zaosusu/smartfolder-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run local file moves; dry-run output lists planned operations before execution.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
