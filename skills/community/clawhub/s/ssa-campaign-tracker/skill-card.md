## Description: <br>
Campaign Tracker archives outbound email campaign records, matches customer replies, generates performance reports, and recommends email template optimizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, operations, and developer teams use this skill to maintain a local email campaign analytics loop: archive sent records, match replies, produce weekly or monthly reports, and identify template experiments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local email-system data, including draft, review, and captured inbox files that may contain sensitive customer information. <br>
Mitigation: Set EMAIL_SKILL_ROOT and processed-file paths deliberately, run dry-run mode first, and limit execution to a workspace approved for customer email data. <br>
Risk: The skill persists campaign analytics, reply tracking, logs, reports, and optional Obsidian output locally. <br>
Mitigation: Review generated archives and reports before using metrics, and avoid shared or synced Obsidian vaults for sensitive customer data. <br>
Risk: Template optimization can update A/B testing configuration based on local report data that may be incomplete or low-volume. <br>
Mitigation: Inspect generated recommendations and configuration changes before running optimization live or acting on the proposed experiments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/ssa-campaign-tracker) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Tracking schema](artifact/config/tracking-schema.json) <br>
- [Sample weekly report](artifact/reports/weekly-report-2026-03-24.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON reports, JSONL records, configuration updates, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews and writes local archive, reply-tracking, reports, logs, and optional Obsidian output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
