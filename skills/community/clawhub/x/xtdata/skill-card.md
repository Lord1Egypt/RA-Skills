## Description: <br>
Guides agents in using XtQuant xtdata with local miniQMT for real-time quotes, K-line, tick, Level2, and financial data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and quantitative analysts use this skill to have an agent produce read-only xtdata guidance, examples, and setup steps for retrieving market data through a locally running miniQMT client. Use should be constrained to market-data workflows unless a human explicitly approves account or trading actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised for market data but also bundles trading, cancellation, account query, transaction import, and bank/securities transfer material. <br>
Mitigation: Limit unattended use to read-only xtdata market-data tasks and require explicit human approval before any order, cancellation, account, transaction, or transfer action. <br>
Risk: Sample account or password patterns could be copied into executable code. <br>
Mitigation: Use placeholders and secure secret handling; never store real credentials in scripts, prompts, or generated examples. <br>


## Reference(s): <br>
- [ClawHub xtdata release](https://clawhub.ai/coderwpf/xtdata) <br>
- [XtData documentation](http://dict.thinktrader.net/nativeApi/xtdata.html) <br>
- [XtQuant getting started](http://dict.thinktrader.net/nativeApi/start_now.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include xtquant API examples, miniQMT setup notes, and read-only market-data workflow guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
