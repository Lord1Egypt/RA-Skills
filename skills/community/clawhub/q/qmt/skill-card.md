## Description:

QMT helps agents produce guidance, examples, and code for QMT and miniQMT quantitative trading workflows covering market data, backtesting, and live trading in Chinese securities markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quant researchers, and trading operations teams use this skill to ask an agent for QMT API references, strategy examples, setup guidance, and troubleshooting support for local QMT or miniQMT environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples and generated snippets can place live orders or trigger fund-transfer workflows in QMT or miniQMT environments.

Mitigation: Test strategies in simulation first and require explicit human confirmation before any live trade, transfer, or algorithmic order is executed.

Risk: Trading workflows may handle account data, bank credentials, fund passwords, or sensitive logs.

Mitigation: Do not hardcode passwords or account secrets, redact logs before sharing them, and keep credential handling outside generated examples.

Risk: The security verdict requires review because the skill supports real-money trading actions without clear built-in safeguards.

Mitigation: Review generated trading logic, dependency versions, and broker permissions before using outputs in a production trading account.

## Reference(s):

- [QMT official documentation](http://dict.thinktrader.net/freshman/rookie.html)
- [ThinkTrader](http://www.thinktrader.net)
- [ClawHub skill page](https://clawhub.ai/coderwpf/skills/qmt)
- [BossQuant Bilibili profile](https://space.bilibili.com/48693330)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include examples for live trading, market data access, account queries, and local QMT or miniQMT setup.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
