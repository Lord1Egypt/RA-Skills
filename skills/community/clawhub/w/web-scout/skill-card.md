## Description: <br>
Gives AI agents web collection workflows through Agent Reach for webpages, Twitter/X, Reddit, YouTube, Bilibili, Xiaohongshu, Douyin, GitHub, LinkedIn, Boss Zhipin, RSS, and web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aizain](https://clawhub.ai/user/aizain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to install, configure, and call third-party web collection tools for cross-platform research and content retrieval. It is intended for workflows that need command guidance for web pages, social platforms, RSS, GitHub, and search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run third-party CLI, Docker, and MCP tooling. <br>
Mitigation: Review the Agent Reach and connector sources before installation, start with safe or dry-run modes, and remove containers, watchers, and installed tooling when finished. <br>
Risk: Some platform workflows require live browser cookies or account login state. <br>
Mitigation: Avoid primary-account cookies, prefer throwaway accounts, store only the minimum credentials needed, and delete stored cookies after use. <br>
Risk: Broad web collection can access third-party platforms with different account and network requirements. <br>
Mitigation: Confirm each platform's access requirements and run collection through reviewed connectors and approved network settings. <br>


## Reference(s): <br>
- [ClawHub Web Scout](https://clawhub.ai/aizain/web-scout) <br>
- [Agent Reach](https://github.com/Panniantong/Agent-Reach) <br>
- [Agent Reach source archive](https://github.com/Panniantong/agent-reach/archive/main.zip) <br>
- [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct agents to use optional web fetching and required shell execution tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
