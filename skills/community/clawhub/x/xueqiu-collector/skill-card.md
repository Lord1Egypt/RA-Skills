## Description: <br>
xueqiu-collector collects full or incremental Xueqiu user posts, downloads images for OCR, applies local V4 rule analysis, and exports SQLite, JSON, and Markdown backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangjia-ie](https://clawhub.ai/user/zhangjia-ie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to archive, update, and analyze Xueqiu posts for personal investment records, monitored accounts, market discussion tracking, or knowledge-base workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses logged-in Edge browser automation to collect Xueqiu posts, images, and OCR data at broad scope. <br>
Mitigation: Use a dedicated Edge profile and Xueqiu account, and confirm that the target account and collection scope are authorized before running collection. <br>
Risk: Large or repeated scraping may violate site rules or trigger rate limits. <br>
Mitigation: Avoid large or repeated scraping, respect Xueqiu terms, and keep the built-in delays, retry limits, and collection limits enabled. <br>
Risk: Exported databases, Markdown, JSON, images, OCR text, and logs may contain sensitive or private data. <br>
Mitigation: Store outputs in a private folder, restrict access, and define a deletion plan before collecting data. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [category_keywords.json](artifact/references/category_keywords.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime artifacts include SQLite databases, JSON exports, Markdown exports, downloaded images, OCR text, and logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a logged-in Edge browser profile and local rule-based analysis; no AI API is required by the artifact documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
