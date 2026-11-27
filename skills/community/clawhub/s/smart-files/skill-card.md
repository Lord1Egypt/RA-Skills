## Description:

Secure file search, dedup, organize, and rename for workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect workspace files, search file contents, find duplicates, categorize files, preview renames, and monitor file changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad local file-read and monitoring access, and the security evidence says workspace boundaries and security claims should be reviewed before trusted use.

Mitigation: Install only in workspaces where local file reading and monitoring are acceptable, avoid sensitive directories, and review path validation, symlink handling, and scoping before trusted automation.

Risk: Using snippet output can expose raw file contents, including secrets, to terminal logs or agent context.

Mitigation: Keep snippets disabled by default and avoid `--snippets` on directories that may contain credentials, private data, or confidential files.

Risk: `--force` can permit external-path access and watch-mode operations that persist file metadata to a journal.

Mitigation: Avoid `--force` unless external access is intentional, run dry-run previews first, and clear or protect `memory/smart-files-journal.json` when path and hash metadata is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/smart-files)
- [README](README.md)
- [Vetting report](VET-REPORT.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output with optional JavaScript object results when used as a module]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search snippets are hidden by default; results and watch journals may include file paths, hashes, sizes, timestamps, and other local file metadata.]

## Skill Version(s):

2.2.3 (source: server release metadata, SKILL.md frontmatter, clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
