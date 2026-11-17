## Description:

Organises a messy local music library into a clean Language/Artist/Album hierarchy using acoustic fingerprinting, deduplication, metadata enrichment, and optional Spotify sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drajb](https://clawhub.ai/user/drajb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents helping users clean local music collections use this skill to prepare environment settings, run the Sonic Phoenix pipeline, review generated catalogs, stage duplicates for manual review, and optionally sync playlists to Spotify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks the user to clone and run upstream code that is not pinned to a reviewed commit.

Mitigation: Pin the upstream repository to a specific reviewed commit and inspect dependencies before installing or running the pipeline.

Risk: Pipeline actions can make broad changes to a local music library.

Mitigation: Run against a backup or copy of the library first, keep MUSIC_ROOT scoped to the intended collection, and use dry-run or preflight checks before full execution.

Risk: The security review identifies an unsafe helper-script pattern involving status.sh.

Mitigation: Avoid running status.sh until the eval issue is fixed and reviewed.

Risk: Optional Spotify sync can change playlists and uses local library metadata during synchronization.

Mitigation: Enable Spotify only after reviewing the OAuth setup, playlist backup step, and expected playlist changes.

## Reference(s):

- [Data files reference](references/data-files.md)
- [Language hints guide](references/language-hints-guide.md)
- [Declared upstream source](https://github.com/drajb/sonic-phoenix)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file operations, pipeline execution steps, environment variables, and optional Spotify setup guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
