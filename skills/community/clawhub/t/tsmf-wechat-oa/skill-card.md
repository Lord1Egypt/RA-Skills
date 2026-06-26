## Description: <br>
Guides an agent through WeChat Official Account article planning, drafting, theme-based formatting, cover generation, content validation, and optional draft publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onegrown](https://clawhub.ai/user/onegrown) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and developers use this skill to generate WeChat Official Account article drafts, apply reusable themes, create covers, validate factual claims, and prepare drafts for publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle WeChat Official Account drafts and credentials. <br>
Mitigation: Use a dedicated low-privilege WeChat app credential, keep AppSecret out of prompts and commits, and review before any draft push, update, or delete. <br>
Risk: Security evidence flags under-disclosed draft deletion, broad host inspection, and cleanup/Git helper scripts. <br>
Mitigation: Review the affected behavior before installation and avoid cleanup or upload helper scripts unless the exact paths and effects have been verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onegrown/tsmf-wechat-oa) <br>
- [Skill overview](references/SKILL_OVERVIEW.md) <br>
- [Workflow design](references/WORKFLOW_DESIGN.md) <br>
- [Themes guide](references/THEMES_GUIDE.md) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>
- [WeChat draft API](https://api.weixin.qq.com/cgi-bin/draft/add) <br>
- [html2canvas](https://html2canvas.hertzen.com/) <br>
- [FileSaver.js](https://github.com/eligrey/FileSaver.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated article artifacts may include Markdown, HTML, JSON, and cover files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally interact with WeChat Official Account credentials and external validation/search services when configured.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
