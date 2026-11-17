## Description:

Classifies Chinese standards PDFs by standards level and subject domain, organizes them into folder structures, and produces CSV inventories, offline HTML reports, and filtered ZIP exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffm2020](https://clawhub.ai/user/jeffm2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and records managers use this skill to organize folders of national, industry, local, group, or enterprise standards PDFs into searchable corpora with inventories, reports, and exportable subsets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File organization can move PDFs and may damage or disrupt an original corpus.

Mitigation: Run the classifier with --dry first, work on a backed-up or copied corpus, and review duplicate filenames and target folders before running the moving operation.

Risk: Generated reports or exports may be unsafe or misleading when built from untrusted custom CSV, domain taxonomy, or source registry inputs.

Mitigation: Use trusted registries where possible, avoid untrusted CSV/domain inputs before report generation, and run the consistency verifier before relying on or sharing generated artifacts.

Risk: Optional source discovery can expose lookup terms when web search is used to identify new official standards platforms.

Mitigation: Use web-based discovery only when sharing those lookup terms externally is acceptable; otherwise update sources.json manually from already approved sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffm2020/skills/standards-corpus-classifier)
- [Publisher profile](https://clawhub.ai/user/jeffm2020)
- [Built-in source registry](references/sources.json)
- [General domain taxonomy](references/domains.json)
- [QX domain taxonomy](references/qx_domains.json)
- [National standards platform](https://std.samr.gov.cn/)
- [National standards full-text platform](https://openstd.samr.gov.cn/)
- [Industry standards filing platform](https://hbba.sacinfo.org.cn)
- [Local standards information platform](https://dbba.sacinfo.org.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include CSV, HTML, ZIP archives, and organized PDF folders.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts and JSON registries; supports dry runs, custom source/domain registries, yearly folder views, filtered exports, and consistency verification.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
