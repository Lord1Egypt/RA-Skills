## Description: <br>
Automates OpenClaw skill management by checking for updates, browsing the ClawHub marketplace, recommending useful skills, and safely installing low-risk skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cooperiano](https://clawhub.ai/user/cooperiano) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor installed skills, discover marketplace recommendations, apply risk-based installation decisions, and generate management reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently and automatically install other skills, changing the user's agent environment under broad trust assumptions. <br>
Mitigation: Keep automatic installation disabled until the trust criteria and recommended skills have been reviewed manually. <br>
Risk: Recurring automation can continue modifying the OpenClaw environment after initial setup. <br>
Mitigation: Confirm the cron schedule before enabling the skill and periodically review generated reports and installation logs. <br>
Risk: The security review notes that VirusTotal was pending and was not used for the verdict. <br>
Mitigation: Treat the release as requiring manual review before installation and scan recommended skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cooperiano/skills-auto-manager) <br>
- [ClawHub marketplace](https://clawhub.ai/skills) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run recurring OpenClaw skill checks, marketplace scans, recommendations, installation decisions, and status reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
