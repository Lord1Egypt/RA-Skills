## Description: <br>
Access Yahoo Finance data including real-time pricing, fundamentals, analyst estimates, options, news, and historical data via the yahooquery Python library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[512z](https://clawhub.ai/user/512z) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and financial analysts use this skill to ask an agent for yahooquery examples and guidance for retrieving Yahoo Finance pricing, fundamentals, financial statements, screeners, options, news, historical data, and premium research data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Premium Yahoo Finance credentials may be exposed if pasted into prompts, shared transcripts, or checked-in files. <br>
Mitigation: Use premium credentials only when needed and provide them through protected environment variables or a secrets manager. <br>
Risk: Disabling TLS verification or routing through untrusted proxies can expose finance requests and credentials. <br>
Mitigation: Keep TLS verification enabled and avoid untrusted proxies. <br>
Risk: Yahoo Finance may rate-limit or block requests, and upstream data accuracy or availability can vary. <br>
Mitigation: Use retry, backoff, and timeout settings for robustness, and verify finance data before relying on it for decisions. <br>


## Reference(s): <br>
- [yahooquery overview](references/index.md) <br>
- [Keyword arguments](references/keyword_arguments.md) <br>
- [Ticker intro](references/ticker/intro.md) <br>
- [Ticker modules](references/ticker/modules.md) <br>
- [Ticker financials](references/ticker/financials.md) <br>
- [Ticker historical prices](references/ticker/historical.md) <br>
- [Ticker options](references/ticker/options.md) <br>
- [Screener](references/screener.md) <br>
- [Research](references/research.md) <br>
- [Miscellaneous functions](references/misc.md) <br>
- [Advanced session sharing](references/advanced.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include yahooquery API usage examples and configuration options for async requests, retries, proxies, TLS verification, and premium credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
