## Description: <br>
WeChat Official Account Writer turns topics, source material, links, or AI news into WeChat Official Account drafts with optional images, WeChat-safe HTML, upload JSON, validation, and draft-box creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ymz2012](https://clawhub.ai/user/ymz2012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, technical bloggers, AI-news writers, product teams, content operators, and Codex users use this skill to draft, polish, illustrate, validate, and prepare WeChat Official Account articles. When configured with WeChat credentials, it can generate upload JSON and create draft-box entries for human review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured WeChat credentials and DRY_RUN=0 can allow the workflow to create real draft-box entries. <br>
Mitigation: Keep DRY_RUN=1 during setup and testing, review generated JSON and images, and disable dry-run only when draft creation is intended. <br>
Risk: The local .env file can contain sensitive WeChat AppID and AppSecret values. <br>
Mitigation: Protect the .env file, keep it out of published packages, and do not paste real credentials into prompts, logs, or documentation. <br>
Risk: Generated articles or images can contain unsupported claims, sensitive wording, or layout problems before upload. <br>
Mitigation: Review titles, claims, source handling, images, and WeChat-safe HTML before creating draft-box entries. <br>


## Reference(s): <br>
- [Article Patterns](references/article-patterns.md) <br>
- [Image and Draft Upload Integration](references/image-and-draft-upload.md) <br>
- [Output Checklist](references/output-checklist.md) <br>
- [WeChat Article Workbench README](scripts/wechat-article-workbench/README.md) <br>
- [WeChat Article Workbench Automation](scripts/wechat-article-workbench/AUTOMATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, JSON, HTML, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional WeChat-safe HTML, generated article JSON, local file paths, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare local image and article files and create WeChat draft-box entries when credentials are configured; dry-run validation is recommended before upload.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
