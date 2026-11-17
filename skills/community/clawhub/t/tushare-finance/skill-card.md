## Description:

Helps an agent retrieve financial market data through Tushare Pro, covering A-shares, Hong Kong and U.S. stocks, funds, futures, bonds, financial statements, and macroeconomic indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanleychanh](https://clawhub.ai/user/stanleychanh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to have an agent identify the right Tushare Pro interface, configure token-based access, and produce Python or shell examples for market data retrieval and export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tushare API requests require a token and send user queries to Tushare.

Mitigation: Use the skill only with an intended Tushare account, keep tokens in environment variables, and avoid exposing secrets in prompts, logs, or generated files.

Risk: The bundled documentation crawler can use Tushare account credentials, CAPTCHA OCR, a headless browser, network access, and broad local writes.

Mitigation: Do not run scripts/crawl_docs.py or enable the documented sync workflow unless document crawling is intended; run it in an isolated environment, prefer dry-run mode first, pin dependencies, and review write targets.

Risk: The security scan flags broader-than-advertised datasets and recommends review before installation.

Mitigation: Review requested data categories and installed files before deployment, especially when workflows touch non-financial or crawler-sourced datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stanleychanh/skills/tushare-finance)
- [Bundled Tushare API documentation index](reference/README.md)
- [Tushare official documentation](https://tushare.pro/document/2)
- [Tushare API test tool](https://tushare.pro/document/1)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tushare token for live API calls; examples commonly return pandas DataFrames or exported CSV/XLSX files.]

## Skill Version(s):

2.1.0 (source: server release metadata, artifact metadata, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
