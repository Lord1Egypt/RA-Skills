## Description: <br>
Tracks Donald Trump's Truth Social posts by syncing CNN's public archive to a local SQLite database for querying, statistics, and keyword-based market-impact alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to keep a local archive of public Trump Truth Social posts, query post history, review engagement statistics, and surface keyword matches that may warrant attention. Market alerts are simple keyword matches and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync process retains public Truth Social post content in a local SQLite database. <br>
Mitigation: Use the skill only when local retention is intended, review the database path, and delete retained files when they are no longer needed. <br>
Risk: Keyword-based market alerts can be incomplete, noisy, or misleading. <br>
Mitigation: Treat alerts as review prompts only and verify any market-related interpretation against authoritative sources before acting. <br>
Risk: Report output appends alert content to a local Markdown file. <br>
Mitigation: Enable report writing only when persistent reports are desired and periodically review or remove generated report files. <br>


## Reference(s): <br>
- [CNN Truth Social Archive](https://ix.cnn.io/data/truth-social/truth_archive.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/laigen/trump-truth-social-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, SQL queries, Files] <br>
**Output Format:** [Plain text status output, optional JSON, Markdown alert reports, SQL examples, and SQLite database files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local SQLite database under ~/.openclaw/workspace/temp and can append Markdown alerts under ~/.openclaw/workspace/reports when report output is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
