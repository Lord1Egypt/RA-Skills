## Description:

Scores and explains nine psychology scales covering mood, stress, sleep, trauma, personality, and motivation, including reverse scoring, standard-score conversion, severity labels, plain-language interpretation, and a non-diagnostic disclaimer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxw-wwwww](https://clawhub.ai/user/zxw-wwwww)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, and researchers use this skill to calculate questionnaire scores for supported psychological scales and receive structured, educational explanations. It is not a clinical diagnostic tool and should not be used for urgent or formal mental-health decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mental-health scoring and crisis-adjacent guidance may be mistaken for diagnosis or treatment advice.

Mitigation: Keep outputs educational and non-diagnostic, avoid medication recommendations, and direct users to qualified professionals for clinical decisions.

Risk: Under-specified scale names, incomplete answers, or incorrect scoring rules could produce misleading results.

Mitigation: Require an explicit supported scale and complete response set before scoring, stop on answer-count mismatches, and verify scoring rules against authoritative references before relying on results.

Risk: Self-harm or suicide-risk signals require urgent support beyond automated scoring.

Mitigation: Pause score interpretation when urgent-risk signals appear and direct users to local emergency services, crisis resources, or qualified professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxw-wwwww/skills/psych-scale-scorer)
- [Artifact README](artifact/README1.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Structured Markdown with scale name, raw score, standard score when applicable, severity label, plain-language explanation, and disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational self-assessment output; no tools, API calls, shell commands, or configuration changes are produced.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and README list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
