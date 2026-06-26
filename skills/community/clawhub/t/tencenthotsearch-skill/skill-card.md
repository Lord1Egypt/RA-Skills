## Description: <br>
Fetches trending news and articles using Tencent Cloud Online Search API (SearchPro), with web-wide or site-specific search and JSON, CSV, TXT, and Markdown exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neuhanli](https://clawhub.ai/user/neuhanli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Tencent Cloud SearchPro for trending topics, recent articles, and site-specific news, then export the results for review or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Cloud API credentials are required for use. <br>
Mitigation: Use a dedicated or temporary least-privileged Tencent API key, keep config.json private, and rotate credentials after testing. <br>
Risk: Search queries and retrieved results are sent through Tencent Cloud SearchPro. <br>
Mitigation: Avoid confidential search queries and review whether the data is appropriate for the selected Tencent Cloud account and region. <br>
Risk: The skill writes search output files to user-selected or configured paths. <br>
Mitigation: Choose a non-sensitive output directory and avoid paths that could overwrite important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neuhanli/tencenthotsearch-skill) <br>
- [Configuration guide](CONFIG.md) <br>
- [Security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, CSV, TXT, and console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include titles, summaries, source platforms, publication times, URLs, relevance scores, image URLs, and query metadata.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
