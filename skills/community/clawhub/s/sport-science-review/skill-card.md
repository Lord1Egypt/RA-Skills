## Description:

Automated sports science intelligence engine that fetches sports science sources, filters noise, translates content, and syncs reports to Feishu or Notion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w2478328197-arch](https://clawhub.ai/user/w2478328197-arch)

### License/Terms of Use:


## Use Case:

Sports scientists, coaches, and analysts use this skill to collect recent sports science literature and industry updates, filter and deduplicate items, translate content, and publish a daily report to Feishu or Notion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow fetches public sources, sends content for translation, and creates or sends reports through Feishu and optionally Notion using configured credentials.

Mitigation: Review recipient IDs, app credentials, optional Notion settings, and target language before running.

Risk: The generated report may contain irrelevant, duplicated, or incomplete public-source items despite filtering and deduplication.

Mitigation: Review the report before relying on it and adjust lookback, history, source, and language options when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/w2478328197-arch/skills/sport-science-review)
- [Project homepage](https://github.com/w2478328197-arch/sports-science-daily)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash command examples; runtime output is a dated Markdown report and cloud document links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu credentials for cloud document sync and can optionally use Notion credentials for page sync.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
