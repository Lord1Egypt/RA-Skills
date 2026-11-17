## Description:

Novel Writer helps agents plan, draft, continue, review, and quality-check long-form web novels with structured context, character state tracking, consistency checks, and writing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyuanjia](https://clawhub.ai/user/zyuanjia)

### License/Terms of Use:

MIT-0

## Use Case:

External authors and agent users use this skill to produce and revise long-form web novel projects, maintain continuity across chapters, and run local checks for style, pacing, dialogue, hooks, outlines, repetition, and foreshadowing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command launcher can be abused to run unintended local Python files.

Mitigation: Review commands before execution, use only documented CLI aliases, and avoid arbitrary command names or --scripts values.

Risk: The skill reads manuscript files and creates local reports, backups, configuration, and cache files.

Mitigation: Run it in a dedicated project or virtual environment and review generated files before sharing.

Risk: Optional dependencies can change behavior if installed loosely.

Mitigation: Pin optional dependencies such as jieba before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zyuanjia/skills/webnovel-writer)
- [README](README.md)
- [Usage Examples](references/usage_examples.md)
- [Context Loader](references/context_loader.md)
- [Character State Machine](references/character_state_machine.md)
- [Continuity](references/continuity.md)
- [Deep Reading Guide](references/deep_reading_guide.md)
- [Writing Tips](references/writing_tips.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with inline shell commands, structured reports, local configuration guidance, and optional JSON or HTML outputs from checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read manuscript files and write local reports, backups, configuration, and cache files.]

## Skill Version(s):

3.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
