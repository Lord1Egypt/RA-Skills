## Description:

Fetch, transcribe, summarize, and filter YouTube channels or individual videos. Use when asked to analyze a full YouTube channel, parse a single video, collect transcripts, group or filter videos by date, topic, speakers, or metadata criteria, or produce reusable summaries and structured outputs from YouTube content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ulyanas](https://clawhub.ai/user/ulyanas)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, researchers, and developers use this skill to inventory YouTube channels or analyze individual videos, retrieve or generate transcripts, filter content by metadata or spoken criteria, and produce reusable summaries, notes, reports, and datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Insecure YouTube download settings can weaken transport assurance.

Mitigation: Review download behavior before use and remove the default certificate-bypass behavior before relying on outputs.

Risk: Weak boundaries around URLs, cookies, output paths, and persistent generated files can expose sensitive video data or local artifacts.

Mitigation: Run the skill in an isolated workspace, avoid browser-cookie options unless explicitly needed, avoid sensitive or proprietary videos, and clean generated artifacts after use.

Risk: Runtime dependencies may change behavior across runs when they are not pinned.

Mitigation: Prefer pinned versions of yt-dlp, youtube-transcript-api, and faster-whisper for repeatable production use.

## Reference(s):

- [Dependencies](references/dependencies.md)
- [Filtering](references/filtering.md)
- [Outputs](references/outputs.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Guidance]

**Output Format:** [Markdown reports, transcript text files, JSON and CSV datasets, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent artifacts under output/<output_prefix>/, including inventory, filtered dataset, transcript, and report directories.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
