## Description: <br>
Scrapes Spotify-related public news from configured RSS, Hacker News, and DuckDuckGo News sources, then formats a daily or weekly digest with source links and Chinese one-sentence summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibillxia](https://clawhub.ai/user/ibillxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product analysts, and communications teams use this skill to collect recent Spotify product, engineering, research, community, and industry news into a concise digest for briefings or scheduled updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public news and search results over the network, which may be inappropriate in environments where outbound public access is restricted. <br>
Mitigation: Run it only where outbound public news and search access is acceptable, and keep configured sources limited to public news domains. <br>
Risk: Scheduled digests can send generated summaries to an unintended recipient or cadence if approved without review. <br>
Mitigation: Verify the recipient and schedule before approving any automated digest. <br>
Risk: Unpinned Python dependencies can change over time and affect reproducibility. <br>
Mitigation: Review or pin dependencies before installation when reproducibility or production controls matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibillxia/spotify-news-digest) <br>
- [Source Reference - Spotify News Digest](references/sources_reference.md) <br>
- [Configured news sources](config/sources.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest with source links; optional grouped article data from the Python helpers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest entries are grouped by category and use one-sentence Chinese summaries when supplied by the calling LLM.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
