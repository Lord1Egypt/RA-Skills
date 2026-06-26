## Description: <br>
Provides agent guidance and examples for using the XtQuant QMT Python SDK to access market data and trading interfaces for Chinese securities markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and quantitative trading engineers use this skill to get XtQuant setup guidance, market data examples, trading API examples, and QMT/miniQMT workflow references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes live trading, cancellation, account query, and bank-transfer patterns that can affect funded brokerage accounts. <br>
Mitigation: Keep usage read-only by default and require explicit user confirmation before any order, cancellation, transfer, or bank query. <br>
Risk: Brokerage credentials, bank passwords, or fund passwords could be exposed if supplied in prompts or source files. <br>
Mitigation: Do not provide bank or fund passwords in prompts or source files; use the broker client and approved local credential handling instead. <br>
Risk: Examples may interact with a live QMT or miniQMT client if run in a funded brokerage environment. <br>
Mitigation: Test against a simulated or non-live environment before connecting a funded brokerage account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coderwpf/xtquant) <br>
- [XtQuant official documentation](http://dict.thinktrader.net/nativeApi/start_now.html) <br>
- [ThinkTrader platform](http://www.thinktrader.net) <br>
- [XtQuant download page](http://dict.thinktrader.net/nativeApi/download_xtquant.html) <br>
- [BossQuant Bilibili profile](https://space.bilibili.com/48693330) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an installed xtquant package; live data and trading examples require a running QMT or miniQMT client with broker access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
