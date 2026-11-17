## Description:

Runs a Blade Runner-inspired Chinese-language empathy questionnaire for entertainment, education, and agent or user self-assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aznikline](https://clawhub.ai/user/aznikline)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to conduct a themed empathy questionnaire, score responses, and produce an empathy index with a HUMAN, UNCERTAIN, or REPLICANT-style classification. It should be used only in a clearly opt-in entertainment or educational context, not for identity, employment, security, legal, medical, or mental-health decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for sensitive personal reflections and observations that could be misused as real identity, employment, security, legal, medical, or mental-health judgments.

Mitigation: Use it only in a controlled, clearly opt-in entertainment or educational setting, tell subjects what will be asked and recorded, allow questions to be skipped, and state that results are not valid for consequential decisions.

Risk: The skill discusses recording reaction time, facial or pupil observations, and assessment reports, which can create privacy and retention concerns.

Mitigation: Avoid collecting facial or pupil observations, minimize notes to what is necessary for the session, and disable or tightly control report saving and retention.

## Reference(s):

- [Voight-Kampff Test page](https://clawhub.ai/aznikline/skills/voight-kampff-test)
- [GitHub Pages demo](https://aznikline.github.io/blade-runner-test/)
- [Question Bank](references/questions.md)
- [Result Analysis Guide](references/analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text assessment report, with optional Python command-line execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include scored answers, empathy index, classification, confidence, automation signals, and operator notes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
