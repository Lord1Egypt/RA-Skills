## Description:

End-user guide for running and configuring the `translate` CLI across text/stdin/file/glob inputs, provider selection, presets, custom prompt templates, and TOML settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atacan](https://clawhub.ai/user/atacan)

### License/Terms of Use:


## Use Case:

Developers and CLI users use this skill to construct reliable `translate` commands, configure providers and TOML defaults, customize prompts, and troubleshoot translation behavior for text, stdin, files, globs, and `.xcstrings` catalogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translated text or file contents may be sent to the configured provider.

Mitigation: Use trusted providers for sensitive documents and run `--dry-run` first when checking provider, model, and prompt resolution.

Risk: `--in-place` or `--yes` can overwrite files without an interactive confirmation.

Mitigation: Prefer explicit output files or backups, review the output plan, and use `--yes` only after confirming overwrite behavior.

Risk: API keys can be exposed if placed directly on command lines or stored carelessly.

Mitigation: Prefer environment variables or protected config files and avoid sharing shell history or logs that contain credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atacan/skills/translate-cli)
- [Quickstart](references/quickstart.md)
- [Flags and Subcommands](references/flags-and-subcommands.md)
- [TOML Configuration](references/config-toml.md)
- [Providers and Environment](references/providers-and-env.md)
- [Presets and Prompts](references/presets-and-prompts.md)
- [Behavior, Validation, and Errors](references/behavior-and-errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples, provider setup steps, prompt templates, config keys, validation checks, and troubleshooting guidance.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
