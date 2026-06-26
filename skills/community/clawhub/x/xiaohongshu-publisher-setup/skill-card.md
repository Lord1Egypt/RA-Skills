## Description: <br>
Deploys a Xiaohongshu publishing agent team for content formatting, browser-assisted publishing, and basic analytics; it is triggered with /xiaohongshu-publisher-setup and requires the content-creation team. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[little-ke](https://clawhub.ai/user/little-ke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to install a two-agent Xiaohongshu workflow that formats content packages, registers the publishing agents, initializes a local login session, and guides confirmed publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow saves local Xiaohongshu account profile data and browser session state. <br>
Mitigation: Protect ~/.openclaw/workspace-xiaohongshu-publisher, and delete .session/state.json and .env when retained login or profile state is no longer needed. <br>
Risk: Browser automation can publish content to a live Xiaohongshu account. <br>
Mitigation: Review the generated content package and confirm publishing only when the title, body, images, tags, and login state are correct. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/little-ke/xiaohongshu-publisher-setup) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com) <br>
- [Xiaohongshu publish page](https://creator.xiaohongshu.com/publish/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local agent workspaces, account profile configuration, and Playwright session state under ~/.openclaw/workspace-xiaohongshu-publisher.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
