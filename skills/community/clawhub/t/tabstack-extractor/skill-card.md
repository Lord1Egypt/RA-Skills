## Description:

Extract structured data from websites using Tabstack API. Use when you need to scrape job listings, news articles, product pages, or any structured web content. Provides JSON schema-based extraction and clean markdown conversion. Requires TABSTACK_API_KEY environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noblepayne](https://clawhub.ai/user/noblepayne)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract clean Markdown or schema-shaped JSON from public web pages such as job listings, news articles, product pages, and other structured web content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start path recommends piping a mutable remote install script directly into a shell.

Mitigation: Prefer a package-manager install path or inspect and pin the installer before executing it.

Risk: Target URLs, schemas, and extracted page content are processed by the third-party Tabstack API.

Mitigation: Avoid internal, authenticated, private, or sensitive pages unless that third-party processing is intended and approved.

Risk: API keys can be exposed if stored in plaintext config files or committed with examples.

Mitigation: Use environment variables or a secure credential store and keep Tabstack credentials out of source control.

## Reference(s):

- [Tabstack API Reference](references/api_reference.md)
- [Schema Creation Guide](references/schema_guide.md)
- [Job Listing Schema](references/job_schema.json)
- [News Article Schema](references/news_schema.json)
- [Simple Article Schema](references/simple_article.json)
- [Tabstack API Docs](https://docs.tabstack.ai/api/tabs-api)
- [JSON Schema Documentation](https://json-schema.org/learn/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and API wrapper code; runtime extraction returns Markdown text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tabstack API key and sends target URLs, schemas, and extracted page content to the Tabstack API.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
