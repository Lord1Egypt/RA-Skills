## Description:

Self-Eval helps agents evaluate their own outputs with reproducible rubric scoring, optional reference comparison, JSON score reports, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Self-Eval to grade candidate or final responses against configurable rubrics, compare against optional references, and decide whether to revise before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning behavior can retain local usage history, error notes, and preferences.

Mitigation: Review the learning helper before installation and avoid recording sensitive details in notes or preferences.

Risk: The learning helper can write data into arbitrary skill directories when directed there.

Mitigation: Constrain use to this skill's own directory or avoid the learning helper in environments with multiple installed skills.

Risk: Heuristic rubric scoring can miss factual or task-specific quality issues.

Mitigation: Use score reports as review aids and require human or reference-based validation for high-impact outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/self-eval)
- [ClawHub publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON reports and Markdown or text guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update learned_patterns.json when the learning helper is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
