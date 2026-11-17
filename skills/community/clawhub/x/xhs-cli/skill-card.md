## Description:

Searches and harvests Xiaohongshu content, including topic search results, notes, user profiles, comments, and saved reports through an authenticated agent-browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[excalibursssooo](https://clawhub.ai/user/excalibursssooo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to collect Xiaohongshu search results, note details, comments, and user-profile content into local JSON data and Markdown reports. It is intended for workflows where the operator can provide and manage an authenticated Xiaohongshu browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires live Xiaohongshu login cookies and can persist session-related data.

Mitigation: Use a private data directory, restrict cookie-file permissions, rotate or revoke cookies after use, and avoid installing on shared, CI, or heavily monitored machines.

Risk: Harvested notes, comments, user data, and reports may contain sensitive or policy-relevant content.

Mitigation: Review outputs before sharing, avoid publishing raw harvest data, and delete local artifacts that are no longer needed.

Risk: Bulk scraping, comment collection, proxy or IP changes, and captcha-related workflows may create compliance risk.

Mitigation: Confirm the workflow complies with applicable obligations and Xiaohongshu rules before use, and stop when captcha or IP-risk signals appear.

Risk: Repeated browser opens or retries can increase captcha and IP-risk lockouts.

Mitigation: Prefer the provided scripts with their rate limits, avoid manual high-frequency agent-browser calls, and do not retry automatically after captcha or IP-risk failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/excalibursssooo/skills/xhs-cli)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Anti-scraping pitfalls](docs/pitfalls.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime scripts write JSON files and Markdown reports to disk.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, agent-browser, and authenticated Xiaohongshu cookies; cookie and data paths can be configured with XHS_COOKIE_FILE and XHS_DATA_DIR.]

## Skill Version(s):

1.3.1 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
