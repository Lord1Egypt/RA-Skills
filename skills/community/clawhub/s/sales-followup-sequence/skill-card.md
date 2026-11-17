## Description:

Builds a dated follow-up plan for U.S. sales reps managing an active deal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

U.S. account executives and sales managers use the skill to draft and review a follow-up cadence for an active deal, including touch purposes, stop conditions, and rep actions.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The generated calendar is a draft and may not include the detailed touch schedule or message content needed for outreach.

Mitigation: Manually complete and verify dates, channels, and message text before each person-reviewed touch; do not auto-send.

Risk: Running the script replaces an existing `plan.md` in the chosen output folder.

Mitigation: Choose a dedicated output folder and preserve any existing plan before running the script.

Risk: The optional Windows application is a separate download whose safety is not established by this skill's clean verdict.

Mitigation: Review the application separately and only download or run it if you accept the risks described by the publisher.

## Reference(s):

- [Follow-up cadence reference](references/follow-up-cadence.md)
- [Publisher homepage](https://github.com/rapidworker1)
- [Optional Windows toolkit repository (review separately)](https://github.com/rapidworker1/Multiple-AI-models-Toolkit)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Local Markdown plan file (`plan.md`)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes a 21-day weekly calendar and guardrails; manually add and verify actual dates, channels, touch copy, and other deal-specific details before outreach. Use a dedicated output folder because an existing `plan.md` is replaced.]

## Skill Version(s):

1.0.7 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
