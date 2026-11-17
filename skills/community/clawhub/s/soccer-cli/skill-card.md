## Description:

A CLI to check soccer scores, game details, and player stats from your terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrojas537](https://clawhub.ai/user/jrojas537)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to install and operate a soccer statistics CLI that retrieves recent scores, fixture details, match events, squads, and player stats from API-Football.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API-Football key is stored in a local config file.

Mitigation: Treat the key as a secret and store ~/.config/soccer-cli/config.yaml with restrictive file permissions.

Risk: The Go build is not reproducibly pinned in the release evidence.

Mitigation: Review or pin Go dependencies before installing or deploying the CLI.

## Reference(s):

- [API-Football](https://www.api-football.com/)
- [ClawHub skill page](https://clawhub.ai/jrojas537/skills/soccer-cli)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and ASCII tables, with Markdown setup and usage instructions in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided API-Football key in ~/.config/soccer-cli/config.yaml.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
