## Description: <br>
Collects multi-channel Weibo hot search rankings, stores the data in SQLite, and generates local HTML visualization reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and social media analysts use this skill to collect Weibo trending topics across hot, social, entertainment, and life channels, then query stored history or generate local reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls an OpenClaw browser profile for Weibo and stores scraped trend data locally. <br>
Mitigation: Use a dedicated low-privilege browser profile and review the local database and generated files before sharing them. <br>
Risk: Unsafe command construction and missing URL validation were identified by the security guidance. <br>
Mitigation: Avoid the optional detailed-content fetch until shell=True usage and URL validation are fixed. <br>
Risk: Generated HTML reports render scraped titles and links as local files. <br>
Mitigation: Treat generated HTML as untrusted local content and open it only in a controlled browser context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/noah-1106/weibo-trending) <br>
- [Publisher Profile](https://clawhub.ai/user/noah-1106) <br>
- [Weibo Hot Search](https://weibo.com/hot/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON data, SQLite records, and local HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an OpenClaw browser profile, stores scraped trend data locally, and can render a browser-readable HTML report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
