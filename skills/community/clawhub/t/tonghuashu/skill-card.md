## Description:

操作同花顺炒股软件，覆盖盯盘、选股、自选、下单前检查、复盘等个人炒股全流程

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimuoo](https://clawhub.ai/user/zimuoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide an agent through Tonghuashun personal trading workflows, including market monitoring, watchlist review, pre-order checks, risk calculation, and trade journaling. The skill is intended to assist navigation and preparation while keeping final trading confirmation under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send keystrokes to a real trading client, including opening order-entry screens.

Mitigation: Use test or observation-only workflows first, watch the screen during any live-account session, and require manual confirmation before any F12 or order-entry step.

Risk: Trading workflow logs and journal files may contain sensitive trading history.

Mitigation: Periodically delete or protect generated files under scripts/logs and avoid storing sensitive account details in notes.

Risk: Automated GUI actions can affect the wrong window or state if Tonghuashun is not ready.

Mitigation: Run actions step by step, confirm the active window and visible result before continuing, and fall back to manual shortcuts if automation is unreliable.

## Reference(s):

- [Tonghuashun Homepage](https://www.10jqka.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local trading workflow logs and JSONL journal records under scripts/logs when the bundled scripts are run.]

## Skill Version(s):

1.0.2 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
