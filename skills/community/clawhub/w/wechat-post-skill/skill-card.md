## Description: <br>
User-authorized WeChat Official Account workflow for topic selection, drafting, editing, image planning, pre-publish review, and handoff to a configured WeChat publishing tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiao1yin2he3](https://clawhub.ai/user/jiao1yin2he3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to plan, draft, review, and hand off Chinese WeChat Official Account articles to a user-authorized publisher. It supports draft-box workflows where account access and publishing credentials remain under the user's control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can be misused against a WeChat Official Account the user is not authorized to operate. <br>
Mitigation: Use only for accounts the user owns or is authorized to operate, and require explicit user direction before creating or updating drafts. <br>
Risk: WeChat credentials such as WECHAT_APP_SECRET, tokens, cookies, or private account configuration could be exposed in chat, article files, logs, or commits. <br>
Mitigation: Configure credentials outside chat through environment variables or private user-controlled configuration, and do not store, print, commit, or publish secret values. <br>
Risk: A companion publishing tool may create or publish drafts with permissions beyond this documentation-only skill. <br>
Mitigation: Review and trust the companion publisher separately before use, confirm required configuration is present without printing values, and default to WeChat draft-box handoff unless the user explicitly asks otherwise. <br>
Risk: Publishing can fail because of invalid credentials, account permissions, or WeChat IP allowlist settings. <br>
Mitigation: Stop on those failures and ask the user to fix WeChat account settings; do not bypass platform controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiao1yin2he3/wechat-post-skill) <br>
- [Project Homepage](https://github.com/jiao1yin2he3/wechat-post-skill) <br>
- [Content Playbook](references/content-playbook.md) <br>
- [Publishing Notes](references/publishing-notes.md) <br>
- [baoyu-post-to-wechat](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat) <br>
- [gemini-browser-image-skill](https://github.com/jiao1yin2he3/gemini-browser-image-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown articles, image placeholders, review notes, and handoff commands or checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create an article folder with article.md, cover.png, and body image assets when authorized by the user.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
