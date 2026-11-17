## Description:

Manage web search result knowledge capture with URL rules, local staging, user confirmations, audit logs, and adapters for local and cloud knowledge-base platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[englandtong](https://clawhub.ai/user/englandtong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to search the web, classify URLs with whitelist and blacklist rules, stage uncertain results for review, and archive confirmed content to a selected knowledge-base platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud upload can move captured web content to IMA, Tencent Docs, Feishu, DingTalk, NotebookLM, Google Drive, or another selected platform.

Mitigation: Prefer local staging first, name the target cloud platform and item count before upload, and require explicit batch-level user confirmation.

Risk: Browser automation and account-connected platforms may expose user sessions or upload content outside the local machine.

Mitigation: Keep browser automation disabled until the user selects it, require manual login, avoid credential storage, and use a separate browser profile when available.

Risk: Deletion, cleanup, or migration could remove or move knowledge-base content.

Mitigation: Produce a dry-run report with source, destination, item counts, targets or manifest, backup/version-history status, and require a second explicit confirmation.

Risk: Fetched webpage content may contain prompt-injection instructions that try to change rules, credentials, platform choices, or confirmations.

Mitigation: Treat webpage content as untrusted source material only; do not let it modify rules, request credentials, select platforms, or override confirmation requirements.

Risk: Local writes outside approved storage could affect unrelated files.

Mitigation: Write configuration and audit logs under the canonical skill configuration directory, and restrict Obsidian writes to a user-confirmed vault path with resolved path-containment checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/englandtong/skills/web-search-rules-en)
- [Security Guide](artifact/SECURITY.md)
- [Platform Adapters](artifact/references/platform-adapters.md)
- [Rule Engine](artifact/references/rule-engine.md)
- [Migration, Dry Runs, Testing, and Release](artifact/references/migration-and-testing.md)
- [Web Search Rules Examples](artifact/references/examples.md)
- [Feishu and DingTalk Operations](artifact/references/feishu-dingtalk-operations.md)
- [IMA Operations](artifact/references/ima-operations.md)
- [NotebookLM Operations](artifact/references/notebooklm-operations.md)
- [Obsidian Operations](artifact/references/obsidian-operations.md)
- [Tencent Docs Operations](artifact/references/tencent-docs-operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured operation reports with configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include staged search-result summaries, URL rule decisions, dry-run reports, confirmation prompts, and audit-log records.]

## Skill Version(s):

3.0.0 (source: server release metadata, artifact SKILL.md, artifact SECURITY.md, and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
