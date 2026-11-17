## Description:

TqSdk helps agents use the open-source Python futures and options trading SDK for market data, backtesting, simulated trading, and live trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to draft TqSdk setup steps, Python examples, API usage guidance, and trading workflow snippets for futures and options analysis. It is most appropriate for sandbox, simulated, or backtest work unless a human explicitly authorizes live-account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can place live trades or change positions through TqSdk APIs.

Mitigation: Use a sandbox, simulation, or backtest account by default, and require explicit user confirmation before generating or running calls to insert_order, cancel_order, TargetPosTask, or live-account APIs.

Risk: Trading account credentials may be exposed if users place passwords in prompts, source files, or logs.

Mitigation: Keep credentials in environment variables or a secrets manager, avoid echoing them in generated code or logs, and never ask the model to store production trading passwords.

Risk: Unreviewed dependency or package changes could alter trading behavior.

Mitigation: Pin and review dependencies before installation, and test generated code against simulated or historical data before any live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderwpf/skills/tqsdk)
- [TqSdk documentation](https://doc.shinnytech.com/tqsdk/latest/)
- [TqSdk GitHub repository](https://github.com/shinnytech/tqsdk-python)
- [ShinnyTech website](https://www.shinnytech.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference python3, tqsdk, pandas, and TQ_USERNAME/TQ_PASSWORD configuration.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
