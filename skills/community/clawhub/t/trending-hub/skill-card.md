## Description:

Aggregates hourly hot-search rankings from Douyin, Weibo, Bilibili, Kuaishou, Zhihu, Toutiao, and Baidu for cross-platform trend monitoring, filtering, reporting, and scheduled summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, market operators, media editors, PR teams, and data analysts use this skill to scan multi-platform hot-search rankings, filter by platform or keyword, compare trends, and generate concise reports or scheduled push summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key exposure or misuse because the skill requires REDFOX_API_KEY and the security evidence reports insecure key handling.

Mitigation: Use only a narrowly scoped, revocable RedFox API key; do not store it in prompts, code, logs, or generated output; rotate or revoke it after testing.

Risk: Network request integrity risk because the security evidence calls for fixing TLS verification.

Mitigation: Do not deploy until TLS certificate and hostname verification are restored and verified in the fetch helper.

Risk: Local file safety risk because the security evidence calls out unsafe temporary-file creation.

Mitigation: Replace unsafe temporary-file creation with a secure named temporary file or controlled output path before use.

Risk: Unexpected recurring notifications because the skill advertises scheduled push behavior without enough controls.

Mitigation: Require explicit subscription confirmation, document cancellation, and keep notification scope and schedule visible to the user.

Risk: Execution reliability risk because the security guidance says the release has a syntax error and an unnecessary unpinned dependency.

Mitigation: Repair the syntax error, remove or pin unnecessary dependencies, and run a clean execution check before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/trending-hub)
- [README.en.md](artifact/README.en.md)
- [README.md](artifact/README.md)
- [Instruction List](artifact/references/instruction-list.md)
- [Output Templates](artifact/references/output-templates.md)
- [Prediction Logic](artifact/references/prediction-logic.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, compact text summaries, and JSON data files produced by a Python command-line helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; supports platform filters, keyword filters, date ranges, compact output, JSON output, and Markdown output.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
