## Description:

Retrieve YouTube captions and subtitle segments with FlashData. Use for uploader-provided subtitles, language-specific caption tracks and SRT or WebVTT exports. Selects manual captions by default. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve an existing YouTube caption track in a selected language, return its text and timings, or convert the timed segments to SRT or WebVTT while preserving the source wording and timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted FlashData service receives the API key and query arguments, and the available security scan is incomplete.

Mitigation: Keep the API key in protected environment or secret-manager settings, send only intended query arguments, and review the skill and its dependencies before installation.

Risk: Caption data queries spend paid FlashData Credits; a timed-out submission may have an unknown outcome.

Mitigation: Check pricing and the approved query budget before submitting. After a timeout, check the existing job or FlashData Jobs before considering another request.

## Reference(s):

- [FlashData YouTube Captions documentation](https://flashdata.dev/docs/sources/youtube_captions?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_captions-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_captions-task)
- [FlashData API key signup](https://flashdata.dev/signup?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_captions-task)
- [Caption query example](references/query.json)
- [Caption query schema](references/schema.json)

## Skill Output:

**Output Type(s):** [Text, JSON, SRT, WebVTT]

**Output Format:** [Caption text or timed caption segments; SRT and WebVTT subtitle text can be produced from returned segments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an existing caption track in the requested language; preserves source wording, order, and timing. Manual and automatic tracks are selected explicitly without fallback.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
