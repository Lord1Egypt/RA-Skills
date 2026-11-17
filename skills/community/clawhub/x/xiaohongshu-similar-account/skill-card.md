## Description:

Finds comparable Xiaohongshu accounts from an account ID or from niche, follower, and account-level criteria, then returns same-level benchmarks, higher-level reference accounts, analysis, subscription options, and an HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content operations teams, MCN agencies, and brand marketers use this skill to identify comparable Xiaohongshu accounts for account growth, creator benchmarking, and KOL screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends Xiaohongshu account IDs or targeting criteria to redfox.hk.

Mitigation: Use a scoped, revocable API key, avoid sharing sensitive account criteria, and review RedFoxHub terms before installation.

Risk: The security evidence reports TLS verification, generated HTML escaping, and subscription consent concerns.

Mitigation: Use only after TLS verification is fixed, generated report content is escaped, and subscription actions are explicit opt-in.

Risk: Generated benchmark reports may not reflect real-time Xiaohongshu data.

Mitigation: Treat recommendations as decision support and verify current account metrics before outreach, spend, or campaign decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/xiaohongshu-similar-account)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox API endpoint](https://redfox.hk/story/api/xhsUser/querySimilarAccounts)
- [Account report template](artifact/references/account_template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown tables and prose with generated JSON and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends account IDs or targeting criteria to redfox.hk; report data may differ from real-time Xiaohongshu data.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
