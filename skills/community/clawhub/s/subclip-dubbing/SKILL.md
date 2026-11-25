---
name: subclip-dubbing
description: Translate and dub an existing Subclip timeline audio/video item under assistant control using exact captions, speaker-aware temporary voices, bounded TTS retries, duration-fit review, atomic timeline placement, and translated visual-caption replacement when captions were already shown. Use for translated voice replacement or multilingual dubbing; do not route this workflow through the separate Dub Studio/Dubbing API.
---

# Subclip Assistant Dubbing

The assistant owns translation and semantic timing decisions. MCP tools own source extraction, temporary voice lifecycle, speech generation, measurement, placement, accounting, and cleanup.

1. Identify one exact audible `mediaItemId` or `audioItemId`. If it lacks exact-item captions, look for a saved transcript with `list_reference_transcripts`; otherwise call `transcribe_project` with `purpose: "reference"`. For multiple speakers use `mode: "cloud"` and `detectSpeakers: true`; wait for its terminal callback.
2. Call `create_dubbing_workspace` for that item, passing `referenceTranscriptId` when using a saved reference transcript. Read every page with `get_dubbing_workspace`. Keep segment IDs, speaker IDs, and timing windows unchanged.
3. Translate each segment yourself and call `update_dubbing_translations`. Preserve meaning, intent, names, numbers, dates, negation, calls to action, and other returned `lockedTerms`.
   - Prefer a natural concise equivalent before paid TTS when a translation is marked `likely-overflow`.
   - Remove redundancy and choose shorter idioms; never delete a required fact merely to fit.
   - A short translation may leave natural silence. Expand it only when tighter sync matters and an equally faithful phrasing exists; never invent filler or facts.
4. Configure every speaker independently.
   - For a system or already-saved voice, call `list_ai_voices`, then `set_dubbing_speaker_voice` with the exact stable ID.
   - Call `prepare_dubbing_temporary_voice` only when the creator explicitly asks to clone, preserve, match, or use the source speaker’s voice. A generic “translate/dub” request does not authorize voice cloning.
   - Prepare one temporary speaker voice at a time and wait for its terminal callback before starting the next clone.
   - `referenceMode: "source"` extracts only that diarized speaker’s non-overlapping source passages. `referenceMode: "attachment"` requires an exact current-conversation attachment. Never import either reference into AudioPanel.
   - Never assign one reference to several detected speakers unless the creator explicitly requests one common voice. If a speaker lacks enough clean source speech, use an authorized attachment/system voice or ask; do not silently reassign the speaker.
5. Call `generate_dubbing_segments` in batches of at most 12. A direct request for this exact dubbing workflow authorizes the first matching bounded batch; pass `confirmed: true`. Do not start another batch until the terminal callback or workspace state proves the prior batch is terminal.
6. After completion, call `get_dubbing_workspace` and use measured duration, not character count, as truth.
   - `actualDurationRatio <= 1.08` is normally safe for a mild final speed fit.
   - Above the chosen maximum speedup, rewrite that segment more concisely with `update_dubbing_translations`, then regenerate only that segment.
   - A substantially short result may be rewritten with a longer equivalent when exact sync matters; otherwise preserve natural silence.
   - Never truncate speech. Never exceed the workspace attempt cap or the creator’s credit ceiling. A failed operation is not permission to regenerate unrelated/completed segments.
7. Call `commit_dubbing_workspace` only when every segment is completed and semantically reviewed. Commit downloads and imports all segment audio first, then atomically mutes the exact original source when the workspace requests replacement. It never stretches a short audio source across a longer Remotion trim window. Use `captionReplacement.hadVisibleSourceCaptions` and `captionReplacement.sourceItemId` from the result as the canonical caption-replacement decision; do not try to reconstruct ownership after the hidden workspace is cleaned.
8. If the source had visible captions, caption the committed dubbed audio too.
   - Keep the source-language captions visible as a fallback until every new caption batch succeeds. Preserve the existing project-wide caption style; transcription must change caption content/timing, not restyle it.
   - When the committed dubbed items are the finished audible timeline, call `transcribe_project` once with `allTimelineClips: true` and the target language. This mixes every audible dubbed clip, saves one coherent target-language transcript, and atomically replaces the complete old caption set; do not guess or wait for individual item IDs.
   - Pass a base ISO language code such as `fr`, `es`, or `de`, not a regional locale such as `fr-FR`. The local runtime normalizes accepted locale inputs, but canonical codes keep cloud/local behavior consistent.
   - Follow an explicitly requested local/cloud mode. Otherwise use local transcription for clean generated speech. Do not request diarization again: speaker separation was already established by the dubbing workspace.
   - Use per-item transcription only when the creator explicitly wants bilingual captions or needs independently owned caption batches. In that case use the exact IDs returned by `commit_dubbing_workspace.imported`, transcribe chronologically, and remove the original source batch only after the final new batch succeeds.
   - After the terminal callback, verify visible target-language captions and confirm the source-language batch is absent when replacement was requested. If transcription fails, the editor keeps the previously saved captions as fallback; retry or report the failed run without manually clearing caption data.
9. If the creator abandons the uncommitted workflow, call `discard_dubbing_workspace` with `confirmed: true` after all running jobs are terminal.

The hidden `.agent/dubbing/<workspaceId>/plan.md` is scratch context; `state.json` is canonical. Temporary provider voices, reference samples, intermediate cloud speech operations, and the hidden workspace are cleanup-owned. Do not copy provider voice IDs or signed URLs into captions, director notes, or user-facing text.
