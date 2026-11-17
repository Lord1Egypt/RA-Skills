## Description:

SuperPicky CLI skill wraps the upstream SuperPicky bird-photo workflow with predictable install and run scripts for photo culling, bird identification, and eBird country or region code lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoshino-s](https://clawhub.ai/user/yoshino-s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install and run SuperPicky's local CLI workflow for bird-photo culling, identification, batch organization, and region-code lookup. It is intended for local automation over photo directories through fixed shell entry points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and runs mutable upstream code and dependencies at install time.

Mitigation: Install only after reviewing and trusting the upstream SuperPicky repository and dependency set, preferably in a sandbox or disposable environment.

Risk: The --py helper can execute Python scripts through the skill-managed virtual environment.

Mitigation: Do not pass untrusted values to --py, and restrict usage to reviewed scripts and known paths.

Risk: reset, restar, organize, and related commands can move files, edit metadata, or change photo directory contents, especially when -y is used.

Mitigation: Run on backed-up or disposable photo directories first, and use -y only when the file changes are explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoshino-s/skills/superpicky)
- [SuperPicky upstream repository](https://github.com/jamesphotography/SuperPicky)
- [Captured CLI help](artifact/reference/cli-help-captured.txt)
- [Reference metadata](artifact/reference/SOURCE.md)
- [Reference index](artifact/reference/README-INDEX.md)
- [Manifest behavior notes](artifact/reference/manifest机制说明.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance, with optional JSON output from the region-query helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on local CLI entry points, install options, and photo-directory operations.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
