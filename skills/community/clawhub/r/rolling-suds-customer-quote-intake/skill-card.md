## Description:

Normalize messy Rolling Suds customer or salesperson inputs for exterior cleaning jobs into a clean intake summary, estimator-ready handoff, Workiz-friendly internal note, follow-up questions, and manual-review flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwdearing](https://clawhub.ai/user/mwdearing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and estimating staff use this skill to turn rough customer messages, call notes, photos plus notes, or address-only lead details into clean quote-intake output for Rolling Suds exterior cleaning work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer addresses and lead notes may contain sensitive business or personal information.

Mitigation: Use the skill only with quote-intake data appropriate for the intended Rolling Suds workflow and avoid adding unrelated sensitive details.

Risk: Incomplete lead details can make an estimator handoff unreliable.

Mitigation: Require the Lead number and address before an estimator-ready handoff, ask only the highest-value follow-up questions, and flag low-confidence scope for manual review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mwdearing/skills/rolling-suds-customer-quote-intake)
- [Skill homepage](https://github.com/mwdearing/rolling-suds-customer-quote-intake)
- [Default design](references/default-design.md)
- [Version history](references/version-history.md)
- [Iteration notes](references/iteration-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style structured text with labeled intake, handoff, Workiz note, follow-up, and manual-review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Lead number before estimator-ready handoff and keeps known facts separate from assumptions.]

## Skill Version(s):

0.1.10 (source: evidence.release.version and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
