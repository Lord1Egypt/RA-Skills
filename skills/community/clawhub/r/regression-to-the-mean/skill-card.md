## Description:

Applies a statistical framework for assessing whether performance changes after extreme results reflect regression to the mean or an intervention effect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and managers use the framework to assess whether a change after an extreme performance result reflects regression to the mean or a genuine intervention effect. It guides comparisons against controls or baseline expectations and helps calibrate causal claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regression estimates may be mistaken for proof that an intervention caused a performance change.

Mitigation: Treat conclusions as estimates and compare against a control group or baseline before assigning causal credit or blame.

Risk: Real-use examples could contain confidential details.

Mitigation: Omit confidential details when recording examples.

## Reference(s):

- [Sources](artifact/references/sources.md)
- [NLP Evaluation in Trouble: On the Need to Measure LLM Data Contamination for each Benchmark](https://aclanthology.org/2023.findings-emnlp.722/)
- [Chatbot Arena Leaderboard](https://lmarena.ai/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown regression analysis with causal calibration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the observations and control or baseline data provided by the user.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
