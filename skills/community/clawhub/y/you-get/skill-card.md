## Description:

A web media download assistant that helps agents use you-get to inspect and download videos, audio, images, subtitles, and metadata from supported websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through installing you-get, checking available media formats, selecting download options, and troubleshooting common download failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser cookie files can act like account credentials when used for authenticated media downloads.

Mitigation: Only provide exported cookies or browser cookie databases when the user understands the account-access implications, and prefer scoped, temporary cookie files.

Risk: Unpinned or mutable install commands can install code that differs from the reviewed release.

Mitigation: Use an isolated Python environment and prefer stable package releases over mutable develop-branch installs.

Risk: Download commands can write media files to unexpected paths or overwrite existing files.

Mitigation: Confirm the destination directory, filename, and overwrite behavior before running download commands.

Risk: Troubleshooting guidance that disables a system firewall can reduce host protection.

Mitigation: Do not run firewall-disable troubleshooting steps; use narrower network diagnostics or rule-specific changes instead.

## Reference(s):

- [you-get GitHub repository](https://github.com/soimort/you-get)
- [you-get project website](https://you-get.org/)
- [you-get documentation wiki](https://github.com/soimort/you-get/wiki)
- [FFmpeg downloads](https://ffmpeg.org/download.html)
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/skills/you-get)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local installation, media inspection, download, playback, proxy, cookie, batch download, and troubleshooting commands.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
