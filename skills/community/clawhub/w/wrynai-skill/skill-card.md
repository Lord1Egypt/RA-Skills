## Description: <br>
Helps agents use the WrynAI SDK for web crawling, search result crawling, content extraction, link extraction, structured data extraction, and screenshot capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrynai](https://clawhub.ai/user/wrynai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to gather web content, crawl documentation or search results, extract page text and links, and capture screenshots through WrynAI-backed workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WrynAI as an external provider for crawling, search, extraction, and screenshot workflows. <br>
Mitigation: Use it only where third-party processing is approved, and avoid crawling private, internal, regulated, or sensitive pages unless explicitly authorized. <br>
Risk: The skill requires a WRYNAI_API_KEY environment variable. <br>
Mitigation: Use a revocable API key, keep it out of committed files and logs, and rotate it if exposure is suspected. <br>
Risk: The screenshot example writes screenshot.png in the current working directory and may overwrite an existing file. <br>
Mitigation: Choose a unique output path or check for an existing file before running screenshot capture examples. <br>
Risk: The skill depends on the third-party wrynai package. <br>
Mitigation: Verify the package source before installation and pin versions in controlled environments. <br>


## Reference(s): <br>
- [WrynAI Documentation](https://docs.wryn.ai) <br>
- [WrynAI API Signup](https://wryn.ai) <br>
- [wrynai-python GitHub Repository](https://github.com/wrynai/wrynai-python) <br>
- [ClawHub Skill Page](https://clawhub.ai/wrynai/wrynai-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/wrynai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce text, markdown, JSON-like dictionaries, links, structured extraction results, and screenshot files through WrynAI SDK examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact version information) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
