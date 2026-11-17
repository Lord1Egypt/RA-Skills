## Description:

This skill helps Xiaohongshu creators and operators fetch and analyze top 7-day viral notes across 25 content categories, with optional HTML reporting and daily subscription prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand marketers, MCN operators, and growth analysts use this skill to monitor Xiaohongshu 7-day viral-note rankings, compare content patterns, generate Markdown analysis, and optionally produce shareable HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a RedFox API key.

Mitigation: Set REDFOX_API_KEY only in the current session or a proper secret store, and do not print, hard-code, or log the full key.

Risk: The skill contacts redfox.hk to fetch Xiaohongshu ranking data.

Mitigation: Install and run it only in environments where outbound access to redfox.hk is expected and permitted.

Risk: Fetched API responses and generated HTML reports are written locally.

Mitigation: Review and delete .cache data and generated reports when they are no longer needed.

Risk: Generated HTML reports may include untrusted API data and remote script dependencies.

Mitigation: Avoid opening generated HTML from untrusted or unreviewed data until the escaping and remote-script issues are fixed.

Risk: Daily subscription behavior may create persistent automation.

Mitigation: Confirm how to cancel or disable the daily subscription before enabling it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/if530770/skills/xhs-weekly-ranking)
- [Core Workflow](references/core_workflow.md)
- [RedFoxHub API Keys](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, HTML files, guidance]

**Output Format:** [Markdown tables and analysis, shell commands, configuration guidance, and optional standalone HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and network access to redfox.hk; fetched API data is cached locally for report generation.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
