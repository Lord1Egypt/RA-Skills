## Description:

Turn client conversation notes into a Markdown follow-up plan that separates customer needs, open issues, each party's commitments, next actions with owners and timing, and risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, account management, and customer success users use this skill to convert meeting transcripts, chat excerpts, or visit notes into an actionable client follow-up plan. It is intended for text supplied by the user and emphasizes separating our commitments from customer commitments, identifying unresolved items, and listing follow-up questions without inventing missing details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be invoked by broad meeting-organization phrases and may be applied to non-client conversations.

Mitigation: Confirm the source text is client-related before relying on the generated follow-up plan.

Risk: Follow-up plans may contain inferred stages, implicit concerns, or missing time points when the input notes are incomplete.

Mitigation: Review inferred items, keep unknowns in the follow-up question list, and avoid treating inferred statements as confirmed customer commitments.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-client-followup-plan)
- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-client-followup-plan)
- [Info separation rules](artifact/references/info-separation-rules.md)
- [Risk signals](artifact/references/risk-signals.md)
- [Follow-up plan template](artifact/templates/followup-plan-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown follow-up plan with tables and bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seven-section client follow-up structure covering overview, needs, commitments, open issues, plan, risks, and follow-up questions.]

## Skill Version(s):

0.1.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
