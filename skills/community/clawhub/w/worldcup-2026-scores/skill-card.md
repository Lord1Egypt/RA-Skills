## Description:

一键部署2026世界杯实时比分系统，双数据源（worldcup26.ir + 直播吧），免API Key，纯前端+Node.js。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to deploy a Node.js and static frontend site for 2026 FIFA World Cup live scores, schedules, standings, squads, match events, and statistics. The skill is intended for users who want a no-API-key deployment backed by the declared free data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can run unpinned remote code and install dependencies before local review.

Mitigation: Pin the external repository and dependency versions, inspect the checkout and dependency manifest, and run only in an isolated or disposable environment.

Risk: The setup script can kill any process currently using port 3001.

Mitigation: Remove or explicitly confirm the port-killing behavior before execution, and choose a managed port allocation when deploying on shared hosts.

Risk: The service is started in the background without clear lifecycle controls.

Mitigation: Prefer foreground execution during review or run it under a managed service with explicit start, stop, status, and log handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuboacean/skills/worldcup-2026-scores)
- [Declared project repository](https://github.com/liuboacean/WorldCup-2026)
- [worldcup26.ir data source](https://worldcup26.ir)
- [qiumibao live data endpoint](https://s.qiumibao.com)
- [qiumibao detail data endpoint](https://dc.qiumibao.com)
- [qiumibao mobile score endpoint](https://bifen4m.qiumibao.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and deployment notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local Node.js service on port 3001 when the bundled setup script is run.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
