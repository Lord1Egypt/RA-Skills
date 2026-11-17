## Description:

Read a source through the lens of a specific problem. Produces an applied playbook, not a summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjhenriksen](https://clawhub.ai/user/jjjhenriksen)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, researchers, and professionals use the skill to apply a source to a defined strategic question and produce an actionable, source-traced playbook. It requires both source text and a specific problem or question.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may overstate what a source passage supports or blur source claims with proposed applications.

Mitigation: Give each recommendation a precise passage locator, a scoped source claim, a separately labeled applied inference, and assumptions or checks; label unsupported ideas as hypotheses.

Risk: The resulting playbook may be generic or disconnected from the user's decision.

Mitigation: Require a specific strategic problem before reading and connect each recommendation to a relevant source passage.

## Reference(s):

- [Strategic Reading release page](https://clawhub.ai/jjjhenriksen/skills/strategic-reading)
- [Traceable example](artifact/references/traceable-example.md)
- [Fictional source fixture](artifact/references/fictional-source.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown applied-reading playbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each recommendation has a source passage locator, source claim, separately labeled applied inference, and assumptions or limits.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
