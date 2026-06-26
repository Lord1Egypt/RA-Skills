## Description: <br>
Archives web articles into an Obsidian vault by extracting, cleaning, classifying, and saving content from WeChat, Futu, Xueqiu, Eastmoney, and general webpages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to capture authorized web articles, clean navigation and advertising noise, classify the content by industry, and store both raw text and structured Markdown in Obsidian. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic scraping fallbacks may be inappropriate for private, paywalled, tokenized, or otherwise unauthorized pages. <br>
Mitigation: Use the skill only with public or authorized URLs and avoid submitting private or access-controlled links. <br>
Risk: Optional Tavily and Firecrawl extraction paths may send URLs or article content to third-party providers. <br>
Mitigation: Configure Tavily or Firecrawl only when their data handling is acceptable for the target content. <br>
Risk: The release security summary flags under-scoped scraping bypass behavior that should be reviewed before installation. <br>
Mitigation: Review the extraction behavior and installed dependencies before deployment, especially in environments with compliance or website-use restrictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/web-article-to-obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown files with YAML frontmatter, raw text archives, and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes article archives into a local Obsidian vault and may require Python dependencies, Playwright, Tavily API credentials, or Firecrawl depending on the extraction path used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
