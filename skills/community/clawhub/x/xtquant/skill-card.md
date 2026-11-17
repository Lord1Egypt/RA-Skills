## Description:

XtQuant QMT Python SDK guidance for market data and trading APIs across Chinese securities markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading practitioners use this skill to generate XtQuant/QMT setup guidance, Python examples, API usage notes, and operational cautions for market data retrieval and brokerage trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for a real brokerage trading SDK that can place orders or transfer funds.

Mitigation: Use it only in a controlled XtQuant/QMT environment, prefer paper or test accounts first, and add explicit confirmations and limits before order or transfer calls.

Risk: Examples may expose account data or credentials if copied directly into scripts or logs.

Mitigation: Never hardcode bank or fund passwords, redact account data from logs, and review generated code before execution.

Risk: Unpinned dependencies can change runtime behavior.

Mitigation: Pin dependencies in the consuming project's lockfile before deployment.

## Reference(s):

- [ClawHub xtquant Skill Page](https://clawhub.ai/coderwpf/skills/xtquant)
- [XtQuant Official Documentation](http://dict.thinktrader.net/nativeApi/start_now.html)
- [ThinkTrader QMT Platform](http://www.thinktrader.net)
- [XtQuant Download Page](http://dict.thinktrader.net/nativeApi/download_xtquant.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading, transfer, account-query, market-data, and dependency-installation examples that require user review before execution.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
