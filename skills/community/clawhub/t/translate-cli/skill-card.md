## Description: <br>
End-user guide for running and configuring the `translate` CLI across text/stdin/file/glob inputs, provider selection, presets, custom prompt templates, and TOML settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atacan](https://clawhub.ai/user/atacan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to construct `translate` CLI commands, configure providers and TOML defaults, manage presets and prompt templates, validate dry runs, and troubleshoot translation behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI may send user text or file contents to configured translation providers. <br>
Mitigation: Review provider choice and custom base URLs before use, and prefer dry-run validation when checking command behavior. <br>
Risk: Commands can overwrite files when in-place output and confirmation bypass flags are used. <br>
Mitigation: Use output-file modes before broad file operations, and avoid `--in-place --yes` unless files are backed up or version-controlled. <br>
Risk: API keys may be exposed if entered directly into commands or shared configuration. <br>
Mitigation: Prefer environment variables or private local configuration for provider credentials. <br>


## Reference(s): <br>
- [Quickstart](references/quickstart.md) <br>
- [Flags and Subcommands](references/flags-and-subcommands.md) <br>
- [TOML Configuration](references/config-toml.md) <br>
- [Providers and Environment](references/providers-and-env.md) <br>
- [Presets and Prompts](references/presets-and-prompts.md) <br>
- [Behavior, Validation, and Errors](references/behavior-and-errors.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/atacan/translate-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples and TOML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider setup, credential handling guidance, dry-run checks, and troubleshooting notes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
