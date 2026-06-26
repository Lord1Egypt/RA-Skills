## Description: <br>
YNote News analyzes recent favorite notes in Youdao Cloud Notes, searches for current related articles, and produces a structured news briefing that can be triggered on demand or scheduled daily. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lephix](https://clawhub.ai/user/lephix) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users with a YNote account use this skill to turn recently favorited notes into topic clusters, current-article searches, and a concise news briefing. The skill can also help configure a recurring daily briefing schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads recent favorite-note excerpts and derives search topics from them. <br>
Mitigation: Review YNote API permissions before installing and avoid using the skill with notes that contain sensitive material. <br>
Risk: The skill can be configured to run every day, creating recurring access to note excerpts and web search services. <br>
Mitigation: Enable the cron job only when recurring briefings are intended, and remove or review the scheduled job when it is no longer needed. <br>
Risk: The open-websearch fallback runs an unpinned npm package at runtime. <br>
Mitigation: Pin or remove the open-websearch fallback before use in higher-trust environments. <br>
Risk: The skill depends on external search credentials and services. <br>
Mitigation: Use a dedicated Perplexity key and review any Brave or fallback search configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lephix/ynote-news) <br>
- [OpenClaw Brave Search documentation](https://docs.openclaw.ai/brave-search) <br>
- [Perplexity Search API quickstart](https://docs.perplexity.ai/docs/search/quickstart) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown news briefing with article links and a summary table, plus shell commands for note retrieval, search, notifications, and cron setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YNOTE_API_KEY and command-line tools curl, jq, and node; search can use Perplexity, Brave, or an open-websearch fallback.] <br>

## Skill Version(s): <br>
1.2.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
