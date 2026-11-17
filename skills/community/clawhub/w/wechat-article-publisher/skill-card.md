## Description:

WeChat Article Publisher extracts articles from Markdown files or webpages, formats them with WeChat style templates, and creates drafts or optionally submits publications to a WeChat Official Account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenglong2015](https://clawhub.ai/user/zhenglong2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to turn reviewed Markdown files or webpage articles into WeChat Official Account drafts, with optional submission for publication and status lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses WeChat Official Account API credentials and can create drafts or optionally submit publications.

Mitigation: Run dry-run first, review the rendered preview and account target, and use publication submission only after human approval.

Risk: API secrets are stored in a local configuration file.

Mitigation: Keep app_secret out of shared repositories, restrict access to the config file, and rotate credentials if exposure is suspected.

Risk: The skill can fetch arbitrary article and image URLs.

Mitigation: Prefer local reviewed Markdown and local cover images; use only trusted URLs when remote extraction is necessary.

Risk: Dependency installation modifies the Python environment used to run the skill.

Mitigation: Install dependencies in an isolated environment before using the publishing workflow.

## Reference(s):

- [WeChat Official Account access token endpoint](https://api.weixin.qq.com/cgi-bin/token)
- [WeChat draft creation endpoint](https://api.weixin.qq.com/cgi-bin/draft/add)
- [WeChat free publish submit endpoint](https://api.weixin.qq.com/cgi-bin/freepublish/submit)
- [WeChat free publish status endpoint](https://api.weixin.qq.com/cgi-bin/freepublish/get)
- [WeChat material upload endpoint](https://api.weixin.qq.com/cgi-bin/material/add_material)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON stdout with an HTML preview file and optional WeChat draft, publication, and status identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode renders a preview without calling WeChat APIs; publishing requires configured WeChat Official Account credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
