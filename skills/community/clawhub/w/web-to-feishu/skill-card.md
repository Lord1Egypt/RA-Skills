## Description:

Web To Feishu converts webpages or local files into structured Markdown and can save the result to Feishu Cloud Docs or Tencent ima notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn URLs or local files into Markdown, then optionally publish the result to Feishu Cloud Docs or Tencent ima notes. It is suited for document capture workflows involving web pages, X/Twitter posts, WeChat articles, YouTube videos, and common local file formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill asks users to run unpinned external code.

Mitigation: Pin or vendor the x-tweet-fetcher dependency before using Twitter/X conversion.

Risk: The security review says the skill asks for broader cloud permissions than the implementation appears to need.

Mitigation: Use a dedicated Feishu or ima app or API key with minimal permissions, and remove unnecessary Feishu folder access unless it is required.

Risk: Converted local files may be uploaded to external document services when save-to-cloud steps are used.

Mitigation: Avoid converting sensitive local files unless upload is intended, and review generated Markdown before saving it to Feishu or ima.

## Reference(s):

- [Feishu Cloud Docs API setup guide](references/feishu-setup.md)
- [Tencent ima notes API setup guide](references/ima-setup.md)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Tencent ima Agent Interface](https://ima.qq.com/agent-interface)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown files locally and may create remote Feishu documents or Tencent ima notes when credentials are configured.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
