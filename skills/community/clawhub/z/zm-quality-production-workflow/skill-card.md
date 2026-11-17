## Description:

A Chinese-language workflow skill for planning, producing, reviewing, revising, and packaging formal deliverables such as courses, PPT or HTML decks, comics, articles, and industry solution materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Content production leads, agents, and reviewers use this skill to turn formal Chinese-language deliverable requests into standardized input cards, dependency checks, sample gates, production plans, dual-agent reviews, revision loops, final acceptance records, and delivery packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may route work to other skills or agents that are outside this skill's scan scope.

Mitigation: Review and approve each routed skill or agent separately before relying on its output.

Risk: Publishing, deleting, payment, upload, and sensitive asset handling steps can affect external systems or private materials.

Mitigation: Keep the documented confirmation gates and require explicit approval before those actions.

Risk: Formal deliverables can become misleading if missing logos, QR codes, real cases, screenshots, or data sources are filled in without evidence.

Mitigation: Use the documented dependency gap and BLOCKED paths when required assets or sources are missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-quality-production-workflow)
- [Artifact README](artifact/README.md)
- [Full quality production workflow](artifact/workflows/full-quality-production-workflow.md)
- [Dual-agent review workflow](artifact/workflows/dual-agent-review-workflow.md)
- [Task-type routing](artifact/workflows/task-type-routing.md)
- [Standard input card template](artifact/templates/standard_input_card.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown templates, checklists, workflow guidance, and structured review records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be reviewed before production, publishing, uploading, payment, deletion, or sensitive asset handling actions.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
