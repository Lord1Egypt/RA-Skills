## Description: <br>
Rivalwatch helps agents track, analyze, compare, and export local competitive intelligence data for competitor analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Rivalwatch to log competitor updates, compare positioning, search activity history, and export locally stored competitive intelligence for reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Entries and exports are stored locally under ~/.local/share/rivalwatch and may contain confidential competitor intelligence. <br>
Mitigation: Avoid entering secrets or sensitive business data unless local storage is acceptable, and review or remove local logs and exports according to policy. <br>
Risk: Documented export and status utility behavior may differ because the script contains duplicate command branches for those commands. <br>
Mitigation: Test the intended command path before relying on export or status output in automated workflows. <br>


## Reference(s): <br>
- [Rivalwatch on ClawHub](https://clawhub.ai/bytesagain3/rivalwatch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text CLI output with optional JSON, CSV, and TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local logs and export files under ~/.local/share/rivalwatch when the CLI is used.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
