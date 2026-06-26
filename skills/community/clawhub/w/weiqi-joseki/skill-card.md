## Description: <br>
weiqi-joseki v2.1.1 围棋定式数据库 - 基于KataGo棋谱构建。重构版采用多级时序连通性过滤，性能大幅提升。模块化设计，数据完全本地存储。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangbin2025](https://clawhub.ai/user/zhangbin2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Go players, developers, and agents use this skill to build, maintain, inspect, and export a local joseki database from public KataGo SGF archives. It supports extracting corner sequences from SGF files and discovering matching joseki patterns in game records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto mode can download and process large public KataGo SGF archives and create substantial local cache data. <br>
Mitigation: Check available disk space before running auto mode; use --limit or --download-only for testing; keep ~/.weiqi-joseki in a location where large cache files are acceptable. <br>


## Reference(s): <br>
- [KataGo Archive rating games](https://katagoarchive.org/kata1/ratinggames/index.html) <br>
- [ClawHub skill page](https://clawhub.ai/zhangbin2025/weiqi-joseki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local joseki database files, exported JSON or SGF data, and CLI status output.] <br>

## Skill Version(s): <br>
2.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
