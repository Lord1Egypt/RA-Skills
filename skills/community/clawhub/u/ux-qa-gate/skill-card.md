## Description:

Self-review gate for UI/UX work before delivering user-facing changes, covering functional completeness, usability heuristics, state handling, interaction quality, responsiveness, and severity classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michellebolander](https://clawhub.ai/user/michellebolander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill after frontend or user-facing work to check that UI flows work end-to-end, common states are handled, and usability issues are classified before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gate can add extra review steps after UI work.

Mitigation: Run it before delivery and keep the report brief unless a fuller UX review is requested.

Risk: Locale-related checklist findings may not match the product's intended audience.

Mitigation: Apply locale checks according to explicit product requirements or user preferences.

## Reference(s):

- [Nielsen's 10 Usability Heuristics - QA Checklist](references/heuristics-checklist.md)
- [Nielsen Norman Group: 10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown status summary with issue severity notes when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks the agent to keep the QA result brief unless the user requests a full heuristic report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
