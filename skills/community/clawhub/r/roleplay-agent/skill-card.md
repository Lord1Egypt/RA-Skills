## Description:

Roleplay Agent helps writers build actor-direction personas, run scene-based roleplay interactions, and generate natural dialogue from each character's want, obstacle, and moment-before context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[defineagain](https://clawhub.ai/user/defineagain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative writers use the skill to create persona-driven roleplay scenes, generate dialogue from wants and obstacles, and preserve arc notes for later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Roleplay notes and arc logs may persist sensitive creative or personal material in local files.

Mitigation: Use the skill only in workspaces where persistent roleplay notes are acceptable, and ask for explicit user consent before writing arc logs or updating persona files.

Risk: Helper scripts accept persona names or file paths with weak boundaries.

Mitigation: Avoid untrusted persona names or file paths until path validation is tightened.

Risk: The artifact contains language that may weaken safety and content boundaries during difficult roleplay scenes.

Mitigation: Keep all writing guidance subordinate to applicable safety, consent, and content boundaries.

## Reference(s):

- [Roleplay Agent release page](https://clawhub.ai/defineagain/skills/roleplay-agent)
- [Beat Writing Format](assets/beat_format.md)
- [Persona Template](personas/template.md)
- [Example Persona: Eve](personas/example_eve.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown dialogue, persona definitions, scene setup prompts, arc notes, and helper script commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persona and arc-log files when the user consents.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
