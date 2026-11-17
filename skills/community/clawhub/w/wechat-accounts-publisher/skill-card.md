## Description:

Automates WeChat Official Account draft creation through the WeChat API, including credential-based account access and upload or replacement of cover and in-article images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlr25](https://clawhub.ai/user/zlr25)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to configure an agent to create WeChat Official Account article drafts, upload local cover and body images, and prepare posts for later review or publishing in the WeChat backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat AppID, AppSecret, and cached access tokens.

Mitigation: Review and control config.json before use, protect config.json and .tokens with owner-only permissions, and avoid committing credentials or token caches.

Risk: The configured API base URL affects where credentials and token-bearing requests are sent.

Mitigation: Keep apiBaseUrl fixed to https://api.weixin.qq.com unless an authorized reviewer approves a different endpoint.

Risk: Local cover and body images may be uploaded to the WeChat material library.

Mitigation: Check the selected thumb file, content directory, and HTML image paths before draft creation, especially for scheduled or batch workflows.

Risk: Scheduled workflows can repeatedly create drafts or upload media without a final human prompt.

Mitigation: Review scheduled triggers before enabling them and require account-owner review of generated drafts in the WeChat backend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlr25/skills/wechat-accounts-publisher)
- [Publisher profile](https://clawhub.ai/user/zlr25)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [Artifact setup and usage guide](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python or Node.js code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create WeChat drafts and upload local image files through the provided scripts after user-controlled configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
