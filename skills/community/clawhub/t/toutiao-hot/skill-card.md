## Description: <br>
Fetches Toutiao hot-board entries and can save, query, and visualize hot news rankings with titles, heat values, links, covers, labels, cluster IDs, and categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch current Chinese hot-news rankings from Toutiao, inspect the returned ranking data, and optionally persist or visualize it for trend review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: One helper script can execute code from an unrelated local OpenClaw skill path. <br>
Mitigation: Use the documented package-local scripts that call the bundled scripts/toutiao.js, and avoid scripts/fetch-toutiao.py unless it is fixed to reference only package-local code. <br>
Risk: Generated HTML reports render external news data unsafely. <br>
Mitigation: Treat generated HTML as untrusted until external data is escaped and links are validated. <br>
Risk: The skill can store fetched history in local SQLite and HTML report files. <br>
Mitigation: Delete data/toutiao.db and data/index.html when stored history is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noah-1106/toutiao-hot) <br>
- [Toutiao hot-board endpoint](https://www.toutiao.com/hot-event/hot-board/) <br>
- [Toutiao website](https://www.toutiao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files, shell commands, guidance] <br>
**Output Format:** [JSON hot-list data, terminal text output, SQLite data files, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default hot-list limit is 50 items; command input can request a different top-N limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
