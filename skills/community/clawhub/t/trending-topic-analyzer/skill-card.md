## Description:

Trending Topic Analyzer generates Chinese-language markdown reports for a supplied topic, including simulated multi-platform trend metrics, key viewpoints, sentiment, spread-path predictions, competitor comparison, and action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nh5gntnf78-oss](https://clawhub.ai/user/nh5gntnf78-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent generate a topic trend analysis report and optional competitor comparison for content planning. The bundled script currently produces simulated report data rather than verified live platform analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated report may be mistaken for live social-platform analytics even though the bundled script uses simulated metrics.

Mitigation: Label report outputs as simulated unless the implementation is connected to validated live data sources.

Risk: A user-supplied --output path may create or overwrite a local report file.

Mitigation: Run the script from an appropriate working directory and choose only output paths that are safe to create or replace.

Risk: Future extensions that add live APIs or crawlers could introduce platform compliance, rate-limit, privacy, and credential-handling obligations.

Mitigation: Review platform terms, crawler behavior, rate limits, privacy expectations, and API key storage before enabling live data collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nh5gntnf78-oss/skills/trending-topic-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report printed to stdout or written to a user-specified file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content is generated from simulated metrics unless the implementation is extended to real platform APIs or crawlers.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
