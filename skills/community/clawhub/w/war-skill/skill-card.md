## Description:

Delivers and maintains Kitchen War RTS, a self-contained HTML5 Canvas real-time strategy game in the style of Red Alert with base building, resource harvesting, unit production, a tech tree, fog of war, enemy AI, a superweapon, and browser-based verification scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmily741963](https://clawhub.ai/user/hmily741963)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to deliver, extend, fix, or re-verify a playable browser RTS game with Red Alert-style mechanics and a kitchen-war theme.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The game stores minor progress and preference data in browser localStorage.

Mitigation: Tell users that progress and preferences are local to the browser and can be reset by clearing site data if needed.

Risk: Optional verification scripts launch a local Playwright browser against the bundled HTML game.

Mitigation: Run verification scripts only from a trusted local workspace after edits, and review environment-specific browser and Node paths before execution.

Risk: The game UI is Chinese-only.

Mitigation: Review localization needs before publishing to audiences that require another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmily741963/skills/war-skill)
- [hmily741963 publisher profile](https://clawhub.ai/user/hmily741963)
- [Kitchen War RTS verification methodology](references/testing.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown guidance with file paths and shell command blocks; the bundled game output is a self-contained HTML file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces or maintains a local browser game and may recommend running local Playwright verification scripts after edits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
