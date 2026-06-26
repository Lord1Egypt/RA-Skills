## Description: <br>
Generates WeChat Official Account article drafts from a user-provided topic, with planned search, AI summarization, formatting, and draft-saving workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onWalking](https://clawhub.ai/user/onWalking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to draft WeChat Official Account articles from a topic and prepare formatted article previews or draft-save workflows for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive WeChat Official Account credentials. <br>
Mitigation: Keep WECHAT_SECRET out of source control and logs, use environment variables or a protected runtime secret store, and install only when connecting a WeChat Official Account is intended. <br>
Risk: The current CLI can report successful article generation without actually generating content or saving a WeChat draft. <br>
Mitigation: Verify draft creation manually in WeChat and prefer a preview or confirmation step before treating any run as successful. <br>
Risk: Generated content may violate WeChat content rules or include inaccurate claims. <br>
Mitigation: Review generated drafts manually for policy compliance, accuracy, formatting, and suitability before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onWalking/wechat-article-creator) <br>
- [Publisher profile](https://clawhub.ai/user/onWalking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and Markdown article preview with configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and WeChat Official Account credentials supplied through WECHAT_APPID and WECHAT_SECRET.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
