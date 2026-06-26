## Description: <br>
Searches WeChat public account articles through WeRead search and returns titles, account names, timestamps, summaries, and direct article links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanikig](https://clawhub.ai/user/kanikig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to find recent WeChat public account articles when they need publication timing, article summaries, and direct mp.weixin.qq.com links. It is intended for search and link discovery, not article-body scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad browser control through CDP and a logged-in WeRead session. <br>
Mitigation: Use an isolated browser profile, avoid normal browsing profiles, and do not expose the CDP endpoint on 0.0.0.0 beyond the required local workflow. <br>
Risk: Login QR images and search result files may remain in shared temporary paths. <br>
Mitigation: Delete temporary QR and result files after use, including /tmp/weread_qr.png and generated /tmp URL JSON files. <br>
Risk: WSL portproxy and firewall rules can leave browser debugging reachable after the task. <br>
Mitigation: Remove Windows portproxy and firewall rules after use and reconnect only for dedicated search sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kanikig/wechat-search-weread) <br>
- [README](README.md) <br>
- [Detailed workflow](references/detailed-workflow.md) <br>
- [Extraction pattern](references/extraction-pattern.md) <br>
- [API limitations](references/api-limitations.md) <br>
- [WSL CDP browser setup](references/wsl-cdp-browser.md) <br>
- [CDP patterns](references/cdp-patterns.md) <br>
- [Edge CDP scroll issue](references/edge-cdp-scroll-issue.md) <br>
- [LLM filter pattern](references/llm-filter-pattern.md) <br>
- [Topology optimization filter](references/topology-optimization-filter.md) <br>
- [agent-browser dependency](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with article lists, inline commands, and JSON result files such as /tmp/urls.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in WeRead browser session; search data and QR/result files may be written to shared temporary paths.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
