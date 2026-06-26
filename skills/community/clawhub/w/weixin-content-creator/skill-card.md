## Description: <br>
Helps self-media creators track trending topics, customize writing profiles, draft and review platform-specific content, fact-check key claims, and sync drafts to Tencent Docs or WeChat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Suzanneyp](https://clawhub.ai/user/Suzanneyp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and media operators use this skill to turn a topic or trend into drafts for WeChat, Xiaohongshu, or Zhihu. It supports writing-profile selection, article generation, quality review, fact-check prompts, and optional draft publishing or backup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing and sync workflows can create Tencent Docs documents or WeChat public-account drafts through connected accounts without a clear final approval gate. <br>
Mitigation: Require the agent to preview the exact title, content, destination account, and service action, then wait for explicit approval before sync or publishing. <br>
Risk: Optional external MCP helpers and connected third-party services may receive draft content or perform account actions. <br>
Mitigation: Review the external MCP helper before installation and avoid sending confidential or regulated content to connected services unless that transfer is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Suzanneyp/weixin-content-creator) <br>
- [Publisher profile](https://clawhub.ai/user/Suzanneyp) <br>
- [Tencent Docs MCP setup](https://docs.qq.com/desktop/wikispace?tab=1) <br>
- [WeChat access token API](https://api.weixin.qq.com/cgi-bin/token) <br>
- [WeChat material upload API](https://api.weixin.qq.com/cgi-bin/material/add_material) <br>
- [WeChat draft creation API](https://api.weixin.qq.com/cgi-bin/draft/add) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/text article drafts, review reports, fact-check reports, configuration snippets, API payload examples, and optional publishing status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Tencent Docs documents or WeChat public-account drafts through configured connected accounts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
