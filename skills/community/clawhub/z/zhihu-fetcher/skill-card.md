## Description: <br>
Zhihu Data Fetcher helps agents collect Zhihu hot-list data through browser-profile, file-cookie, or unauthenticated fallback-source retrieval, then save and inspect the results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch Zhihu hot-list data, persist it to SQLite, query historical results, and generate a local HTML visualization. It is intended for data-source workflows where the user can choose between a logged-in browser profile, configured file cookies, or fallback data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled or user-supplied Zhihu cookie values can expose account session material. <br>
Mitigation: Remove bundled cookie values before use and avoid pasting personal Zhihu session cookies unless the account-risk exposure is acceptable. <br>
Risk: Anti-crawl and diagnostic scripts can create account, service, or compliance risk when run against Zhihu. <br>
Mitigation: Avoid running the anti-crawl and diagnostic scripts during normal use; prefer unauthenticated fallback data or an isolated browser session. <br>
Risk: The package was flagged as suspicious by the authoritative security scan. <br>
Mitigation: Review the skill before installing or executing it, and follow the security guidance supplied by the scan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noah-1106/zhihu-fetcher) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/noah-1106) <br>
- [Zhihu](https://www.zhihu.com) <br>
- [Zhihu hot list](https://www.zhihu.com/hot) <br>
- [Configured fallback source](https://raw.githubusercontent.com/SnailDev/zhihu-hot-hub/master/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, HTML files, SQLite data] <br>
**Output Format:** [Markdown guidance with bash, JavaScript, Python, SQL, and JSON examples; runtime scripts emit JSON data, SQLite records, terminal summaries, and a local HTML report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configurable authentication fallback chain and rate limiting; may read cookie values from configuration when file-cookie mode is enabled.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
