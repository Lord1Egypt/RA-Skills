## Description: <br>
财经热点新闻爬取与话题归纳系统 crawls selected finance news sources, summarizes hot topics, scores news relevance, collects market flashes, and prepares finance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diudiuhuang](https://clawhub.ai/user/diudiuhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance-focused users can use this skill to collect current finance news, group and score hot topics, gather important market flashes, and generate report files for review. It is not intended for non-finance news, weather, entertainment, or gossip coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes reports and logs and can automatically clean configured temp/report paths. <br>
Mitigation: Set temp_dir and reports_dir to dedicated disposable directories before running the workflow, and review the configured paths before enabling cleanup. <br>
Risk: The skill may use configured API credentials and browser profile or cookie paths. <br>
Mitigation: Use scoped API keys, avoid real browser profiles unless required, and remove credential or partial-key logging before use. <br>
Risk: The workflow can make outbound requests to finance websites and model APIs and invokes external commands. <br>
Mitigation: Run it in a controlled environment, review the configured sites and shell execution paths, and confirm that outbound network access is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diudiuhuang/stock-hot-news) <br>
- [Publisher profile](https://clawhub.ai/user/diudiuhuang) <br>
- [README](artifact/README.md) <br>
- [Directory migration notes](artifact/DIRECTORY_MIGRATION.md) <br>
- [Configuration example](artifact/url_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifacts may include JSON, text, and HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured finance source access, local output directories, and model API credentials when model-based scoring or summarization is used.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
