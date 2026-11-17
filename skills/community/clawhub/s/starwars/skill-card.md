## Description:

CLI for AI agents to look up Star Wars universe information using SWAPI with no authentication required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffaf](https://clawhub.ai/user/jeffaf)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to look up Star Wars characters, planets, films, species, and starships through SWAPI-backed CLI queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package appears to document a CLI that is not included in the inspected artifact, so commands may not work as described.

Mitigation: Confirm the CLI wrapper or script is present in the installed package before relying on command examples.

Risk: The skill depends on public SWAPI data and is limited to the coverage described by the artifact.

Mitigation: Use it for the documented character, planet, film, species, and starship lookups, and verify answers outside Episodes 1-6 with another source.

## Reference(s):

- [SWAPI](https://swapi.dev)
- [ClawHub skill page](https://clawhub.ai/jeffaf/skills/starwars)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text command output and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, and jq; uses public SWAPI queries and does not require credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
