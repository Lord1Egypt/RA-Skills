## Description: <br>
Unified News retrieves and formats Web3/Crypto, AI technology, macroeconomic, and financial market news with category fetching, scheduled delivery, deduplication, and Feishu message output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to collect news across Web3/Crypto, AI, macroeconomic, finance, and technology categories, then produce a concise digest for Feishu delivery. It is suited to recurring news briefings where duplicate items should be filtered before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring delivery can send repeated or unintended Feishu messages if a cron job is created without confirming the recipient, bot account, and desired cadence. <br>
Mitigation: Confirm the Feishu recipient and bot account before creating the cron job, and only enable recurring delivery when scheduled messages are intended. <br>
Risk: Local deduplication state can suppress or resend items depending on the contents of memory/news-sent.md. <br>
Mitigation: Review, preserve, or delete memory/news-sent.md intentionally when changing deduplication behavior or resetting delivery history. <br>
Risk: News retrieval depends on external APIs and RSS feeds, so source availability or content quality can affect the digest. <br>
Mitigation: Review generated digests before relying on them for important decisions or onward distribution. <br>


## Reference(s): <br>
- [Unified News ClawHub page](https://clawhub.ai/gaoren36-arch/unified-news) <br>
- [6551 API categories endpoint](https://ai.6551.io/open/free_categories) <br>
- [6551 API crypto news endpoint](https://ai.6551.io/open/free_hot?category=crypto) <br>
- [6551 API AI news endpoint](https://ai.6551.io/open/free_hot?category=ai) <br>
- [6551 API macro news endpoint](https://ai.6551.io/open/free_hot?category=macro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest with optional shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source labels, bilingual summaries, heat scores, related token or stock tags, Feishu message content, and deduplication state updates when used as documented.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
