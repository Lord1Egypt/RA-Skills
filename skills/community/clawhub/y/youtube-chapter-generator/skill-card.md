## Description:

Auto-generate YouTube video chapters from subtitles by parsing VTT/SRT files, identifying topic transitions, and producing timestamped chapter markers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzxiatian-crypto](https://clawhub.ai/user/dzxiatian-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to generate YouTube-ready chapter timestamps from subtitle files. It helps agents propose subtitle download commands, chapter extraction logic, and formatted chapter lists for videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references command-line processing of YouTube subtitles and local subtitle files.

Mitigation: Run the referenced commands only for videos and subtitle files you are authorized to process, and review generated shell commands before execution.

Risk: The artifact provides guidance and example logic rather than a complete packaged tool.

Mitigation: Confirm any referenced local script such as generate_chapters.py exists and has been reviewed before running it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces timestamped chapter markers and procedural guidance; no bundled executable code is included in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
