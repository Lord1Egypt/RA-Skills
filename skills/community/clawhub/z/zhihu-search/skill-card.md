## Description: <br>
Searches and extracts Zhihu questions, answers, columns, comments, and hot-list content using API-first Python commands with a user-provided session cookie. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[excalibursssooo](https://clawhub.ai/user/excalibursssooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to retrieve read-only Zhihu search results, answers, article text, column article lists, comments, and hot-list summaries for content research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a live Zhihu logged-in session cookie. <br>
Mitigation: Use a dedicated low-privilege Zhihu account when possible, keep the cookie file private, and restrict file permissions such as chmod 600. <br>
Risk: Optional keepalive cron can persist the session through scheduled background refreshes. <br>
Mitigation: Run install-cron only when daily refresh is intentional, and review or remove the cron entry when persistence is no longer needed. <br>
Risk: Keepalive commands may restart existing agent-browser sessions. <br>
Mitigation: Run keepalive open, check, or refresh only when interrupting other agent-browser work is acceptable, or isolate browser sessions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/excalibursssooo/zhihu-search) <br>
- [Project homepage](https://github.com/excalibursssooo/zhihu-search) <br>
- [Release v1.1.0](https://github.com/excalibursssooo/zhihu-search/releases/tag/v1.1.0) <br>
- [agent-browser optional dependency](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON files, shell commands, configuration] <br>
**Output Format:** [CLI text, Markdown summaries, and JSON files written under the skill data directory or an explicit --md-out path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and curl. Uses ZHIHU_COOKIE_FILE or the skill data directory for user-supplied Zhihu cookies.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, CHANGELOG, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
