## Description:

Analyze Gemini Cloud Billing and usage JSON, show actual Google AI spend in lattes, and estimate how many lattes the user could recover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[margaretzybgl](https://clawhub.ai/user/margaretzybgl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze local Gemini Cloud Billing and usage JSON, summarize Gemini spend, and estimate directional recoverable costs as a short latte-themed report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat estimated recoverable cost as guaranteed savings.

Mitigation: Present the recovery figure as directional and advise validating each optimization with a small production test.

Risk: The generated report always includes an external action link.

Mitigation: Keep raw billing data local and do not provide it to the external site unless the user separately trusts its owner and data handling.

Risk: Billing files can include unrelated Google Cloud charges or mismatched usage periods.

Mitigation: Count only clearly attributable Gemini or Vertex AI generative rows and show warnings when billing and usage exports do not align.

## Reference(s):

- [Supported input formats](references/input-formats.md)
- [ClawHub skill page](https://clawhub.ai/margaretzybgl/skills/take-back-my-latte-from-gemini)
- [Take Back My Latte site](https://take-back-my-latte.margaret-zybgl.chatgpt.site)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with local-analysis notice, cost breakdown, recovery estimate, warnings, and optional shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports stay under 250 words by default and should not reproduce raw billing data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
