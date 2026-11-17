## Description:

Renders finalized text, Markdown, or prepared HTML into WeChat-compatible rich text and can publish it to a WeChat Official Account draft box with themes, previews, cover generation, and preflight checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouq2039-lang](https://clawhub.ai/user/zhouq2039-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, editors, and developers use this skill to turn finalized Markdown, text, or prepared HTML into WeChat Official Account drafts while previewing layout, managing themes, generating covers, and checking WeChat rich-text compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat Official Account credentials and can create drafts and upload media.

Mitigation: Install only when credential access and draft creation are acceptable; keep credentials outside the skill directory and use the documented --config or WECHAT_PUSH_CONFIG paths.

Risk: Override options such as --force and --no-validate can bypass normal preflight checks.

Mitigation: Avoid these options for routine publishing and review generated content before creating or publishing drafts.

Risk: The --build path loads a named Python module for advanced article rendering.

Mitigation: Use --build only with trusted modules from reviewed local source.

Risk: Generated previews that include remote images may cause browser network requests.

Mitigation: Prefer trusted local images for sensitive previews and review remote image sources before opening generated preview files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouq2039-lang/skills/wechat-native-publisher)
- [WeChat rich-text whitelist](references/wechat-whitelist.md)
- [WeChat rich-text reference article](https://mp.weixin.qq.com/s/qLWS4clCcMtciwAmL7JAfw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples; scripts can generate HTML previews, cover images, profile JSON, and WeChat draft uploads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal push mode uses WeChat account credentials and API calls; preview mode is documented as local-only when --no-push is used.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
