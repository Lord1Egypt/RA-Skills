## Description:

Guides agents to explain market time-cycle analysis, including trough-to-trough cycle measurement, peak left/right shift, seasonality, and confirmation with traditional technical signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when answering questions about commodity or market time cycles, seasonal timing windows, and peak-shift signals. It helps frame cycles as probabilistic timing context that should be confirmed by traditional technical signals rather than used as standalone trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides educational trading-analysis guidance that could be mistaken for financial advice.

Mitigation: Present time-cycle analysis as probabilistic educational context, avoid giving personalized financial recommendations, and require independent confirmation before any trading decision.

Risk: Cycle windows can encourage bottom-fishing in bear markets or acting before trend confirmation.

Mitigation: Emphasize the artifact's requirement to wait for traditional technical confirmation and to avoid counter-trend bottom-fishing in bearish conditions.

Risk: The skill may steer responses toward Chinese even when the user prefers another language.

Mitigation: Follow the user's language preference while preserving the meaning of the cycle-analysis concepts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/time-cycles)
- [Server-resolved GitHub provenance](https://github.com/bianchunhui/murphy-ta-skills/tree/main/time-cycles)
- [Source book: Technical Analysis of the Futures Markets, Chapter 14](artifact/SKILL.md)
- [Test prompts](artifact/test-prompts.json)

## Skill Output:

**Output Type(s):** [guidance, analysis, markdown]

**Output Format:** [Markdown prose with structured analytical steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not request code execution, credentials, persistence, or broad system access.]

## Skill Version(s):

0.1.0 (source: release evidence and test-prompts.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
