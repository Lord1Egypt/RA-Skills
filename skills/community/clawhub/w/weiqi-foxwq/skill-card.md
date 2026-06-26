## Description: <br>
weiqi-foxwq 野狐棋谱下载 - 自动从野狐围棋网站下载棋谱，支持分享链接提取（API历史棋谱/WebSocket实时）、按日期下载，含性能计时报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangbin2025](https://clawhub.ai/user/zhangbin2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Go players, and automation users use this skill to download public Foxwq game records as SGF files from share links, public player lookups, or date-based game lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Foxwq services and writes downloaded SGF files locally. <br>
Mitigation: Run it in a Python virtual environment and choose an explicit output directory when saving files. <br>
Risk: WebSocket mode uses Playwright and processes live share-link data. <br>
Mitigation: Prefer API mode for historical games and use WebSocket mode only with trusted Foxwq links. <br>
Risk: Nickname downloads can fetch multiple public records and create many local files. <br>
Mitigation: Set --limit and --output-dir explicitly before running nickname-based downloads. <br>
Risk: The artifact includes its own security-audit statement. <br>
Mitigation: Use the server security evidence as the review source instead of treating the skill's self-attestation as independent assurance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangbin2025/weiqi-foxwq) <br>
- [Foxwq game records page](https://www.foxwq.com/qipu.html) <br>
- [Foxwq chess fetch endpoint](https://h5.foxwq.com/yehuDiamond/chessbook_local/YHWQFetchChess) <br>
- [Foxwq user lookup endpoint](https://newframe.foxwq.com/cgi/QueryUserInfoPanel) <br>
- [Foxwq chess list endpoint](https://h5.foxwq.com/yehuDiamond/chessbook_local/YHWQFetchChessList) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated SGF files when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes SGF files to /tmp by default or to user-specified output paths.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
