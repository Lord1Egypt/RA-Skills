## Description:

ZM 公众号草稿发布与核验。用于将已准备好的 Markdown/HTML 公众号稿通过 zm-md2wechat-conversion-tool 推送到公众号草稿箱，并强制执行 draft/get 真实落库与排版核验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to push prepared WeChat Official Account Markdown or HTML articles into the draft box, upload cover media, and verify the created draft through draft/get before reporting success.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload article content, cover images, authentication-derived access, and draft metadata to WeChat.

Mitigation: Run it only for the intended WeChat Official Account, review article and image paths first, and confirm the configured credentials belong to that account.

Risk: A command can return a submission receipt without proving the draft exists in the backend.

Mitigation: Require the draft/get verification artifact to pass before reporting draft publishing success.

Risk: The release evidence notes a naming mismatch between md2wechat and zm-md2wechat-conversion-tool command references.

Mitigation: Confirm the installed CLI name and update commands or PATH before depending on automated publish steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jerryxn/skills/zm-wechat-draft-publish-verify)
- [Troubleshooting](references/troubleshooting.md)
- [Themes and Layout Notes](references/themes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON verification artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft creation and verification artifacts next to the source article when the publishing script is run.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
