## Description: <br>
Searches Xiaohongshu, reads notes and user profiles, and harvests selected content through agent-browser using user-provided login cookies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[excalibursssooo](https://clawhub.ai/user/excalibursssooo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to collect Xiaohongshu search results, note details, comments, and user-profile content into local JSON and Markdown reports. It is intended for logged-in, read-only collection workflows that require Xiaohongshu session cookies and agent-browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Xiaohongshu session cookies and can store those credentials locally. <br>
Mitigation: Keep cookie files private, use secure local or explicitly configured paths, and avoid sharing cookie or state files. <br>
Risk: Harvested Xiaohongshu content may include user-generated personal or sensitive information. <br>
Mitigation: Review harvested JSON and Markdown reports before sharing or publishing them, and follow applicable privacy expectations. <br>
Risk: Scraping activity may conflict with Xiaohongshu rules or trigger platform rate limits and account/IP controls. <br>
Mitigation: Use the documented rate limits and no-retry behavior, and confirm that planned scraping complies with Xiaohongshu rules and applicable policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/excalibursssooo/xhs-cli) <br>
- [README](README.md) <br>
- [Anti-scraping pitfalls](docs/pitfalls.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts produce JSON files and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under the configured data directory, including harvest reports, candidate lists, result status JSON, note detail JSON, user metadata JSON, and cookie/state files.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
