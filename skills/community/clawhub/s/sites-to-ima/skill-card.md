## Description:

Sites to IMA helps an agent crawl a specified website's content listings, export indexes, create categorized IMA notes, import selected URLs into an IMA knowledge base, and generate an update manual for later incremental refreshes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IMA users use this skill to turn professional media or blog sites into categorized knowledge-base imports with companion index notes and update records. It is intended for full-site or category-level indexing, not single-article reading or general knowledge-base administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk website crawling and URL imports can collect or ingest content from sites without appropriate permission.

Mitigation: Run the skill only for sites the user is authorized to collect, and review the execution plan before confirming imports.

Risk: Anti-bot bypass guidance and strong-protection workflows can leave failed or residual IMA knowledge-base entries.

Mitigation: Use the documented small-batch validation step for protected sites and avoid protected targets unless authorization and cleanup expectations are clear.

Risk: Unsafe dependency or system-recovery commands could affect the runtime environment if executed automatically.

Mitigation: Review setup commands manually, prefer pinned dependencies or a prebuilt environment, and do not run dpkg lock cleanup automatically.

## Reference(s):

- [Sites to IMA ClawHub listing](https://clawhub.ai/sedey999/skills/sites-to-ima)
- [ima.copilot](https://ima.qq.com)
- [Update manual template](artifact/references/manual-template.md)
- [Note format specification](artifact/references/note-formats.md)
- [Playwright mirror referenced by setup guidance](https://npmmirror.com/mirrors/playwright/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON progress records, xlsx or csv exports, and IMA note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated through the IMA workflow and may include local progress files plus imported knowledge-base URLs.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
