## Description:

This skill buffers segmented ASR transcript text until an explicit end signal, then rewrites the full segment into fluent written text and optionally translates it when a target language is provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hei-maom](https://clawhub.ai/user/hei-maom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to post-process completed meeting, interview, podcast, video, or dictation transcripts into readable written text. It is suited to workflows that prefer a single final transcript after completion instead of live subtitle updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASR transcripts may contain sensitive meeting, interview, or dictation content.

Mitigation: Control when buffering ends, define transcript retention behavior, and verify which rewriting or translation service processes the text.

Risk: Premature finalization could produce unstable or incomplete written text.

Mitigation: Gate final output on explicit end signals such as end_of_stream, is_session_final, commit=true, or a user submission action.

## Reference(s):

- [Interface and Product Integration Guide](references/interface-guide-zh.md)
- [ClawHub skill page](https://clawhub.ai/hei-maom/skills/shumianyu)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Plain text or Markdown guidance with final rewritten transcript text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Buffers segmented ASR text until an explicit end or commit signal; translation is only applied when target_language is provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
