## Description: <br>
Collect recent high-interaction Xiaohongshu/Rednote public notes and cleaned comments using demand-style keywords for small-scale user need discovery and downstream analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zev55555](https://clawhub.ai/user/zev55555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product researchers, and product teams use this skill to collect small batches of recent Xiaohongshu/Rednote notes and comments around demand-oriented keywords, then prepare cleaned structured data for later LLM or product analysis. It is suited to research, internal product validation, competitive review, and content opportunity exploration where a logged-in Xiaohongshu session is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a logged-in Xiaohongshu session and the package also exposes commands for commenting, liking, collecting, and publishing. <br>
Mitigation: Prefer read-only demand-discovery, search, and feed commands; use account-interaction or publishing commands only when the user explicitly intends to mutate the account. <br>
Risk: Collected datasets may contain public content and hashed author identifiers that should be reviewed before reuse or sharing. <br>
Mitigation: Review generated files before sharing, keep batch sizes conservative, and delete local cookies or output files when the collection task is finished. <br>
Risk: Xiaohongshu login, captcha, rate limits, and platform risk controls can interrupt collection. <br>
Mitigation: Do not bypass platform controls; stop on captcha or expired login and ask the user to handle verification or QR-code login manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zev55555/xiaohongshu-demand-discovery-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zev55555) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal JSON plus JSONL, JSON, and Markdown files such as notes_clean.jsonl, comments_clean.jsonl, collection_summary.json, and collector_report.md.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs through Python and Playwright, uses a logged-in Xiaohongshu browser session, and writes timestamped local collection outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
