## Description: <br>
查询围棋选手段位、等级分、排名信息，支持手谈等级分和易查分业余段位双平台查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangbin2025](https://clawhub.ai/user/zhangbin2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up public Go player ratings, ranks, dan levels, and related records from supported Chinese Go information platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Player names entered for lookup are sent to dzqzd.com and yichafen.com. <br>
Mitigation: Avoid sensitive personal lookups and use the skill only when sharing the searched name with those external sites is acceptable. <br>
Risk: The yichafen lookup uses local Playwright/Chromium browser automation and can retain temporary browser state on disk. <br>
Mitigation: Clear /tmp/yichafen_browser_data and /tmp/yichafen_state.json when local browser-state retention matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangbin2025/weiqi-player) <br>
- [易查分业余围棋段位查询](https://yeyuweiqi.yichafen.com/qz/s9W2g0zKmt) <br>
- [手谈等级分查询 endpoint](https://v.dzqzd.com/SpBody.aspx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with player lookup results, clickable source links, and performance timing reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public player rank, rating, region, event notes, source links, and elapsed query time.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
