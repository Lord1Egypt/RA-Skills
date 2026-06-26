## Description: <br>
网络安全情报爬虫定期抓取安全社区 RSS、NVD、cxsecurity 和安全客的安全新闻与漏洞情报，并将按日期整理的中文笔记写入 IMA。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fallenqu](https://clawhub.ai/user/fallenqu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, developers, and operations teams use this skill to collect recent cybersecurity news and CVE-oriented vulnerability intelligence into daily IMA notes. It supports manual runs, scheduled crawler operation, RSS source management, URL/CVE deduplication, and Chinese translation of English vulnerability descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses IMA note-writing credentials and may use a MiniMax key from local OpenClaw configuration. <br>
Mitigation: Provide credentials explicitly through environment variables, remove or document the OpenClaw config fallback, avoid hardcoded credentials, and rotate exposed keys. <br>
Risk: Recurring crawler automation can repeatedly fetch external sources and write to IMA notes. <br>
Mitigation: Review cron entries and logs before enabling scheduled runs, test with a manual execution first, and provide clear enable, disable, and inspection controls. <br>
Risk: Some crawler paths disable TLS verification for fallback vulnerability feeds. <br>
Mitigation: Prefer feeds with valid TLS, enable certificate verification where possible, and treat unverified feed content as untrusted input. <br>


## Reference(s): <br>
- [RSS Source Status Reference](artifact/references/rss-sources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fallenqu/sec-news-crawler) <br>
- [NVD CVE API](https://services.nvd.nist.gov/rest/json/cves/2.0/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated IMA note content and maintains local JSON deduplication state.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
