## Description:

Web Search Rules helps agents verify web research, attach source-level evidence to claims, and stage approved findings for knowledge-base intake.

This skill is ready for commercial/non-commercial use.

## Publisher:

[englandtong](https://clawhub.ai/user/englandtong)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and knowledge workers use this skill to search current web sources, verify claim support, deduplicate results, and stage or archive research records into local or cloud knowledge bases after required review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webpage text, search snippets, and file metadata may contain prompt-injection content or unsupported claims.

Mitigation: Treat source content and metadata as untrusted, open sources before use, and record claim-level evidence states before staging or archiving.

Risk: Knowledge-base writes or cloud uploads may persist sensitive or unapproved research.

Mitigation: Keep staging separate from archive targets, require explicit confirmation for archive or cloud upload, and prefer the local Obsidian path for sensitive research.

Risk: Deletion or migration can move or remove records unintentionally.

Mitigation: Require an itemized dry run, a copy-first migration plan, and a second confirmation before destructive or cross-platform operations.

## Reference(s):

- [Quickstart](QUICKSTART.md)
- [Rule Engine And Evidence Model](references/rule-engine.md)
- [Platform Adapters](references/platform-adapters.md)
- [Platform Comparison](references/platform-comparison.md)
- [Obsidian Operations](references/obsidian-operations.md)
- [Feishu Wiki and DingTalk Docs Operations](references/feishu-dingtalk-operations.md)
- [Tencent Docs Operations](references/tencent-docs-operations.md)
- [IMA Operations](references/ima-operations.md)
- [NotebookLM Operations](references/notebooklm-operations.md)
- [Migration, Dry Runs, Testing, And Release](references/migration-and-testing.md)
- [Web Search Rules Examples](references/examples.md)
- [Chinese Platform Operation Guide](references/platform-operation-guide-zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports with structured source-record fields and optional JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires opened-source evidence for supported claims; persistence, cloud upload, browser automation, deletion, and migration require confirmation.]

## Skill Version(s):

4.1.0 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
