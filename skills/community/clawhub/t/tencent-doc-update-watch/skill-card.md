## Description:

Privacy-first re-crawl and diff workflow for Tencent Docs (docs.qq.com) update checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasilva](https://clawhub.ai/user/chinasilva)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to re-crawl Tencent Docs links, compare current metadata against previous snapshots, and produce update reports for monitored documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured URLs can cause the script to fetch unintended or untrusted locations.

Mitigation: Review the docs configuration before execution and restrict monitored URLs to expected https://docs.qq.com links.

Risk: Raw debug mode can retain fetched pages, headers, cookies, and related snapshot metadata.

Mitigation: Keep --keep-raw disabled except during debugging, use a disposable workspace, and avoid sensitive authenticated Tencent Docs links.

Risk: The skill writes local snapshots that may reveal document names, IDs, update timing, or comparison metadata.

Mitigation: Store snapshots in an access-controlled workspace and delete them when monitoring data is no longer needed.

## Reference(s):

- [Default Tencent Docs watch configuration](references/default-docs.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated runs produce manifest.json and report.md files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot reports include status values such as UNCHANGED, CHANGED, NEW, and FIRST_RUN.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
