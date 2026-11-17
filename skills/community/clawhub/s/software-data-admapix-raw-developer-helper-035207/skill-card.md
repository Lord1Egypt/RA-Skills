## Description:

Helps agent users and skill maintainers adapt AdMapix-style software-and-data workflows into practical bug-fix, setup-hardening, reliability, and adjacent-skill guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and teams use this skill to produce practical artifacts for AdMapix-style software and data workflows. Typical outputs support debugging, setup hardening, reliability improvements, and adjacent skill design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overly broad activation wording may select the skill for unrelated requests that mention common words such as data or raw.

Mitigation: Confirm the user wants an AdMapix-style workflow helper and narrow trigger phrases before release or installation.

Risk: Workflow guidance can produce incorrect or incomplete implementation advice if the user's constraints are underspecified.

Mitigation: Restate the desired outcome, constraints, inputs, and success criteria before producing code, commands, or configuration changes.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [AdMapix ClawHub Skill](https://clawhub.ai/skills/admapix)
- [Ontology ClawHub Skill](https://clawhub.ai/skills/ontology)
- [Agent Browser ClawHub Skill](https://clawhub.ai/skills/agent-browser-clawdbot)
- [What is the current data language?](https://news.ycombinator.com/item?id=48742811)
- [Context layer discussion](https://news.ycombinator.com/item?id=48745664)
- [How to Implement a DevLake plugin?](https://segmentfault.com/a/1190000042069896)
- [MySQL raw data question](https://segmentfault.com/q/1010000012550302)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with checklists, analysis, implementation notes, and optional command or code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, verification notes, and follow-up risks.]

## Skill Version(s):

0.20260702.35207 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
