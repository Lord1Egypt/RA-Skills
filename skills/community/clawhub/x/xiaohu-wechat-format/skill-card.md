## Description: <br>
Format Markdown or rough notes into WeChat Official Account compatible inline-style HTML, preview 33 themes, upload images, generate optional covers, and push articles to WeChat draft box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingmafuture](https://clawhub.ai/user/lingmafuture) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and publishing teams use this skill to prepare Markdown or rough notes for WeChat Official Account publishing, preview themed HTML, handle images, generate optional covers, and create WeChat draft-box entries when explicitly confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires WeChat publishing credentials and may also use AI API credentials. <br>
Mitigation: Keep config files private, never expose app secrets or API keys in agent output, and install only when those credentials may be used by the workflow. <br>
Risk: Draft publishing, permanent media upload, and comment auto-reply can write to external WeChat services. <br>
Mitigation: Require explicit user confirmation for external writes, run comment auto-reply with --dry-run first, and confirm each batch before sending. <br>
Risk: File and content mutation paths can alter article files, generated covers, logs, state files, and output directories. <br>
Mitigation: Review generated article, cover, and comment output before publishing, and use narrow image search paths instead of broad home or vault roots. <br>
Risk: Imported WeChat images may be mislabeled and rejected by WeChat upload APIs. <br>
Mitigation: Detect image type from bytes, convert WebP or unsupported images to JPEG with Pillow, and verify one theme uploads successfully before bulk publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lingmafuture/xiaohu-wechat-format) <br>
- [Publisher profile](https://clawhub.ai/user/lingmafuture) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration instructions, and generated HTML/image publishing outputs from the bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local preview files, formatted article files, image assets, cover prompts, logs, and WeChat draft or comment updates when the user confirms external actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
