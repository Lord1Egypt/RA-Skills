## Description: <br>
Manage YouTube i18n languages by guiding an agent to list available internationalization languages with the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and YouTube API users can use this skill to list supported YouTube internationalization languages and prepare the yutu CLI authentication needed to run that command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube OAuth credential and token files are sensitive local secrets. <br>
Mitigation: Keep client_secret.json and youtube.token.json private, out of repositories and shared folders; revoke or rotate tokens if either file is exposed. <br>
Risk: The skill relies on the third-party yutu CLI and requires YouTube API access. <br>
Mitigation: Install only if you trust the yutu CLI package and are comfortable granting it YouTube API access. <br>


## Reference(s): <br>
- [I18n Language List](references/i18nLanguage-list.md) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [yutu GitHub repository](https://github.com/eat-pray-ai/yutu) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI flag tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include yutu CLI commands, setup steps, and output-format guidance for table, JSON, or YAML command results.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
