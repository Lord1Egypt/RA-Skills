## Description:

Social Media Dashboard helps an agent collect creator analytics and revenue data from Toutiao, CSDN, and Zhihu through browser-assisted workflows and generate Markdown dashboards or reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luduoxin](https://clawhub.ai/user/luduoxin)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to consolidate logged-in creator-center metrics, including fans, content performance, reading or playback activity, and revenue. Agents can use the collected data to prepare personal operating dashboards, daily reports, trend summaries, and improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent or browser to read logged-in creator dashboards that may include private analytics, revenue, and account information.

Mitigation: Install only when this access is acceptable, keep collected data local when possible, and review or redact reports before sharing them.

Risk: The Chrome remote-debugging helper reuses the normal Chrome profile, which can expose active browser sessions to local debugging clients.

Mitigation: Avoid the helper with a normal browser profile; use a separate temporary profile or manual collection workflow when handling sensitive accounts.

Risk: Cookie and session-based workflows can leak credentials if users paste raw cookies or unredacted session material into chat, terminals, or shared files.

Mitigation: Do not paste raw cookies into chat or terminals, delete unneeded session material, and prefer browser-mediated collection over direct credential handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luduoxin/skills/social-media-dashboard)
- [Toutiao collection notes](artifact/platforms/toutiao.md)
- [CSDN collection notes](artifact/platforms/csdn.md)
- [Zhihu collection notes](artifact/platforms/zhihu.md)
- [Dashboard template](artifact/templates/dashboard.md)
- [Daily report template](artifact/templates/daily-report.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, code, guidance]

**Output Format:** [Markdown reports and dashboards with inline shell, AppleScript, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include locally collected creator analytics, account metrics, and revenue data that should be reviewed and redacted before sharing.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
