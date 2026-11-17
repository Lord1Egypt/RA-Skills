## Description:

Query AI-generated trading signals from vibetrading-datahub. Signals are produced by autonomous agents analyzing whale activity, news, funding rates, and technical indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhaonan00](https://clawhub.ai/user/liuhaonan00)

### License/Terms of Use:

ISC

## Use Case:

Developers, analysts, and trading workflow agents use this skill to fetch public crypto trading-signal summaries for selected symbols and signal types. The results support market monitoring and research, not automated trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto signal output may be incomplete, stale, or unsuitable as financial advice.

Mitigation: Treat results as informational, verify them independently, and apply separate risk management before making trading decisions.

Risk: The skill depends on public network access and npm dependencies.

Mitigation: Review or update dependencies and confirm access to vibetrading.dev before use in a sensitive environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuhaonan00/skills/vibetrading-global-signals)
- [VibeTrading API base](https://vibetrading.dev/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with Node.js command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public crypto signal data from vibetrading.dev and displays sentiment, timestamp, author, model, and analysis summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
