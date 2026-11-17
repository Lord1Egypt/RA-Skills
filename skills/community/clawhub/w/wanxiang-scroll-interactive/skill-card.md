## Description:

Wanxiang Scroll Interactive helps agents run interactive story modes, turn-based life simulation, and guided long-form writing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandanllab](https://clawhub.ai/user/dandanllab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through interactive fiction, life-simulation gameplay, character and world state updates, and structured story or essay generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses hash-prefixed commands and claims high-priority command behavior, which could blur instruction boundaries.

Mitigation: Treat these commands as skill-local story controls and keep higher-priority system, developer, and user instructions authoritative.

Risk: The skill asks users to install an unpinned companion package, so behavior may vary with the companion package version.

Mitigation: Pin or verify the companion package before use, especially in workflows that require stable output formats.

Risk: Interactive story and life-simulation features may convert personal details into story state or generated prose.

Mitigation: Avoid entering sensitive personal information unless users are comfortable with it being represented in narrative state or text.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dandanllab/skills/wanxiang-scroll-interactive)
- [Third chapter: interactive story](references/index.md)
- [Interactive story quick start](references/01-quick-start.md)
- [Core protocols](references/02-core-protocols.md)
- [Li Dan seven-step writing framework](references/chapter-13-lidan-writing/index.md)
- [Cognitive bias writing example](references/chapter-13-lidan-writing/cognitive-bias-demo.md)
- [Life simulation overview](references/chapter-14-life-simulation/index.md)
- [World generation rules](references/chapter-14-life-simulation/01-world-gen.md)
- [Character and attribute system](references/chapter-14-life-simulation/02-character.md)
- [Event system](references/chapter-14-life-simulation/03-event-system.md)
- [Action points and free action](references/chapter-14-life-simulation/04-action.md)
- [Time and death system](references/chapter-14-life-simulation/05-time-system.md)
- [Legacy system](references/chapter-14-life-simulation/06-legacy.md)
- [Background novel generation](references/chapter-14-life-simulation/07-novel-gen.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style narrative text with command examples, status blocks, tables, and structured game or story guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is documentation-driven and intended to be used alongside the main wanxiang-scroll package.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
