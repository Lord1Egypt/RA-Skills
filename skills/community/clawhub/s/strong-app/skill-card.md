## Description: <br>
Interact with the Strong v6 workout tracker REST API to authenticate, list exercises, fetch workout logs and templates, manage folders, tags, measurements, widgets, and share links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanvmoreno](https://clawhub.ai/user/ivanvmoreno) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent query their Strong workout account for profiles, exercises, templates, workout logs, date-range filters, and share links. It is useful for personal training-data lookup and workout-history analysis when the user provides Strong account credentials via environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Strong account credentials and workout data. <br>
Mitigation: Keep STRONG_USERNAME and STRONG_PASSWORD in a trusted local environment, and treat login, refresh, profile, and workout output as sensitive. <br>
Risk: The share_log and share_template commands can create shareable workout or template links. <br>
Mitigation: Run sharing commands only when the user intentionally wants a workout or template link created, and review the returned link before distributing it. <br>
Risk: The Strong API integration is unofficial and reverse-engineered, so API behavior may change. <br>
Mitigation: Review command failures before retrying, and confirm important workout data in the Strong app when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivanvmoreno/strong-app) <br>
- [Strong App](https://www.strong.app/) <br>
- [Strong API (unofficial)](https://github.com/dmzoneill/strongapp-api) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STRONG_USERNAME and STRONG_PASSWORD; commands call https://back.strong.app and print JSON to stdout.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
