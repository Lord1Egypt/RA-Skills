## Description:

Checks copied safety-training record tables and sign-in sheets for six declared issues: hours reconciliation, annual refresher hours, roster coverage, duplicate entries, exam score versus pass line, and blank or malformed fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Safety and training administrators at manufacturing, construction, property-management, and hazardous-chemical organizations use this skill to reconcile monthly training logs, onboarding records, and pre-inspection records against sign-ins, hours, rosters, and exam scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may overread table reconciliation results as proof that training occurred or as a legal compliance determination.

Mitigation: Treat the output as deterministic table checking only; review source records, local rules, and responsible safety judgments before acting.

Risk: The free edition explicitly does not run several checks, including full three-level education completeness, special-operation certificate validity, role-topic matching, attendance-time conflicts, and consolidated remediation summaries.

Mitigation: Confirm checks not run separately when those items matter for the review.

Risk: Security guidance notes that one duplicate-record summary sentence is imprecise.

Mitigation: Review duplicate-record conclusions against the detailed row-level messages before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/safety-training-record-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON containing findings, summaries, missing-input messages, executed-scope details, and checks not run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires copied table text with recognizable Chinese safety-training headers; the wrapper rejects inputs over 4 MB.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
