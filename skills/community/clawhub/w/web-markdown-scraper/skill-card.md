## Description: <br>
Fetches one or more public webpages with Scrapling, extracts main content, and converts HTML to Markdown using html2text across static, concurrent async, stealth, and dynamic browser fetching modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yumiu8103-hue](https://clawhub.ai/user/yumiu8103-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content or data engineers use this skill to fetch authorized public webpages, extract article or body content, and convert it to Markdown for summarization, analysis, indexing, or local review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the skill encourages anti-bot evasion and needs review before use. <br>
Mitigation: Use it only for authorized public pages and avoid anti-bot bypass workflows unless the target site and use case permit that access. <br>
Risk: Proxy credentials may be exposed when placed directly in command-line arguments. <br>
Mitigation: Avoid real proxy passwords in shell history or shared logs; prefer a local config or other secret-handling mechanism when available. <br>
Risk: Scraped page content is written to local output files by default. <br>
Mitigation: Review target URLs and output directories before execution, and handle saved Markdown and index files according to the sensitivity of the source content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yumiu8103-hue/web-markdown-scraper) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yumiu8103-hue) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Python](https://python.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands] <br>
**Output Format:** [JSON on stdout with extracted Markdown content; optional Markdown files and index.json written locally.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include requested URL, status, title, extracted markdown, preview text, and local output paths when files are saved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
