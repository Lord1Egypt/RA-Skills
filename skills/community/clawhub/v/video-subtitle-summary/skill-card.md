## Description:

Extracts exposed subtitles or transcripts from videos, learning platforms, browser-visible transcript panels, or local subtitle files and turns them into timestamped Markdown study notes; it does not perform audio transcription, playback capture, or access-control bypass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hejunhui-73](https://clawhub.ai/user/hejunhui-73)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, employees, and external users use this skill to turn authorized, subtitle-accessible video or course content into structured Markdown notes with timestamps, summaries, terms, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browser automation and API interception may capture more than subtitles from learning pages.

Mitigation: Review before installation, use a contained browser session, avoid accounts or course pages with sensitive material, and minimize token handling and raw JSON persistence.

Risk: Generated notes may be incomplete or inaccurate when subtitles are missing, partial, auto-generated, or lack visual context.

Mitigation: Process only exposed subtitles or transcripts, stop when subtitles are unavailable, preserve timestamps when available, and clearly mark completeness, limitations, and accuracy caveats.

Risk: The workflow touches authenticated course platforms and could be misused for assessment or participation automation.

Mitigation: Do not answer graded assessments, automate course completion, bypass access restrictions, or misrepresent attendance, progress, identity, or results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hejunhui-73/skills/video-subtitle-summary)
- [Online Subtitle Strategy](artifact/references/online-subtitle-strategy.md)
- [Playwright Browser Automation](artifact/references/playwright-browser-automation.md)
- [Processing Policy](artifact/references/processing-policy.md)
- [Report Format](artifact/references/report-format.md)
- [Time Estimation](artifact/references/time-estimation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with timestamped notes, plus optional local metadata and docx/pdf/html exports when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subtitle-only workflow; reports should label source, acquisition method, completeness, limitations, and accuracy notes.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
