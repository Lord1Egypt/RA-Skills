## Description:

Indexes local workspace files, tracks file changes, and helps agents find code, scripts, configuration, and documentation by keyword or intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgbin](https://clawhub.ai/user/zgbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain a local SQLite index of workspace files and retrieve relevant files, paths, summaries, and file statistics during code search or project navigation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can index broad local workspace areas and store file paths plus short content snippets in a local SQLite database.

Mitigation: Restrict watched and scanned directories before enabling the skill, and exclude secret stores, credentials, private agent configuration, and other sensitive files.

Risk: Weak scope controls may cause files outside the intended project area to be indexed.

Mitigation: Review and harden the configured watch directories and hook path validation before deployment.

Risk: Relative subprocess entry points can run the wrong local file if launched from an unexpected working directory.

Mitigation: Use absolute script paths or module execution from a controlled installation directory, and pin dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zgbin/skills/zgbin-file-indexer)
- [README](artifact/README.md)
- [Installation guide](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text or JSON-style command output containing file paths, file metadata, summaries, search results, and index statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores indexed paths and short content snippets in a local SQLite database.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, _meta.json, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
