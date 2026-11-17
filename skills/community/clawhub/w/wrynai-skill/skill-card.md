## Description:

Enables an agent to use the WrynAI SDK for web crawling, content extraction, search result parsing, URL filtering, and screenshot capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrynai](https://clawhub.ai/user/wrynai)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to crawl websites, documentation, and search results, then extract text, markdown, structured data, links, and screenshots for research, monitoring, migration, and knowledge-base workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends target URLs and extracted content through a third-party crawling provider.

Mitigation: Use it only for URLs and page content approved for WrynAI processing; avoid private, internal, or sensitive sites unless that use is authorized.

Risk: The setup example installs an unpinned SDK package.

Mitigation: Use a virtual environment and pin the WrynAI SDK version before operational use.

Risk: The screenshot example writes to a fixed filename and may overwrite an existing local file.

Mitigation: Change the example to write screenshots to a deliberate non-overwriting path.

Risk: Web crawling can hit rate limits, timeouts, or blocked pages.

Mitigation: Keep page and depth limits in place, handle WrynAI rate-limit and timeout errors, and respect robots.txt and site access constraints.

## Reference(s):

- [WrynAI documentation](https://docs.wryn.ai)
- [WrynAI API signup](https://wryn.ai)
- [WrynAI Python SDK](https://github.com/wrynai/wrynai-python)
- [ClawHub skill page](https://clawhub.ai/wrynai/skills/wrynai-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/wrynai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include crawl result dictionaries, extracted page content, search result summaries, link lists, structured text, and screenshot file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version information)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
