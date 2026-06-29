## Description: <br>
一键部署2026世界杯实时比分系统，双数据源（worldcup26.ir + 直播吧），免API Key，纯前端+Node.js <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy a Chinese-language 2026 FIFA World Cup live scores site with schedules, standings, team squads, live events, and match statistics from free data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script pulls changing external code before installation. <br>
Mitigation: Review the referenced repository, pin it to a known commit, and run installation in a container or disposable host. <br>
Risk: The setup script can terminate any process already using port 3001. <br>
Mitigation: Check port usage before running the script and avoid one-click setup on hosts where port 3001 may be used by another service. <br>
Risk: The deployed Node.js server is started as a background process. <br>
Mitigation: Confirm how to inspect logs and stop the process before installation, or run it under an explicit process manager. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuboacean/worldcup-2026-scores) <br>
- [Referenced deployment repository](https://github.com/liuboacean/WorldCup-2026) <br>
- [worldcup26.ir data source](https://worldcup26.ir) <br>
- [qiumibao live data source](https://s.qiumibao.com) <br>
- [qiumibao detail data source](https://dc.qiumibao.com) <br>
- [qiumibao score data source](https://bifen4m.qiumibao.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May clone and run an external Node.js application; review before execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
