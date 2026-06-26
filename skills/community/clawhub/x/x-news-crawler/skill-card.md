## Description: <br>
Crawl X (Twitter) search results through a local CLI that wraps `abs` (agent-browser). Use when the user asks to scrape X posts by keyword, collect Top/Latest news, extract structured fields (author/time/text/link), or produce a deduplicated "top-first then latest" feed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeguooooo](https://clawhub.ai/user/leeguooooo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to collect recent X search results for a keyword and produce a structured, deduplicated news feed for review and summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in social account through Chrome remote debugging, which can expose cookies, sessions, and browsing data. <br>
Mitigation: Use a dedicated temporary Chrome profile when possible, bind remote debugging to localhost, and close the browser after crawling. <br>
Risk: The artifact instructs users to launch Chrome with a regular profile and no isolated user-data directory. <br>
Mitigation: Do not use a daily profile unless the user intentionally accepts the session and browsing-data exposure described by the security guidance. <br>
Risk: Social posts may include rumors or unverified claims, even when engagement is high. <br>
Mitigation: Treat collected posts as source material for review, verify claims against authoritative sources, and report low-confidence items separately. <br>


## Reference(s): <br>
- [CLI Reference](references/cli.md) <br>
- [ClawHub Release Page](https://clawhub.ai/leeguooooo/x-news-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The crawler output JSON includes fetched_at, query, mode, count, warnings, failed_sources, and rows containing source, datetime, status_url, user, text, replies, reposts, and likes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
