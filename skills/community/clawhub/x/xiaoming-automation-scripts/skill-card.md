## Description: <br>
Automation Scripts helps agents work with common local automation tasks such as batch renaming, backups, scheduled jobs, web screenshots, and data scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to automate repetitive local tasks, including batch file renaming, backups, scheduled commands, web screenshots, and data scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local automation commands may affect files outside the intended scope if source, destination, or pattern arguments are too broad. <br>
Mitigation: Review exact paths and patterns before execution, and prefer a small test directory before running bulk rename or backup commands. <br>
Risk: Scheduled commands can repeatedly run broad, destructive, or privacy-sensitive tasks. <br>
Mitigation: Confirm the cron expression and command payload before scheduling, and avoid unattended jobs until their behavior is verified. <br>
Risk: Screenshot and scraping targets may expose private data or conflict with site terms. <br>
Mitigation: Review target URLs for privacy, authorization, and terms-of-use concerns before capturing or scraping content. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/xiaoming-automation-scripts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local paths, cron expressions, URLs, and commands that depend on curl.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
