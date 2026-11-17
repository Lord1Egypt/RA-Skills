## Description:

Sandbox Simulator coordinates Chinese-language, multi-character social roleplay simulations with parallel session scheduling, Markdown state files, and user intervention controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonhu](https://clawhub.ai/user/jasonhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up and run roleplay-style sandbox simulations with multiple characters, persistent scenario state, and interactive interventions such as pause, resume, state edits, and event injection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulation runs can create or update local Markdown scenario state.

Mitigation: Use a dedicated workspace or scenario folder and review changed character, world-state, and history files before reuse.

Risk: Natural-language interventions may be interpreted as state mutations or injected events.

Mitigation: Prefer explicit /sandbox commands for mutations and check scenario status after interventions.

Risk: Future external API extensions could change the skill's security profile.

Mitigation: Review security findings and requested integrations before enabling any external API extension.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonhu/skills/sandbox-simulator)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-formatted status panels, dialogue logs, event summaries, and local scenario state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State is represented in Markdown character files, world-state files, and per-round history files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
