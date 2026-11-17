## Description:

Analyze Terms of Service documents for completeness and fairness. Use when checking ToS sections, detecting unfair clauses, generating TL;DR summaries, scoring user-friendliness, or comparing two versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and external users can use this skill to inspect Terms of Service text for expected sections, potentially unfair clauses, plain-language summaries, fairness scoring, and version-to-version changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic Terms of Service analysis may produce incomplete, incorrect, or overly broad findings and is not legal advice.

Mitigation: Review outputs against the full source terms and consult qualified legal counsel before relying on the results.

Risk: The skill may over-activate on broad phrases such as service agreement.

Mitigation: Confirm that the input document is the intended Terms of Service material before treating the output as relevant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/terms-checker)
- [ClawHub publisher profile](https://clawhub.ai/user/loutai0307-prog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text reports with command examples, summary text, scoring output, and unified diff output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local user-provided Terms of Service text files and prints heuristic results without network access or persistence according to security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
