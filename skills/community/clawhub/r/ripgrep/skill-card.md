## Description:

Blazingly fast text search tool - recursively searches directories for regex patterns with respect to gitignore rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnarsson](https://clawhub.ai/user/arnarsson)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to get concise ripgrep command guidance for fast recursive text search, file filtering, context output, and replacement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using --hidden or --no-ignore can search ignored or private files and surface sensitive content.

Mitigation: Review search scope, path filters, and ignore-related flags before running commands in repositories with private or generated files.

Risk: The sed -i replacement pipeline can modify many files in place.

Mitigation: Preview matches first, narrow paths or file types, and rely on version control or backups before bulk replacement.

## Reference(s):

- [ClawHub Ripgrep Skill](https://clawhub.ai/arnarsson/skills/ripgrep)
- [ripgrep GitHub Repository](https://github.com/BurntSushi/ripgrep)
- [ripgrep User Guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the rg binary; install metadata lists Homebrew formula ripgrep and apt package ripgrep.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
