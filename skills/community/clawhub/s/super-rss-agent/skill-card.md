## Description:

Super RSS Agent helps an agent manage RSS subscriptions, import and export OPML, discover and scan feeds, track read status, search articles, create digests, and clean old items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohyeah521](https://clawhub.ai/user/ohyeah521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent maintain RSS subscriptions, scan for updates, search unread items, produce daily digests, and import or export OPML feed lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests from the agent host to user-configured RSS, Atom, and HTML URLs.

Mitigation: Install it only in environments where this network behavior is acceptable, and avoid attacker-controlled feeds or OPML imports in sensitive networks.

Risk: The skill stores subscription and article history locally.

Mitigation: Use an appropriate database path and treat the database as local browsing and reading history.

Risk: Fetched article text is untrusted input that may influence downstream agent summaries.

Mitigation: Review generated summaries before acting on them and avoid letting fetched content trigger sensitive actions without confirmation.

Risk: Automatic purging can delete older read articles after scans.

Mitigation: Disable auto_purge or adjust auto_purge_days when manual retention control is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ohyeah521/skills/super-rss-agent)
- [Publisher profile](https://clawhub.ai/user/ohyeah521)
- [blogwatcher architecture reference](https://github.com/Hyaxia/blogwatcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [CLI text, Markdown summaries, and OPML files when import or export is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite storage for subscriptions, article history, read status, and settings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
