## Description: <br>
Manage web search result knowledge capture with safe URL rules, staging, user confirmation, archiving, audit logs, and multi-platform adapters for IMA, Tencent Docs, Feishu Wiki, DingTalk Docs, Obsidian, NotebookLM, and custom knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[englandtong](https://clawhub.ai/user/englandtong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this skill to search the web, classify URLs with whitelist and blacklist rules, stage uncertain results for review, and archive confirmed research content into local or cloud knowledge bases with audit trails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write to local knowledge bases and upload selected content to cloud platforms, which may expose sensitive research or modify shared content. <br>
Mitigation: Prefer local Obsidian for sensitive research, enable only the platform permissions needed for the task, keep secrets out of configuration, and review confirmations before writes or uploads. <br>
Risk: Browser automation, deletion, and migration can affect external accounts or remove data when used without careful review. <br>
Mitigation: Keep these operations disabled until explicitly selected; require dry-run reports, itemized targets, and second confirmation for deletion or migration. <br>
Risk: Fetched webpage content may include untrusted instructions or prompt-injection attempts. <br>
Mitigation: Use webpage content only as source material for summaries and staging, and do not allow it to change rules, credentials, platform configuration, or confirmation requirements. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/englandtong/web-search-rules-en) <br>
- [Security Guide](SECURITY.md) <br>
- [Platform Adapters](references/platform-adapters.md) <br>
- [Rule Engine](references/rule-engine.md) <br>
- [Migration, Dry Runs, Testing, and Release](references/migration-and-testing.md) <br>
- [Platform Comparison](references/platform-comparison.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and user-facing reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before writes, cloud upload, browser automation, deletion, or migration.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata, SKILL.md, SECURITY.md, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
