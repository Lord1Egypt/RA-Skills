# Speaker Segmentation

## Promise Level

This skill defaults to rough speaker segmentation based on semantics, not precise diarization.

Apply the same standard to:

- ASR transcripts
- platform subtitle files
- manually provided caption text

Do not assume subtitle boundaries match speaker boundaries.
For conversational media, do not stop at a cleaned transcript if speaker turns can be inferred with reasonable confidence.

## Required Order

For multi-speaker content, use this order:

1. acquire raw text, captions, or transcript
2. reconstruct a cleaned readable transcript
3. group turns into rough speaker blocks
4. write the final memo from the speaker-grouped transcript

Do not jump from raw subtitles straight to the final summary when speaker grouping is feasible.

## Strong Clues

- direct introductions
- moderator phrases such as “你怎么看”
- explicit name mentions
- clear question-answer exchanges
- consistent speaking style over a topic block

## Weak Clues

- short interjections
- agreement tokens
- laughter
- one-word replies

Treat weak clues conservatively.

## Output Style

Recommended labels:

- `主持人`
- the explicit person name when known
- `疑似某说话人` when confidence is low

If the source identifies participants but not line-level speakers, use those participant names as candidate labels and assign them conservatively.

## Boundary Policy

- Prefer fewer, longer blocks over over-fragmented alternating lines.
- Split when the topic control clearly changes hands.
- If the boundary is fuzzy, keep the larger semantic block together and note uncertainty if needed.
- Merge subtitle fragments into speaker blocks before presenting the final transcript to the user.

## Minimum Deliverable

For interviews, podcasts, panels, and multi-speaker videos:

- provide a cleaned transcript
- provide a rough speaker version
- note uncertainty where speaker assignment is weak

A subtitle file by itself is not the final user-facing transcript.
A job is incomplete if it skips the rough speaker version without an explicit user opt-out.
