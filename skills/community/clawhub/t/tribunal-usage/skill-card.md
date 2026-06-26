## Description: <br>
Use Tribunal commands for TDD enforcement, quality gates, secret scanning, Agent Teams hooks, CI integration, and plugin packs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koshaji](https://clawhub.ai/user/koshaji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to run Tribunal quality gates, configure enforcement modes, inspect audit logs, and integrate checks into Claude Code and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tribunal hooks can intercept development activity and affect file writes, test runs, and agent workflows. <br>
Mitigation: Install it only in repositories where these quality gates are intended and review the configured enforcement mode before use. <br>
Risk: Audit logs may contain local development activity details. <br>
Mitigation: Keep .tribunal/ private or ignored unless the project intentionally shares those logs. <br>
Risk: External Tribunal plugin packs and MCP access can expand the tool's behavior. <br>
Mitigation: Review external plugin packs before installation and use MCP access only from trusted local sessions. <br>


## Reference(s): <br>
- [Tribunal homepage](https://tribunal.dev) <br>
- [Tribunal repository](https://github.com/thebotclub/tribunal) <br>
- [ClawHub skill page](https://clawhub.ai/koshaji/tribunal-usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the tribunal command-line tool for the documented workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
