## Description:

Scrape WDFW Puget Sound creel data into salmon CPUE reports: daily digest, weekly top-launch email with chart, and proactive hot-bite alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvin-tsai](https://clawhub.ai/user/calvin-tsai)

### License/Terms of Use:

MIT-0

## Use Case:

External anglers, guides, and developers use this skill to monitor Puget Sound salmon catch and effort trends, produce daily or weekly CPUE reports, and trigger optional hot-bite alerts.

### Deployment Geography for Use:

Global, with a Puget Sound, Washington data focus.

## Known Risks and Mitigations:

Risk: Optional email mode can use stored mail-provider credentials and dynamic mailing-list sources.

Mitigation: Use dedicated low-privilege mail credentials, control subscriber and unsubscribe sources, and review recipients with dry-run or test sends before scheduling real delivery.

Risk: Scheduled unattended email can send reports before subscriber sources and unsubscribe handling are under the operator's control.

Mitigation: Do not schedule unattended email until list ownership, daily caps, and unsubscribe processing are confirmed.

Risk: WDFW same-day data may be partial and the source page can change because the skill scrapes server-rendered HTML.

Mitigation: Review generated reports against current WDFW data and regulations before relying on them for fishing decisions.

## Reference(s):

- [WDFW Puget Sound Creel Reports](https://wdfw.wa.gov/fishing/reports/creel/puget)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown reports, HTML email content, PNG chart output, JSON state files, and plain-text alert messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional chart output requires matplotlib; optional email delivery uses user-provided mail-provider credentials and subscriber sources.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
