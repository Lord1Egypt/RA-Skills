## Description:

Checks and repairs subtitle readability in SRT and WebVTT files by measuring reading speed, line length, cue duration, gaps, and overlaps, fixing timing first and proposing wording changes only with user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypercube67-formal](https://clawhub.ai/user/hypercube67-formal)

### License/Terms of Use:

MIT

## Use Case:

Subtitle editors and reviewers use this skill to check SRT and WebVTT readability and improve timing or, with approval, condense text. It checks reading speed and layout against configurable presets; it does not create subtitles from audio or video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report options may overwrite the original subtitle despite the tool's preservation promise.

Mitigation: Keep a backup; use distinct, unused paths for the repaired subtitle and both reports, avoid links to existing files, and prefer a version that validates every output path before writing.

## Reference(s):

- [Reading-speed limits and method](references/style-guides.md)
- [Condensing and line-break rules](references/condensing.md)
- [Approved edit format](references/apply-format.md)
- [Subtitle reading-speed method](https://scribetoany.com/blog/subtitle-reading-speed-cps)
- [Netflix English timed-text style guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide)
- [Netflix general timed-text requirements](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements)
- [BBC subtitle guidelines](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/)

## Skill Output:

**Output Type(s):** [Analysis, Text, Subtitle files, JSON]

**Output Format:** [Plain-text QC summary; repaired SRT or WebVTT; optional JSON reports and edit instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timing repairs preserve wording; wording edits are proposed for user approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
