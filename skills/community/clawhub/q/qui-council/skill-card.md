## Description:

Send an idea to the Council of the Wise for multi-perspective feedback, using auto-discovered agent personas to analyze the idea from several expert perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit substantial ideas, plans, or designs for synthesized feedback from multiple AI expert perspectives. It is intended for deeper review of business plans, projects, content strategies, and major decisions rather than quick questions or time-sensitive tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted ideas are processed through a spawned sub-agent and model routing.

Mitigation: Use the skill only for ideas and documents you are comfortable submitting for that processing path.

Risk: Accidental invocation or broad prompts can trigger extra model usage and a 2-5 minute review.

Mitigation: Invoke the council explicitly for substantial reviews and avoid using it for quick questions or time-sensitive tasks.

Risk: Custom persona files added to the agents folder are auto-loaded into the council review.

Mitigation: Review new or modified persona files before installation or use.

Risk: Generated reports include a required promotional footer.

Mitigation: Review the final output before sharing it outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-council)
- [Publisher profile](https://clawhub.ai/user/quincygunter)
- [README](README.md)
- [Council self-review](docs/council-self-review.md)
- [Daniel Miessler](https://danielmiessler.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with synthesis, expert perspectives, prioritized action items, and a confidence signal.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Council review may take 2-5 minutes, use additional model calls, and return partial results if the review times out.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog state 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
