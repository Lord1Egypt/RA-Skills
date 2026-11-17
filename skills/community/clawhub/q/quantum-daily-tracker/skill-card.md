## Description:

Generates Chinese quantum technology paper tracking notes and daily briefings from RSS sources covering quantum computing, quantum networks, quantum error correction, and related fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingquanyao](https://clawhub.ai/user/qingquanyao)

### License/Terms of Use:


## Use Case:

External researchers and developers use this skill to monitor quantum research feeds, identify relevant papers, and maintain Chinese-language paper notes, daily summaries, and dashboard updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled backfill and RSS fetching can create more notes than expected.

Mitigation: Set clear limits for backfill runs and review generated file changes before relying on them.

Risk: Some configured RSS sources use plaintext HTTP endpoints.

Mitigation: Prefer HTTPS feed endpoints where available.

Risk: Generated paper links and summaries may be incomplete or misleading.

Mitigation: Review generated links, paper metadata, and summaries before using them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingquanyao/skills/quantum-daily-tracker)
- [arXiv Quantum Physics RSS](http://export.arxiv.org/rss/quant-ph)
- [npj Quantum Information RSS](https://www.nature.com/npjqi.rss)
- [Science RSS](https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science)
- [PRX Quantum RSS](http://feeds.aps.org/rss/recent/prxquantum.xml)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files and Chinese text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dated paper notes, daily briefings, dashboard updates, and last-run state under quantum-tracker.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
