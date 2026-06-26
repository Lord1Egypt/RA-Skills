## Description: <br>
Super Rss Agent helps an agent manage RSS and Atom subscriptions, import and export OPML, scan and search articles, track read status, generate digests and summaries, and store feed state locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohyeah521](https://clawhub.ai/user/ohyeah521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn an OpenClaw agent into a local RSS reader for tracking subscriptions, finding new articles, summarizing selected content, and maintaining read/unread state. It is useful for recurring news, blog, and topic monitoring workflows where feed data should remain in a local SQLite database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts RSS or website URLs that the user adds. <br>
Mitigation: Add feeds intentionally, avoid untrusted internal or sensitive URLs, and rely on the documented SSRF checks for normal HTTP and HTTPS feed access. <br>
Risk: Subscriptions, articles, summaries, and read state are stored in a local SQLite database. <br>
Mitigation: Keep the database in a protected workspace path, use the documented --db option when isolation is needed, and avoid adding feeds whose stored content should not be retained locally. <br>
Risk: Feed content is untrusted text that may be summarized or acted on by an agent. <br>
Mitigation: Treat article titles, summaries, and scraped content as untrusted input; verify important claims before using them for decisions or follow-up actions. <br>
Risk: Old read articles may be deleted automatically after scans. <br>
Mitigation: Disable automatic cleanup with the documented config auto_purge false setting or adjust auto_purge_days before running recurring scans. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ohyeah521/super-rss-agent) <br>
- [blogwatcher architecture reference](https://github.com/Hyaxia/blogwatcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text CLI output with inline shell commands and optional JSON cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores subscriptions, article metadata, read state, and settings in a local SQLite database.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
