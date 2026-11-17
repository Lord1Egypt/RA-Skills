## Description:

This skill guides an AI agent to connect to a user-opened debugging browser session, extract visible page and comment data from Xiaohongshu, Douyin, Bilibili, or generic web pages, and export the results to Excel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yourtsao](https://clawhub.ai/user/yourtsao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill through an AI agent to collect authorized, visible social-media or webpage content and comments from their own logged-in browser session into an Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad CDP access to logged-in browser pages.

Mitigation: Use a dedicated debugging browser session, close unrelated tabs, and review the target URLs before extraction.

Risk: The exported spreadsheet can contain visible page content, comments, user names, and other sensitive personal data.

Mitigation: Collect only pages the user is authorized to access and handle the XLSX output as sensitive data.

Risk: Browser-session scraping may collect only content that has been loaded or expanded in the visible page.

Mitigation: Before extraction, load the intended pages, scroll comment areas to the end, and expand folded replies that should be included.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yourtsao/skills/web-data-scraper)
- [Desktop release link referenced by artifact](https://github.com/Yourtsao/web-data-scraper/releases)
- [Artifact usage guide](artifact/使用说明.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with bash command blocks and generated XLSX spreadsheet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Excel workbook contains an overview sheet for page-level fields and a comments sheet for extracted comments and folded replies.]

## Skill Version(s):

1.5.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
