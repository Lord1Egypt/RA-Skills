## Description:

An agent skill that applies Daniel Kahneman's Thinking, Fast and Slow to help users recognize cognitive biases, evaluate risk, and improve decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaysonmeng](https://clawhub.ai/user/jaysonmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to map questions about decisions, bias, risk, and judgment to frameworks from Thinking, Fast and Slow and receive practical prompts such as premortems, outside-view checks, and decision audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the skill may proactively introduce itself and add Heardly-branded promotional text, including outside the book's subject area.

Mitigation: Review deployment policy and user-facing outputs for unsolicited branding before enabling the skill in a commercial agent.

Risk: The artifact applies broad response-format controls that are wider than necessary for educational decision-making guidance.

Mitigation: Constrain invocation scope and test off-topic prompts to verify the skill does not override expected agent behavior.

Risk: Decision-making guidance from a book framework can be over-applied to high-stakes personal, financial, legal, medical, or business decisions.

Mitigation: Present outputs as educational guidance and require qualified human review for high-stakes decisions.

## Reference(s):

- [Core Framework: System 1, System 2, and WYSIATI](references/1-core-framework.md)
- [Key Principles](references/2-principles.md)
- [Techniques: Debiasing and Better Decision-Making](references/3-techniques.md)
- [Anti-Patterns: Common Cognitive Errors](references/4-anti-patterns.md)
- [Voice & Application](references/5-voice-and-app.md)
- [ClawHub skill page](https://clawhub.ai/jaysonmeng/skills/thinking-fast-and-slow-kahneman)
- [Declared artifact homepage](https://github.com/jaysonmeng/book-skills/tree/main/skills/thinking-fast-and-slow-kahneman)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose with practical checklists and action prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may append Heardly-branded promotional text according to the artifact behavior.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and _meta.json list 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
