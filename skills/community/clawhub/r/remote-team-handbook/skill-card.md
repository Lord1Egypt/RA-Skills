## Description:

Drafts remote work handbook sections for US distributed teams, with FLSA, leave, state and accessibility items flagged for HR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US HR managers and operations leads use the skill to draft remote and hybrid work handbook sections for distributed teams. It flags federal and state-dependent issues for HR or counsel to review.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The documented YAML brief and CSV-based renderer may not work together as described, which could result in incomplete drafts.

Mitigation: Resolve and test the input-format mismatch with trusted sample data, and write to a fresh output folder.

Risk: State-specific employment rules and handbook drafts may be treated as final or universally applicable policy.

Mitigation: Keep state-dependent items open for review and have HR or counsel confirm the draft for each work state before adoption.

Risk: The optional, separately downloaded Windows app is unsigned and outside the bundled workflow review.

Mitigation: The handbook workflow does not require the app; if used separately, verify its download as documented and avoid elevated privileges without a specific need.

## Reference(s):

- [US remote work rules and state variation](references/remote-work-us-rules.md)
- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/remote-team-handbook)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Remote-work handbook section drafts with state-specific open items and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts require HR or counsel review before adoption.]

## Skill Version(s):

1.0.6 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
