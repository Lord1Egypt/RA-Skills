## Description:

Generates illustrated Simplified-Chinese shop-operation reports for mainland-China Taobao and Tmall merchants from their connected SYCM store data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzbarry1980-bot](https://clawhub.ai/user/gzbarry1980-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Taobao and Tmall merchants in mainland China use their own connected SYCM account to prepare daily, weekly, or monthly shop-performance reports with charts, comparisons, and actionable recommendations. The user must specify the shop and reporting period.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Generating a report can overwrite PNG charts or a DOCX report with the same name.

Mitigation: Use a dedicated output directory or date-specific filenames for each report.

Risk: Optional scheduled jobs can repeatedly access store metrics and write report files.

Mitigation: Enable scheduled reporting only when recurring access is intended, and review the configured destination and schedule.

Risk: Example JSON contains synthetic values that do not represent a real store.

Mitigation: Fetch the merchant's current SYCM data and verify comparisons before generating a real report.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/gzbarry1980-bot/skills/sycm-shop-report)
- [SYCM data contract](artifact/references/data_contract.md)
- [Environment setup](artifact/references/environment.md)
- [Scheduled report setup](artifact/references/cron_setup.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Files]

**Output Format:** [Simplified-Chinese summary and illustrated DOCX report with PNG charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the merchant's connected SYCM data; daily and weekly reports have included scripts, while monthly reports adapt the weekly template.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
