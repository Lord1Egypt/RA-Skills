## Description:

Conducts adversarial analysis by decomposing claims and using multiple expert perspectives to produce steelman arguments, counterarguments, and synthesized recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kipasdinding6969-alt](https://clawhub.ai/user/kipasdinding6969-alt)

### License/Terms of Use:


## Use Case:

Developers, reviewers, and decision makers use this skill to stress-test arguments, architecture choices, feature specifications, code review positions, or strategic plans before relying on them. It is suited to producing balanced critique, stronger formulations of an argument, and final recommendations refined through adversarial review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill can load unreviewed home-directory customization files that override reviewed instructions.

Mitigation: Review, disable, or remove those local customization files unless the operator intentionally maintains and trusts them.

Risk: The security summary says the skill automatically sends a local HTTP notification to port 8888 when invoked.

Mitigation: Disable or remove the notification behavior unless the operator intentionally runs and trusts that local notification service.

Risk: The security guidance flags broad red-team activation as a behavior to review before installation.

Mitigation: Use the skill only for intentional adversarial review and have a human review outputs before acting on high-impact recommendations.

## Reference(s):

- [Skill definition](artifact/SKILL.md)
- [Red Team Philosophy](artifact/Philosophy.md)
- [Red Team Integration Guide](artifact/Integration.md)
- [Adversarial Validation Pattern](artifact/Workflows/AdversarialValidation.md)
- [Red Team Parallel Analysis Workflow](artifact/Workflows/ParallelAnalysis.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown analysis with numbered sections, concise critique points, and optional shell command snippets for local notifications.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parallel analysis produces steelman and counterargument sections; adversarial validation produces proposal summaries, critique points, and a synthesized recommendation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
