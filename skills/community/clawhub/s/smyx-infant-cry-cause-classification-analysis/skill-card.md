## Description:

Analyzes infant cry audio to estimate possible causes such as hunger, sleepiness, discomfort, or need for comfort, and returns a confidence-ranked result with care suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and childcare teams can use the skill to review infant cry audio and receive a possible cause, confidence estimate, and directional soothing suggestions. It can also retrieve prior analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags account and identity handling and remote media processing, which may involve sensitive infant recordings.

Mitigation: Review account setup and remote-media handling; submit recordings only with guardian consent and suitable privacy safeguards.

Risk: The security summary reports behavior that may not clearly match the advertised cry-analysis purpose.

Mitigation: Check that the installed behavior and returned results match the intended task before relying on them.

Risk: Cry-cause estimates could be mistaken for medical diagnosis or clinical advice.

Mitigation: Treat results as parenting reference only; seek professional care for persistent or unusual crying.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-infant-cry-cause-classification-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis results and Markdown report tables for history queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence estimates, secondary cause probabilities, suggestions, and report links.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
