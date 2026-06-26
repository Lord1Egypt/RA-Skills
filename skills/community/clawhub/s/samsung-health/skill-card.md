## Description: <br>
Analyze Samsung Health Connect data synced to Google Drive for sleep, steps, heart rate, SpO2, workouts, and daily health reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mudgesbot](https://clawhub.ai/user/mudgesbot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers with Samsung Health Connect backups use this skill to configure a local CLI, sync Health Connect exports from Google Drive, and request health summaries or machine-readable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Samsung Health backup data from the configured Google Drive account. <br>
Mitigation: Install only when comfortable granting that local CLI access, use a Google account with the minimum necessary Drive access, and protect downloaded Health Connect.zip files. <br>
Risk: The release installs and runs a third-party Python CLI from the referenced repository. <br>
Mitigation: Review the repository before installation and run it in a virtualenv or isolated machine. <br>
Risk: Local configuration stores the Google Drive folder, account, and health data handling settings. <br>
Mitigation: Protect ~/.config/samsung-health/config.yaml and avoid sharing local configuration or generated reports that may expose health data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mudgesbot/samsung-health) <br>
- [Publisher profile](https://clawhub.ai/user/mudgesbot) <br>
- [samsung-health-skill repository](https://github.com/mudgesbot/samsung-health-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local access to Samsung Health Connect backup data in Google Drive through the configured gog CLI account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
