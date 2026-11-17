## Description:

Secure file search, dedup, organize, and rename for workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Smart Files to inspect local workspaces, search file contents, find duplicates, summarize file metadata, preview cleanup candidates, and monitor file changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive scans can read files that contain secrets or sensitive local data.

Mitigation: Run the skill only in trusted workspaces and avoid directories that may contain credentials, private documents, or unrelated project data.

Risk: Using --snippets prints raw matched content to stdout and may expose it to terminal logs or agent context.

Mitigation: Leave snippets disabled unless raw content is needed, and review the target directory before enabling --snippets.

Risk: --force can override the workspace boundary and allow scanning of process-readable external paths.

Mitigation: Use --force only for intentional external scans and provide the narrowest practical path.

Risk: Watch mode persists file paths, hashes, sizes, timestamps, and change events to memory/smart-files-journal.json.

Mitigation: Treat the journal as persistent workspace metadata and clear it manually when the file activity history should not be retained.

## Reference(s):

- [Smart Files ClawHub page](https://clawhub.ai/jlacroix82/skills/smart-files)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search snippets are hidden by default; watch mode persists file path, hash, size, timestamp, and change-event metadata.]

## Skill Version(s):

2.2.0 (source: server release evidence, SKILL.md frontmatter, clawhub.yaml, CHANGELOG.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
