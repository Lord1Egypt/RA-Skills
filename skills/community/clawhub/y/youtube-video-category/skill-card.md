## Description: <br>
This skill helps agents list YouTube video categories with the yutu CLI and includes setup guidance for YouTube API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and creators use this skill to list YouTube video category metadata while preparing or automating YouTube workflows with yutu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube OAuth credentials and cached tokens can grant API access if exposed. <br>
Mitigation: Keep client_secret.json and youtube.token.json private, avoid committing or sharing them, use restrictive file permissions or a secret manager where practical, and revoke tokens that are no longer needed. <br>
Risk: The skill depends on a third-party yutu CLI with YouTube API access. <br>
Mitigation: Install yutu only from trusted sources and grant YouTube API access only when the operator trusts the CLI and understands the requested permissions. <br>


## Reference(s): <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Video Category List](references/videoCategory-list.md) <br>
- [yutu project](https://github.com/eat-pray-ai/yutu) <br>
- [yutu README](https://github.com/eat-pray-ai/yutu#readme) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward yutu CLI commands; yutu command results may be table, JSON, or YAML depending on the selected output flag.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
