## Description: <br>
VerdictSwarm provides multi-agent crypto token risk analysis with rug-pull detection, security review, and consensus scoring through MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vswarm-ai](https://clawhub.ai/user/vswarm-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and trading agents use this skill to screen crypto tokens on Solana, Ethereum, Base, and BSC before trades or payments by requesting quick scores, rug-risk checks, full consensus scans, or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends token identifiers, chain choices, and scan context to VerdictSwarm's external service. <br>
Mitigation: Use it only when external transmission of this scan context is acceptable for the user and environment. <br>
Risk: The MCP integration depends on an external package installed with pip. <br>
Mitigation: Review the external MCP package before installation and deployment. <br>
Risk: Risk scores may be mistaken for trade authorization. <br>
Mitigation: Treat scores and consensus reports as decision support rather than automatic approval for trades or payments. <br>


## Reference(s): <br>
- [VerdictSwarm ClawHub listing](https://clawhub.ai/vswarm-ai/verdictswarm) <br>
- [VerdictSwarm API endpoint](https://api.vswarm.io/api/scan/quick) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands and API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verdict scores, risk levels, consensus summaries, disagreement notes, pricing or payment verification details, and report URLs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
