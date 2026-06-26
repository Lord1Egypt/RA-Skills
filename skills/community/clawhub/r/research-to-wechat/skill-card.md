## Description: <br>
A native research-first pipeline that turns a topic, notes, article, URL, or transcript into a sourced article with an evidence ledger, polished Markdown, inline visuals, cover image, WeChat-ready HTML, browser/API-ready draft assets, and optional multi-platform distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, operators, creators, and agents use this skill to turn topics, notes, source articles, URLs, transcripts, or PDFs into researched WeChat Official Account draft assets. It supports source capture, evidence-led writing, Markdown polishing, WeChat-compatible HTML rendering, image handling, draft saving, and optional multi-platform distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WeChat official-account credentials to upload assets and create or update account drafts. <br>
Mitigation: Use dedicated or least-privilege credentials where possible, review generated article files and images before upload, and require explicit user intent before saving or updating a draft. <br>
Risk: Ambiguous requests such as 'save it' may result in account-side draft changes. <br>
Mitigation: Confirm the target draft action and inspect the manifest, title, digest, cover image, and HTML before invoking draft-save commands. <br>
Risk: The bundled WeChat fetcher may violate platform scraping expectations because it impersonates a WeChat client. <br>
Mitigation: Use the fetcher only when authorized and appropriate, respect platform terms, and prefer user-provided source text or approved source exports when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/research-to-wechat) <br>
- [Skill Genie repository](https://github.com/Fei2-Labs/skill-genie) <br>
- [Execution contract](references/execution-contract.md) <br>
- [Capability map](references/capability-map.md) <br>
- [WeChat compatibility reference](references/wechat-compat.md) <br>
- [Design guide](references/design-guide.md) <br>
- [Platform copy specs](references/platform-copy.md) <br>
- [Author config reference](references/author-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, JSON, Images, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Workspace files containing sourced Markdown, WeChat-ready HTML, a JSON manifest, image assets, and optional draft-delivery commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use WECHAT_APPID and WECHAT_SECRET to upload images and save WeChat drafts; the skill is designed to save drafts, not publish live.] <br>

## Skill Version(s): <br>
0.5.6 (source: server evidence release version and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
