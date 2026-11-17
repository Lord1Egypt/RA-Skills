## Description:

Quantitative market-analysis skill for BTC, XAUUSD, and other supported assets that runs Signalbot to compute technical indicators and produce structured JSON reports for market commentary or trade-posture guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanhuhai5739](https://clawhub.ai/user/shanhuhai5739)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for crypto and gold market analysis, multi-timeframe technical indicator reports, support and resistance levels, and concise Chinese market summaries or posts. The agent may run the Signalbot binary to collect JSON analysis before composing human-facing commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update an unpinned third-party Signalbot binary before analysis.

Mitigation: Install a pinned, verified release yourself and avoid automatic @latest updates.

Risk: Scheduled analysis jobs can repeatedly run market analysis or generate posts without interactive review.

Mitigation: Review cron jobs before enabling them and require human review before publishing generated market posts.

Risk: Market indicators and generated trade-posture guidance can be incomplete or misleading.

Mitigation: Use outputs as informational analysis, verify market data independently, and do not rely on the skill as the sole basis for financial decisions.

## Reference(s):

- [Signalbot GitHub repository](https://github.com/shanhuhai5739/signalbot)
- [Signalbot ClawHub skill page](https://clawhub.ai/shanhuhai5739/skills/signalbot)
- [OpenClaw usage guide](artifact/OPENCLAW_USAGE.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON reports plus Chinese text or Markdown market summaries, with shell commands and configuration snippets when setup or scheduled analysis is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signalbot writes JSON to stdout or an optional output file; the skill also includes prompt templates for periodic OpenClaw cron analysis.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
