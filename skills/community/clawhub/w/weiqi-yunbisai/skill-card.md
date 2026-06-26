## Description: <br>
Queries public Yunbisai Go tournament data, including event lists, groups, pairings, player records, and rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangbin2025](https://clawhub.ai/user/zhangbin2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up public Yunbisai Go tournament information, inspect groups and pairings, and calculate ranking tables for players or events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries Yunbisai public APIs and depends on remote public event data. <br>
Mitigation: Use it for public tournament lookup only and verify important ranking or event outputs against the source service before relying on them. <br>
Risk: Generated JSON and HTML reports may include public player, organizer, or contact details. <br>
Mitigation: Review generated files before sharing them and avoid redistributing contact details beyond the intended tournament context. <br>
Risk: The skill may write generated HTML reports to /tmp. <br>
Mitigation: Inspect generated /tmp report paths before sending or attaching them, and delete local reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangbin2025/weiqi-yunbisai) <br>
- [Yunbisai public website](https://www.yunbisai.com/) <br>
- [Yunbisai event list API](https://data-center.yunbisai.com/api/lswl-events) <br>
- [Yunbisai event group API](https://open.yunbisai.com/api/event/feel/list) <br>
- [Yunbisai pairing API](https://api.yunbisai.com//request/Group/Againstplan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML files, shell commands] <br>
**Output Format:** [Markdown text, JSON responses, and generated HTML reports under /tmp.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries Yunbisai public APIs and may require installing requests. Review generated JSON or HTML before sharing because public event records can include player names and organizer contact details.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
