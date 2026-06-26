## Description: <br>
Manage YouTube i18n regions and list available internationalization regions through the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover YouTube Data API internationalization regions through documented yutu CLI commands. It is useful when configuring YouTube API workflows that need valid region identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow requires Google OAuth credential and cached token files, and the security summary notes that exact permissions and protection steps are not fully explained. <br>
Mitigation: Verify the yutu CLI source and OAuth consent scopes before installing, use a dedicated Google project or test account where practical, keep credential files out of repositories, restrict file access, and revoke or delete cached tokens when finished. <br>


## Reference(s): <br>
- [I18n Region List](references/i18nRegion-list.md) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Yutu Homepage](https://github.com/eat-pray-ai/yutu) <br>
- [ClawHub Skill Page](https://clawhub.ai/OpenWaygate/youtube-i18n-region) <br>
- [OpenWaygate Publisher Profile](https://clawhub.ai/user/OpenWaygate) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the yutu CLI plus Google OAuth credential and cached token files before use.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
