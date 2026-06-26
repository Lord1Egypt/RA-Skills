## Description: <br>
Toutiao helps agents retrieve and summarize public Toutiao articles, videos, and topics for lightweight trend analysis and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to summarize public Toutiao search results, channel items, and video metadata, including titles, authors, publish times, interactions, tags, source links, and collection time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated collection from Toutiao could conflict with platform rules or create excessive request volume. <br>
Mitigation: Use the skill only for public pages, prefer manual page opening before parsing, apply frequency controls, and avoid batch scraping. <br>
Risk: Video handling could be misused for downloading content or removing watermarks. <br>
Mitigation: Limit video work to public metadata such as title, description, and visible interactions; do not download videos or remove watermarks. <br>
Risk: Summaries of dynamic public pages can become stale or lose source context. <br>
Mitigation: Include source links and collection time in outputs whenever available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/toutiao-trending) <br>
- [Toutiao homepage](https://www.toutiao.com/) <br>
- [Toutiao search](https://www.toutiao.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and analysis lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes public source links and collection time when available; excludes video downloads and watermark removal.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
