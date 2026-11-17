## Description:

Expert knowledge of Starship cross-shell prompt, including installation, CLI usage, TOML configuration, modules, style strings, presets, transient prompts, custom modules, palettes, right prompt, and Fish shell integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and terminal users use this skill as a Starship prompt reference for installing Starship, configuring Fish shell integration, writing starship.toml settings, selecting presets, and troubleshooting prompt behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes a remote shell installer pattern.

Mitigation: Prefer package-manager or Cargo installation paths, and inspect any downloaded installer before execution.

Risk: Configuration examples and presets may overwrite or alter local Starship settings.

Mitigation: Back up ~/.config/starship.toml before applying presets or examples that write directly to the configuration file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/starship-prompt)
- [Publisher profile](https://clawhub.ai/user/mina-atef-00)
- [Homepage](https://github.com/mina-atef-00/agent-skills)
- [Starship configuration schema](https://starship.rs/config-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reference guidance with inline shell commands and TOML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install packages or write shell and Starship configuration files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
