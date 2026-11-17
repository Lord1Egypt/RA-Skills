## Description:

Builds a related-works report from paper markdown files by extracting related-works sections, resolving and deduplicating cited papers, retrieving arXiv abstracts through Tavily and local helpers, and assembling the results in a user-specified work folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[red0orange](https://clawhub.ai/user/red0orange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use this skill to turn one or more paper markdown files into an auditable related-works survey with extracted citations, deduplicated papers, retrieved abstracts, and a final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local command, file, web, MCP, and subagent authority while processing paper markdowns.

Mitigation: Install it only in contexts where that authority is acceptable, and run it with a dedicated WORKDIR outside synced, version-controlled, or confidential locations.

Risk: Paper titles and related intermediate data may be sent through Tavily/arXiv lookup and retained locally in the work folder.

Mitigation: Avoid unpublished or sensitive manuscripts unless that lookup and local retention are acceptable; review and clean the work folder before sharing or syncing it.

Risk: A generated related-works report may contain missed, failed, or incorrect paper matches.

Mitigation: Review the deduplicated paper list and retrieved abstracts before using the report; keep lookup failures explicit rather than replacing them with guessed matches.

## Reference(s):

- [Related Works Report Examples](artifact/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/red0orange/skills/related-works-report-from-paper-mds)
- [arXiv](https://arxiv.org/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports and JSONL batch records with inline shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes final_related_works_report.md and intermediate artifacts under the user-specified WORKDIR; records Tavily/arXiv lookup failures instead of fabricating matches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
