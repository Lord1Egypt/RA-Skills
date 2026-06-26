## Description: <br>
Rss Content Flow helps an agent manage RSS subscriptions, fetch recent feed items, filter stale or promotional entries, and present structured article candidates for content planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agents use this skill to collect current RSS articles from configured sources and turn the resulting titles, links, descriptions, dates, and source labels into candidate topics or drafts. Optional saving or publishing integrations should be invoked only after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured RSS URLs can cause the agent to fetch external, private, or internal resources. <br>
Mitigation: Review and edit the feed list before use, and avoid private or internal URLs unless fetching them is intended. <br>
Risk: Documentation describes optional saving or publishing workflows beyond the RSS helper itself. <br>
Mitigation: Require explicit user confirmation before invoking any separate Feishu save or social publishing tool. <br>
Risk: Fetched article summaries and generated drafts can be stale, incomplete, or unsuitable for publication. <br>
Mitigation: Review the source links and any generated content before using it in public channels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/freedompixels/rss-content-flow) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Feed Fetch Script](artifact/scripts/fetch_feed.py) <br>
- [Feed Management Script](artifact/scripts/manage_feeds.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON feed output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch results include article title, link, description, publication date, and source when JSON output is requested.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
