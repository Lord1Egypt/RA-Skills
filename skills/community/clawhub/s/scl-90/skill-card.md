## Description:

SCL-90 provides a Chinese-language Symptom Checklist 90 self-assessment with 90 questions, China norm data, score summaries, history lookup, and crisis-resource guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga)

### License/Terms of Use:

MIT-0

## Use Case:

External users can run the skill for SCL-90 self-screening, factor explanations, norm lookup, saved assessment history, and crisis-resource lookup. The results are for personal reference and monitoring, not professional diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive mental-health responses and saves full assessment answers in plaintext under $HOME/.scl90_history.

Mitigation: Use it only where local plaintext retention is acceptable, protect the device account, and delete saved history when it is no longer needed.

Risk: The release presents psychological assessment features, while evidence.security says it should be treated as a Chinese-language demo or reference tool rather than a clinical assessment.

Mitigation: Keep the skill framed as self-screening and personal monitoring, and direct users to qualified professionals or crisis resources for diagnosis, treatment, or urgent support.

Risk: Artifact behavior shows the full factor analysis and quick screening are incomplete or marked as in development.

Mitigation: Do not rely on incomplete scoring features for decisions; review outputs and use the full 90-question results only as preliminary reference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuqingsonga/skills/scl-90)
- [ClawHub publisher profile](https://clawhub.ai/user/zhuqingsonga)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text terminal output with command examples and saved text result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assessment results may be saved locally under $HOME/.scl90_history.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
