## Description: <br>
subagent-archive guides agents through safe OpenClaw sub-agent session archival and cleanup using dry-run, soft-delete, and enforced cleanup modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoyongxiu](https://clawhub.ai/user/zhaoyongxiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and maintainers use this skill to archive, inspect, and clean sub-agent session files while preserving protected main, cron, and active dashboard sessions. It is intended for workspace maintenance workflows where cleanup plans should be reviewed before any storage changes are enforced. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw session storage when cleanup is enforced. <br>
Mitigation: Run the included script in dry-run first, explicitly set the workspace when needed, and review planned targets before using soft or enforce mode. <br>
Risk: Server security review found inconsistent destructive cleanup guidance. <br>
Mitigation: Prefer soft mode before enforce and do not copy cleanup snippets unless they include an explicit enforce check. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoyongxiu/subagent-archive) <br>
- [Publisher profile](https://clawhub.ai/user/zhaoyongxiu) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [Examples](examples/README.md) <br>
- [Tests](tests/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, code] <br>
**Output Format:** [Markdown guidance with PowerShell commands and optional JSON output from the bundled cleanup script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow defaults to dry-run, supports explicit workspace selection, and can produce JSON summaries for scripted review.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
