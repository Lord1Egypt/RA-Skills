## Description: <br>
Finds DST-aware cross-timezone meeting windows across two or more cities or time zones and ranks them as Optimal, Stretch, or Avoid with Telegram-friendly local-time output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeadland](https://clawhub.ai/user/jeadland) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external collaborators, and scheduling-focused agents use this skill to compare cross-timezone availability and choose meeting windows for groups spanning two or more cities or IANA time zones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved local preferences may reveal a user's timezone, preferred meeting hours, and flexibility setting on shared machines. <br>
Mitigation: Review saved settings with --show-settings or delete ~/.openclaw/skills/world-meeting-coordination-skill/config.json when preference retention is not desired. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/jeadland/world-meeting-coordination-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown-style ranked sections with local time lines and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses 24h and 12h time formats, +1 day markers for date rollover, and ranked Optimal, Stretch, and Avoid sections.] <br>

## Skill Version(s): <br>
0.2.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
