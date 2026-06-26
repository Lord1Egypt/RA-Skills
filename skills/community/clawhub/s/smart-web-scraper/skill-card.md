## Description: <br>
Extract structured data from web pages with CSS selectors, table and list auto-detection, and JSON or CSV output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, analysts, and agents use this skill to extract structured data from static HTML pages, including selected elements, tables, links, page structure, and paginated listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scrape sites where automated collection is not authorized or appropriate. <br>
Mitigation: Use it only on sites you are authorized to scrape and keep robots.txt enforcement enabled unless there is a clear lawful reason to override it. <br>
Risk: The skill can collect personal, sensitive, or regulated data from web pages. <br>
Mitigation: Avoid collecting personal or sensitive data without consent or another valid basis, and review extracted data before sharing or storing it. <br>
Risk: The crawler can place unnecessary load on target sites when pagination or short delays are used. <br>
Mitigation: Limit page counts, keep rate limiting enabled, and use conservative delays for repeated requests. <br>
Risk: Saved output can overwrite an existing local file. <br>
Mitigation: Choose output paths deliberately and verify the destination before running commands with the output flag. <br>
Risk: Static HTML extraction can miss content rendered by JavaScript or return incomplete data. <br>
Mitigation: Validate sampled results against the source page and use a JavaScript-capable workflow when the target site renders data client-side. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariusfit/smart-web-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands] <br>
**Output Format:** [Plain text, JSON, CSV, or Markdown extracted from static HTML pages, with shell commands for invoking the scraper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write extracted output to a user-selected file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
