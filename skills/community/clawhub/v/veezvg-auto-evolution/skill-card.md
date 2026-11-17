## Description:

Build and maintain a self-evolving agent skill system that captures corrective feedback, graduates repeated feedback into rule proposals, improves low-performing skills, and proposes new skills for uncovered repeated patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezvg](https://clawhub.ai/user/veezvg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to add a controlled feedback loop that captures corrective user feedback, accumulates repeated issues, and presents rule, skill optimization, or new-skill proposals for confirmation before changes are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent feedback monitoring may persist corrective messages or surrounding context that users did not expect to store.

Mitigation: Configure explicit opt-in before recording, review and redact .claude/feedback regularly, and set retention and deletion rules.

Risk: Generated rule or skill-change proposals could introduce incorrect or misleading guidance if applied without review.

Mitigation: Keep CLAUDE.md and skill-file changes behind visible user confirmation and review proposed changes before deployment.

Risk: Feedback with unclear source attribution could be graduated into the wrong rule or skill.

Mitigation: Use source_skill metadata, keep uncertain sources as N/A, and manually verify the target before graduating feedback into formal rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veezvg/skills/veezvg-auto-evolution)
- [README](artifact/README.md)
- [Reference architecture](artifact/REFERENCE_ARCHITECTURE.md)
- [Examples](artifact/EXAMPLES.md)
- [Feedback signal detector](artifact/scripts/detect_feedback_signal.py)
- [Evolution runner](artifact/scripts/evolution_runner.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update structured feedback files and proposal summaries when connected to a project feedback directory.]

## Skill Version(s):

2.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
