## Description:

Use when the user provides a Bilibili or YouTube URL and asks for a transcript, article, or subtitle extraction. Downloads platform subtitles via BBDown / yt-dlp and produces a clean Markdown transcript in the source language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hqwqf](https://clawhub.ai/user/hqwqf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract available Bilibili or YouTube subtitles, normalize them, and produce clean source-language Markdown transcripts for later reading or article drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install persistent downloader executables.

Mitigation: Review before installing, prefer already-installed trusted BBDown or yt-dlp binaries or package-manager installs, and avoid third-party GitHub proxy mirrors unless their trust risk is acceptable.

Risk: The skill may handle browser session cookies for restricted videos.

Mitigation: Use cookies only after unauthenticated subtitle access fails, treat cookies.txt and BBDown cookie strings like passwords, keep them task-local, restrict access, and delete them after use.

Risk: Adding a tools directory to PATH creates a persistent system change.

Mitigation: Do not add the tools directory to PATH unless a persistent command lookup change is intended.

## Reference(s):

- [Authentication & Cookies Guide](references/auth.md)
- [Subtitle Cleanup Guide](references/cleanup_guide.md)
- [Tool Installation Guide](references/install_tools.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Worked Example](references/worked_example.md)
- [BBDown Releases API](https://api.github.com/repos/nilaoda/BBDown/releases/latest)
- [Get cookies.txt LOCALLY Chrome Extension](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown transcript files with supporting shell commands and task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces source-language transcript deliverables and may use per-task metadata, subtitle files, and cleanup steps before final output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
