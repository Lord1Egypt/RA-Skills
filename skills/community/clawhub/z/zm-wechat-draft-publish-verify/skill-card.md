## Description: <br>
ZM 公众号草稿发布与核验。用于将已准备好的 Markdown/HTML 公众号稿通过 zm-md2wechat-conversion-tool 推送到公众号草稿箱，并强制执行 draft/get 真实落库与排版核验。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create WeChat Official Account drafts from prepared Markdown or HTML, upload the cover image, and verify the resulting draft through WeChat draft/get before reporting success. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends article content and cover images to WeChat while creating drafts. <br>
Mitigation: Use it only when draft creation is intended, review article and image paths before execution, and use a dedicated WeChat AppID/AppSecret. <br>
Risk: A successful local conversion, preview, or media_id receipt can be mistaken for a completed draft. <br>
Mitigation: Require draft/get verification and treat missing or failed verification as submitted-but-unverified or blocked. <br>
Risk: Incorrect credentials or an unapproved public IP can block WeChat API access. <br>
Mitigation: Validate the md2wechat configuration and confirm the current public IP is on the WeChat Official Account allowlist before running the draft workflow. <br>


## Reference(s): <br>
- [Skill homepage](https://github.com/geekjourneyx/zm-md2wechat-conversion-tool-skill) <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-wechat-draft-publish-verify) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Themes and layout notes](references/themes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON verification artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates draft, upload, conversion, and draft/get verification JSON files next to the source article.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
