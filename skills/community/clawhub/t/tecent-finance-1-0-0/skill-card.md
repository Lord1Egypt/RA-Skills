## Description: <br>
Get stock prices, quotes, and compare stocks using Tencent Finance API without an API key, with support for US stocks, China A-shares, Hong Kong stocks, and popular cryptocurrencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squally2k](https://clawhub.ai/user/squally2k) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External users and developers use this skill to install and run a Python CLI for checking current prices, detailed quotes, stock comparisons, and symbol searches through Tencent Finance. It is especially relevant when direct mainland China access to market data is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed bundle contains documentation and metadata, but not the referenced tfin executable or source code. <br>
Mitigation: Verify the actual executable or source code from the publisher before installation, and use a Python virtual environment for dependencies. <br>
Risk: The optional global symlink can expose the CLI broadly on the host system. <br>
Mitigation: Create the /usr/local/bin symlink only when global command access is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squally2k/tecent-finance-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced CLI returns market data from Tencent Finance for supported symbols; unsupported markets and options or dividend data are outside the documented scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
