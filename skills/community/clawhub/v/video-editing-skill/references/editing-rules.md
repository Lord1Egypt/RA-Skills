# Editing rules

What `scripts/edit_video.py` does and why. Most numbers come from editors' and tool makers'
published practice rather than a platform standard; they are defaults to adjust, not laws.

## Styles

| | youtube (default) | tight | podcast |
|---|---|---|---|
| Pauses shortened when longer than | 0.50 s | 0.30 s | 0.80 s |
| Beat kept mid-sentence | 0.30 s | 0.22 s | 0.40 s |
| Beat kept after a sentence | 0.45 s | 0.25 s | 0.60 s |
| Beat kept at a long gap or card | 0.90 s | 0.50 s | 1.00 s |
| Smallest pause worth cutting | 0.40 s | 0.25 s | 0.60 s |
| Punch-in | 1.10x | 1.15x | off |
| Loudness | -14 LUFS | -14 LUFS | -16 LUFS |

A cut that saves less than the smallest pause worth cutting is skipped: every cut in a
continuous shot is a visible jump, and a dozen tiny ones save a few seconds while making the
video look nervous. Removed fillers, stutters and retakes are always cut.

The report separates time removed from inside the talking from time removed in long gaps,
cards, the opening and the ending, so a 20% headline isn't mostly a deleted end slate. It also
shows the pace in words per minute; over 190 is flagged as rushed, and removing more than 45%
of a video usually means something went that shouldn't have.

## Where a cut goes

- **By ear, not only by the transcript.** Transcribers often put a word's end 50 to 150 ms
  early. Every cut-out point moves forward until the audio has been quiet (the room's noise
  floor plus 6 dB) for 30 ms, up to 250 ms; every cut-in point moves back the same way, up to
  200 ms, and never closer than 100 ms before the word. Edges never move into a word.
- **By eye.** Black frames and shot changes are detected once. A title card inside a removed
  gap goes entirely; a shot change within half a second of a kept edge moves the edge past it,
  so no stray frames of a card or another angle flash by.
- **On the frame grid.** Every edge is rounded to a whole frame, and pieces are cut and joined
  in one filter pass per group, so picture and sound stay in sync over hundreds of cuts. The
  script checks the final durations and warns if they differ by more than a frame.
- **No flicker.** A kept piece under 0.4 s joins a touching neighbour; it never pulls back
  something that was removed.
- **4 ms fades** at each cut keep it from clicking without dipping the room tone.

## Fillers

- **Always cut:** um, uh, uhm, umm, er, erm, ah, hmm. Only with a small gap on at least one side;
  a filler fused to both neighbours would take part of them with it. "Mm hmm" (agreement) stays.
- **Opt-in** (`extra_fillers`): "like", "so", "you know", "basically", "actually", "kind of".
  These carry meaning often enough that cutting them by default changes sentences. Single words
  are cut only next to a comma; phrases always.
- **Transcripts drop fillers.** Whisper-family models leave out most "um"s unless the prompt
  contains some, so `transcribe.py` prompts with them. Sounds still missing from the transcript
  are found in the audio between words.

## Stutters and retakes

Always keeping the last take:

- **Stutter:** the same word twice in a row with under 0.25 s between and no comma ("we we
  built"), or the same two words twice ("it's the it's the"). Words people repeat on purpose
  are never touched: very, really, that, had, is, no, yeah, so, bye, well.
- **Retake cue:** "let me say that again", "let me start over", "let me try that again",
  "scratch that", "take two". The cue goes; the sentence before it goes too only when the next
  sentence repeats at least half of its words.
- **Restart:** an unfinished fragment (no end punctuation, 8 words or fewer) followed by a
  sentence that opens with the same words goes. Two **finished** sentences that open the same
  way ("It was great. It was fun.") are never cut automatically; they're listed in the plan as
  possible retakes for the agent and the user to decide.

## Punch-ins

Switching between the full frame and a slight punch-in makes a jump cut read as an edit. The
script switches at every cut that removed a second or more, and otherwise only after 4 seconds
(2.5 in tight) on the same framing; never at a cut onto a new camera shot, which already
changes the picture. Hard cuts, eyes kept level, capped at 1.2x. On sources under 1080p keep it
at 1.1x or turn it off.

## Audio

1. Gain to about -20 LUFS (quiet recordings first come up to a working level).
2. `highpass` at 80 Hz.
3. `afftdn` noise reduction with its floor set from the measured room noise; skipped when the
   room is already quiet (under -60 dB), so quiet word endings aren't eaten.
4. `acompressor` 3:1 from -24 dB, 5 ms attack, 120 ms release.
5. `alimiter`, set so peaks end at -2 dB after the final gain (headroom for the AAC encoder).
6. One clean gain to -14 LUFS, measured on the processed audio. Linear: no pumping.

All of these filters exist in every common ffmpeg build. -14 LUFS is the level YouTube and the
short-form apps are widely measured to play at.

## Captions

- **`captions.srt` every time**, for uploading in YouTube Studio: at most 2 lines of 42
  characters, 1 to 7 seconds each, captions left up long enough to read, gaps under 0.3 s
  closed, two frames between captions. Lines don't break after a small word or inside a name.
- **Burned in** (`"burn": true`, on by default for vertical): white bold text with an outline of
  8% of the font size and a soft shadow, centred, 4.2% of the frame height (one line of 32
  characters in vertical). Not together with an uploaded SRT on the same YouTube video.
- **Names:** pass them to `transcribe.py --terms` and fix the rest with `"replace"`.

## Chapters

YouTube shows chapters when the description lists timestamps with the first at 0:00, at least
three in order, each at least 10 seconds long. Write them in the original video's times; the
script moves them to the edited timeline and warns when one gets too short.
