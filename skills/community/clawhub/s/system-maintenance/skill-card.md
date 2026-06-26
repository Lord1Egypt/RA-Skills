## Description: <br>
Complete maintenance system for OpenClaw with unified architecture, filesystem governance, and cross-platform design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jazzqi](https://clawhub.ai/user/jazzqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to check system status, run local cleanup routines, and configure scheduled maintenance for OpenClaw environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release suspicious because it asks for powerful local actions including file deletion, service restarts, installer execution, and cron persistence. <br>
Mitigation: Review the skill before installing, test in an isolated environment, and back up crontab and OpenClaw data before running maintenance or cron commands. <br>
Risk: The release appears incomplete because referenced maintenance scripts are not present in the artifact. <br>
Mitigation: Do not run one-click setup, restore, service restart, cleanup, or cron installation until the complete package is present and audited at a pinned version. <br>
Risk: Scheduled maintenance can persist through cron and continue changing the local environment after initial setup. <br>
Mitigation: Require dry-run or confirmation behavior and a clear cron removal command before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jazzqi/system-maintenance) <br>
- [Publisher Profile](https://clawhub.ai/user/jazzqi) <br>
- [Project Homepage](https://github.com/jazzqi/openclaw-system-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local maintenance, status, cleanup, and cron-related commands when invoked.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
