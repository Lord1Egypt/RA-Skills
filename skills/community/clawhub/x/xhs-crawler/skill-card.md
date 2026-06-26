## Description: <br>
爬取小红书笔记和评论内容，支持关键词搜索和基础舆情分析，通常需要本地登录小红书账号运行。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[featherjiaxin-oss](https://clawhub.ai/user/featherjiaxin-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect Xiaohongshu notes and comments for keyword-based public-opinion review and simple engagement-based sentiment summaries. It is intended for controlled research and development workflows that can manage account, platform-rule, and data-retention obligations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crawler use may violate Xiaohongshu rules, applicable privacy law, or account expectations if run aggressively or without authorization. <br>
Mitigation: Use a dedicated account, keep crawl rates low, follow platform terms and local law, and stop collection when access limits or login challenges appear. <br>
Risk: Exports may contain personal or sensitive user-generated content from notes, comments, images, or videos. <br>
Mitigation: Minimize collected fields, secure local Excel/SQLite/media outputs, restrict sharing, and delete datasets when no longer needed. <br>
Risk: Referenced external crawler repositories or APIs may change behavior after release. <br>
Mitigation: Inspect external code before running it, pin dependencies or commits where possible, and run in a virtual environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/featherjiaxin-oss/xhs-crawler) <br>
- [redbooks referenced project](https://github.com/xiaofuqing13/redbooks) <br>
- [jiang-xiaohongshu-crawler referenced project](https://github.com/upJiang/jiang-xiaohongshu-crawler) <br>
- [TikHub API Python SDK referenced project](https://github.com/TikHub/TikHub-API-Python-SDK) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local crawler setup steps and exports such as Excel, SQLite, images, videos, and text summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
