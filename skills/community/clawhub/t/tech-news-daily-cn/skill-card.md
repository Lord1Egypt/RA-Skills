## Description:

Generates a daily Chinese technology news report by searching recent technology and AI news, deduplicating and scoring items, saving a Markdown report locally, and publishing the report to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuatochina](https://clawhub.ai/user/binhuatochina)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, operators, and knowledge workers use this skill to compile recent technology and AI news into a ranked Chinese daily report with source links, relevance ratings, and recommendation scores. The report can be stored as a local Markdown file, copied into a Feishu document, and sent to a Feishu group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the full generated report to a fixed Feishu group and uses fixed Feishu knowledge-base identifiers.

Mitigation: Install only when those Feishu destinations are intentionally yours, or modify the skill to ask for and confirm destinations before writing or sending.

Risk: The skill can create local files and create or write Feishu documents.

Mitigation: Review destination settings, generated content, and source links before allowing the skill to publish or persist reports.

## Reference(s):

- [Feishu document operation reference](artifact/references/feishu-doc.md)
- [ClawHub skill release page](https://clawhub.ai/binhuatochina/skills/tech-news-daily-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, API Calls, Configuration]

**Output Format:** [Markdown report with source links, scoring metadata, Feishu document content, Feishu message text, and checkpoint JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates dated local report files under memory/, writes progress checkpoint JSON, and uses Feishu-specific document and message destinations.]

## Skill Version(s):

0.2.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
