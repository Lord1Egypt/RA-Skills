## Description: <br>
Creates T.LY short links through the T.LY API when an agent has a valid T.LY API key available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timleland](https://clawhub.ai/user/timleland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation agents, and external users use this skill to create shareable T.LY short URLs from full http or https destination URLs when a valid T.LY API token is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: T.LY API tokens can be exposed if pasted into commands, logs, or generated files. <br>
Mitigation: Keep TLY_API_TOKEN in an environment variable or secret store and do not hardcode real API keys. <br>
Risk: Shortened links can obscure the destination URL. <br>
Mitigation: Review destination URLs before shortening them and surface API failures clearly instead of guessing. <br>
Risk: The workflow can rely on an optional PyPI package before calling the T.LY API. <br>
Mitigation: Review or pin the package before installing it, or use the direct API fallback when package installation is not appropriate. <br>


## Reference(s): <br>
- [T.LY homepage](https://t.ly/) <br>
- [T.LY Short Link API Reference](references/api.md) <br>
- [tly-url-shortener-api PyPI package](https://pypi.org/project/tly-url-shortener-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell, Python, curl, text, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a short_url when the T.LY API call succeeds; requires a valid TLY_API_TOKEN.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
