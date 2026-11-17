## Description:

Generates and updates structured world bibles for Vietnamese text stories, maintaining lore modules, cross-references, hooks, gap analysis, and character state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaibazax-dev](https://clawhub.ai/user/kaibazax-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and writing agents use this skill to build an initial lorebook from a story premise or update an existing lorebook after 5-10 outline chapters. It is intended for Vietnamese text-based story planning, not for drafting prose or scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated lorebook updates may add or promote creative canon details that the user did not intend.

Mitigation: Review generated canon, hooks, and character-state updates before treating the lorebook as the source of truth.

Risk: Long structured Markdown outputs may become hard to audit if the premise, scope, or outline delta is vague.

Mitigation: Provide a clear premise for Build Mode or concrete chapter deltas for Update Mode, then check the gap analysis and hook registry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaibazax-dev/skills/vn-worldbuilding)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown lorebook or lorebook update]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Build Mode produces long cross-referenced world bibles; Update Mode incorporates outline deltas and updates hooks, gap analysis, and character state.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
