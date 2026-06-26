## Description: <br>
蚁小二 supports one-click distribution across 50+ platforms, multi-account matrix management, team collaboration, and content analytics for image-text, article, and short-video publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yixiaoer888](https://clawhub.ai/user/yixiaoer888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to publish media content, query connected accounts, upload resources, review publication records, retrieve platform metadata, and inspect account or content performance through the Yixiaoer API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content to connected accounts. <br>
Mitigation: Review every target account, platform, publish channel, and content payload before running a publish action. <br>
Risk: The skill can upload local or remote media files to Yixiaoer storage. <br>
Mitigation: Upload only media files intended for publication and confirm returned resource keys before using them in publishing payloads. <br>
Risk: The YIXIAOER_API_KEY environment variable grants access to publishing and account-management actions. <br>
Mitigation: Treat YIXIAOER_API_KEY as high privilege, keep it out of prompts and logs, and install the skill only when the Yixiaoer service and publisher are trusted. <br>
Risk: The skill can update connected account settings such as proxy configuration. <br>
Mitigation: Run update-account only after confirming the account ID and intended proxy or area setting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yixiaoer888/yixiaoer-publish) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [API helper guide](artifact/docs/scripts/api-guide.md) <br>
- [Platform definitions](artifact/docs/platform.md) <br>
- [Resource upload guide](artifact/docs/upload-resource.md) <br>
- [Video publishing guide](artifact/docs/publish/video/index.md) <br>
- [Proxy management guide](artifact/docs/proxy-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YIXIAOER_API_KEY and action-specific JSON payloads for API calls.] <br>

## Skill Version(s): <br>
1.6.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
