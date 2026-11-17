## Description:

Ptrade 恒生量化交易平台 - 策略运行在券商服务器上，低延迟执行，支持A股、期货、融资融券等中国证券市场。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading practitioners use this skill as a Ptrade API reference for writing, reviewing, and adapting Python strategies for Chinese equities, futures, margin trading, ETF workflows, and broker-hosted backtests or live trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples may place live broker-backed trading orders or alter positions if run in a live Ptrade account.

Mitigation: Use paper trading or backtests first, add explicit account-mode checks, and enforce position limits before live deployment.

Risk: Persistence examples use pickle, which can be unsafe for untrusted or corrupted files.

Mitigation: Use safer validated formats such as JSON for persisted state, or strictly control and validate any files loaded by strategy code.

Risk: Demo dependencies may be installed without pinned versions.

Mitigation: Install demo dependencies only in an isolated environment with pinned package versions.

## Reference(s):

- [ClawHub Ptrade Skill](https://clawhub.ai/coderwpf/skills/ptrade)
- [Ptrade Documentation](https://ptradeapi.com)
- [QMT API Documentation](http://qmt.ptradeapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API usage notes, trading strategy examples, environment constraints, and broker-platform guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
