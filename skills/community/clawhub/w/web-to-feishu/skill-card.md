## Description: <br>
Converts web links and local files into structured Markdown, then can save the result to Feishu cloud documents or Tencent ima notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn URLs, social posts, articles, YouTube pages, and local documents into Markdown, with optional publication to Feishu or Tencent ima. It is useful for collecting, normalizing, and saving research or reference material in a document workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected converted content may be sent to Feishu or Tencent ima when those save options are used. <br>
Mitigation: Use the save integrations only for content approved for those services, and confirm destination workspace policies before upload. <br>
Risk: Feishu and Tencent ima credentials can grant access to document or note workspaces. <br>
Mitigation: Use least-privilege API credentials, keep them in environment variables or a secret manager, and rotate them if exposed. <br>
Risk: Twitter conversion depends on an external x-tweet-fetcher helper that is not part of this artifact. <br>
Mitigation: Review and scan the x-tweet-fetcher helper separately before relying on Twitter or X import workflows. <br>
Risk: Unpinned Python dependencies may change behavior over time. <br>
Mitigation: Pin dependency versions and test conversion workflows before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardwason/web-to-feishu) <br>
- [Feishu Setup Guide](references/feishu-setup.md) <br>
- [Tencent ima Setup Guide](references/ima-setup.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Tencent ima Agent Interface](https://ima.qq.com/agent-interface) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents or Markdown text with optional Feishu or Tencent ima document links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided URLs or local file paths; Feishu and Tencent ima saving require API credentials configured in environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
