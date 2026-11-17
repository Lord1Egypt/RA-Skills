## Description:

Runs a calibration report on a Simmer trade journal, breaking win rate and expected value down by strategy, time of day, price band, day of week, and market type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Simmer JSONL trading journals and identify where trading performance is strongest or weakest. It supports sim or live journal files and reports analytics only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill asks for a trading API key that is not needed for its local analytics behavior.

Mitigation: Install only when comfortable providing SIMMER_API_KEY; avoid live credentials unless the skill is revised to require them.

Risk: The security summary says the skill can read live journal data unexpectedly.

Mitigation: Set CALIB_JOURNAL_PATH explicitly to the intended JSONL journal and review the selected path before scheduled runs.

Risk: The security guidance recommends dependency review for simmer-sdk.

Mitigation: Use a pinned trusted simmer-sdk version before enabling scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djdyll/skills/simmer-calibration-report)
- [ClawHub publisher profile](https://clawhub.ai/user/djdyll)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain-text console report with optional JSON automaton summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable by environment variables for journal path, minimum trades, lookback window, and unresolved-trade inclusion.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
