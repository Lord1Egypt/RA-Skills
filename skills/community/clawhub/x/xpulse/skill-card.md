## Description:

Xpulse scans X/Twitter search results with DuckDuckGo and local Qwen filtering to surface prediction-market signals relevant to a user's active Kalshi positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

External prediction-market traders use Xpulse to monitor configured social topics, filter repeated or low-materiality signals, and alert only when a signal appears relevant to active Kalshi positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kalshi credentials and private position data may be read even when the documented position gate is disabled.

Mitigation: Review or patch position_gate behavior before installing if you plan to run without Kalshi position matching.

Risk: Local cache, history, debug logs, and Kalshi key paths can expose sensitive trading context.

Mitigation: Restrict access to local state and logs, treat them as sensitive data, and clear cached state when it is no longer needed.

Risk: The optional bulk stack install may install additional skills outside this card's review scope.

Mitigation: Install only Xpulse unless the companion skills have been reviewed separately.

## Reference(s):

- [Xpulse ClawHub listing](https://clawhub.ai/kingmadellc/skills/xpulse)
- [Materiality Gate](references/materiality-gate.md)
- [Position Matching](references/position-matching.md)
- [Ollama](https://ollama.ai)
- [Kalshi](https://kalshi.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text alerts and JSON cache/history records, with Markdown documentation and shell/configuration snippets for setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts are limited to the highest-confidence position-matched signals per run; detected signals may also be cached locally for later review.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
