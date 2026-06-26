## Description: <br>
Monitor topics of interest and proactively alert when important developments occur across web searches, RSS/Atom feeds, GitHub releases, and scheduled digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, operators, and analysts use this skill to configure recurring monitoring for topics, feeds, releases, and alerts. It helps turn configured sources into prioritized alerts, sentiment-aware summaries, and weekly digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring monitoring can repeatedly query external search, feed, or GitHub sources and send alerts through configured channels. <br>
Mitigation: Review every configured query, feed, GitHub repository, alert channel, and generated cron job before enabling automation. <br>
Risk: Sensitive watchlists or topics may be disclosed to search providers, feed hosts, or GitHub endpoints during monitoring. <br>
Mitigation: Avoid sensitive watchlists unless the user accepts disclosure to those services, and keep local state in a controlled data directory. <br>
Risk: A configured WEB_SEARCH_PLUS_PATH can cause the skill to invoke a local search script. <br>
Mitigation: Set WEB_SEARCH_PLUS_PATH only to a trusted local web-search-plus script. <br>


## Reference(s): <br>
- [Topic Monitor ClawHub Skill Page](https://clawhub.ai/robbyczgw-cla/topic-monitor) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Example Configuration](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, alert records, and digest text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit Telegram or Discord alert payloads through the agent and maintain local monitoring state.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release metadata, SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
