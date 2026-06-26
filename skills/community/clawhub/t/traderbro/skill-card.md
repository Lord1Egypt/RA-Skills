## Description: <br>
Query analyst predictions, content, and market research from the TraderBro platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datalin](https://clawhub.ai/user/datalin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query TraderBro analyst rankings, market predictions, symbol coverage, content, and research through the TraderBro CLI. It supports investment research workflows but should treat market predictions as research inputs rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TraderBro API key, which could be exposed in chats, shell history, or logs. <br>
Mitigation: Use a dedicated TraderBro API key where possible, avoid pasting real keys into chats or logs, and revoke or rotate the key if exposed. <br>
Risk: The workflow depends on an external Homebrew-installed TraderBro binary and tap. <br>
Mitigation: Install only when the TraderBro publisher and Homebrew tap are trusted, and review the binary source before use in sensitive environments. <br>
Risk: Analyst predictions and market research may be incorrect or misleading if treated as financial advice. <br>
Mitigation: Use TraderBro outputs as research inputs and require independent review before making investment decisions. <br>


## Reference(s): <br>
- [TraderBro skill page](https://clawhub.ai/datalin/traderbro) <br>
- [TraderBro platform](https://traderbro.ai) <br>
- [TraderBro CLI homepage](https://github.com/TraderBro/traderbro-cli-binary) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the traderbro binary and TRADERBRO_API_KEY for authenticated queries.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
