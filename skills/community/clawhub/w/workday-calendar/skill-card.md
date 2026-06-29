## Description: <br>
workday-calendar helps agents manage local workday calendars, statutory holidays, make-up workdays, rotation schedules, special rest days, personal schedules, and HTML or JSON calendar exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to calculate workdays, manage holiday and compensatory-work rules, maintain local schedules, configure rotation or special rest patterns, and export calendar views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports an unauthenticated configuration web server that can be LAN-reachable. <br>
Mitigation: Run the web UI only in trusted environments, bind it to localhost or firewall the port, and stop the server when configuration is complete. <br>
Risk: The skill stores schedule data locally. <br>
Mitigation: Review the configured data directory before use and avoid storing sensitive calendar information where local users or backups may expose it. <br>
Risk: The skill can create executable Windows backup files. <br>
Mitigation: Inspect and trust generated .bat backups before running them, and use normal file restore workflows when possible. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ldxs001/skills/workday-calendar) <br>
- [Usage guide](references/guide.md) <br>
- [CLI command reference](references/cli.md) <br>
- [Data format specification](references/data_format.md) <br>
- [Permissions and testing](references/permissions.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown and text guidance with Python or shell commands, plus JSON data and exported HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores schedule and calendar data locally and can generate local backup files and calendar exports.] <br>

## Skill Version(s): <br>
2.2.0 (source: release evidence, frontmatter, and changelog, released 2026-06-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
