## Description: <br>
Stock Watcher is a Chinese stock monitoring and alert skill that documents configurable alerts for cost thresholds, moving-average crosses, RSI levels, volume changes, gap moves, intraday movement, and trailing profit protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandelion80231](https://clawhub.ai/user/dandelion80231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and investors can use this skill as agent guidance for setting up stock watchlists, portfolio thresholds, and alerting workflows for China-market stocks, ETFs, and gold instruments. The skill focuses on monitoring and alert explanation, not financial decision automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Referenced daemon-mode monitor scripts are not bundled in this documentation-only release. <br>
Mitigation: Review any separately obtained scripts before execution, especially before enabling continuous background monitoring. <br>
Risk: Continuous stock monitoring may store watchlist or portfolio details locally and contact market-data services. <br>
Mitigation: Review local configuration and data files before use, and avoid storing sensitive portfolio information where other users or services can access it. <br>
Risk: Financial alerts and technical indicators can be stale, incomplete, or misleading. <br>
Mitigation: Treat generated alerts as informational guidance and review market context before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dandelion80231/skills/stock-watcher-2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only artifact; referenced monitor scripts are not bundled in this release.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
