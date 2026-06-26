## Minimal live rehearsal loop

One workable MVP loop is:

1. Build blueprint.
2. Create `history.json`:

```json
{"turns": []}
```

3. Generate first counterpart turn from phase `opening`.
4. Synthesize counterpart audio.
5. User answers by voice.
6. ASR transcribes the answer.
7. Save transcript as current user reply.
8. Generate the next counterpart turn with `build_counterpart_turn.py`.
9. Repeat for 3 to 4 rounds.
10. Concatenate the user's replies and run `analyze_rehearsal_transcript.py`.

Good fit for AudioClaw:

- AudioClaw handles state and session memory.
- AudioClaw handles:
  - ASR for user spoken turns
  - TTS for counterpart turns
- LLM layer handles:
  - counterpart reasoning
  - pressure style
  - debrief and rewrite suggestions
