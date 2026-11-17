## Description:

Web scraping and content comprehension agent for multi-strategy extraction with cascade fallback, news detection, boilerplate removal, structured metadata, and LLM entity extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to plan and generate web scraping workflows for public pages, including Python extraction scripts, YAML selector configuration, and structured article or entity outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used to reveal or collect soft-paywalled content.

Mitigation: Use it only on content the user is authorized to access, avoid collecting paywalled content, and restrict hard-paywall handling to public preview text and metadata.

Risk: Optional LLM entity extraction can send scraped page text to OpenRouter.

Mitigation: Disable LLM extraction for private, authenticated, or sensitive pages unless the user gives explicit approval for that data flow.

Risk: Generated scraping code may install and run browser, crawling, and network dependencies.

Mitigation: Run generated scripts in an isolated environment with pinned dependencies and review network targets before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guifav/skills/web-scraper)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python, YAML, shell commands, and structured JSON result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scraper scripts and output files that perform network access; optional entity extraction uses OPENROUTER_API_KEY in generated code.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact changelog and manifest report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
