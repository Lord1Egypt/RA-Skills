## Description: <br>
Formats Markdown articles into WeChat public-account-compatible inline HTML with theme previews, content-structure enhancements, code highlighting, copy-to-WeChat support, and optional draft publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[love254443233](https://clawhub.ai/user/love254443233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and agent workflows use this skill to convert Markdown drafts into polished WeChat public-account articles, preview and choose among themes, copy the rendered HTML, or optionally publish to a WeChat draft box. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formatted content may be copied or published before final editorial review. <br>
Mitigation: Review the generated preview and use dry-run behavior before publishing. <br>
Risk: WeChat credentials could authorize publishing to the wrong account if configured broadly or incorrectly. <br>
Mitigation: Keep WeChat credentials limited to the intended account and verify the target before draft upload. <br>
Risk: Untrusted articles may contain remote or private-network image URLs that are fetched during publishing. <br>
Mitigation: Avoid publishing untrusted articles with remote or private-network image URLs, and inspect image references before upload. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/love254443233/wechat-typeset-pro) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated HTML files, browser preview pages, and optional WeChat draft API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces theme-specific WeChat-compatible inline HTML and local preview/gallery files; optional publishing requires WeChat credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
