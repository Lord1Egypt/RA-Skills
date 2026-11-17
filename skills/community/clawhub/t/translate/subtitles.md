# Subtitles, Captions, and Dubbing

Subtitling is translation under two hard constraints the source never had: the viewer reads at a fixed speed while watching pictures, and the text disappears. Everything here follows from those two facts.

**Contents:** [The Reading Budget](#the-reading-budget) · [Line Breaks and Segmentation](#line-breaks-and-segmentation) · [Timing](#timing) · [Condensation](#condensation) · [File Formats](#file-formats) · [Frame Rates and Drift](#frame-rates-and-drift) · [Translating an Existing Subtitle File](#translating-an-existing-subtitle-file) · [Captions and SDH](#captions-and-sdh) · [Forced Narratives and On-Screen Text](#forced-narratives-and-on-screen-text) · [Songs](#songs) · [Dubbing and Voice-Over](#dubbing-and-voice-over) · [Audio Description](#audio-description) · [Review Against the Picture](#review-against-the-picture) · [What To Write Down](#what-to-write-down)

**Before starting a title for a client you have worked with**, read `## Environment` and any `artifacts/subtitle-spec-*.md` that `## Boxes` names. Every platform has its own style guide, and the differences are numeric — one wrong ceiling means the whole file is rejected.

## The Reading Budget

These are the widely adopted streaming defaults; `subtitle_cps` overrides the first one, and a client style guide overrides all of them.

| Parameter | Default | Notes |
|---|---|---|
| Reading speed, adult | 17 characters per second | The single most important number; exceed it and the viewer stops watching the picture |
| Reading speed, children | 13 characters per second | Applies to the whole title, not to individual lines |
| Characters per line, Latin script | 42 | Broadcast style guides often use 37-38; check before starting |
| Lines per subtitle | 2 | Three lines exist only in a few broadcast standards |
| Minimum duration | 5/6 second (0.833 s) | Below this the eye registers a flash, not a word |
| Maximum duration | 7 seconds | Longer and the viewer re-reads it |
| Gap between subtitles | 2 frames minimum | Without it, consecutive subtitles look like one that flickered |

**Formula**: a subtitle of `n` characters needs at least `n ÷ cps` seconds on screen, floored at 0.833 s. A two-line 80-character subtitle at 17 CPS needs 4.7 seconds — if the shot is 3 seconds long, the text must lose 29 characters, not the shot gain time.

CJK is counted differently, in full-width characters: Japanese convention is about 13 full-width characters per line, two lines, and a budget near 4 full-width characters per second of screen time; Chinese usually prefers a single line of about 16 full-width characters. Never apply a Latin CPS figure to a CJK file.

## Line Breaks and Segmentation

Break where the sentence breaks, not where the line fills:

- Break **after** punctuation, and between clauses.
- Never split an article from its noun, a preposition from its object, a first name from a surname, a verb from its auxiliary, or a number from its unit.
- Prefer a bottom-heavy or balanced two-line shape over a long first line and a two-word second.
- One sentence spanning two subtitles is fine; a sentence spanning three is a signal to condense.
- One speaker per subtitle where possible; when two speak, use a dash before each line.

## Timing

- **Cue in on the first frame of speech** (a few frames early is acceptable and reads as natural), cue out at the end of the phrase, not the end of the pause.
- **Do not cross a shot change.** The eye re-reads any text that is on screen across a cut. Where crossing is unavoidable, extend at least about half a second past the cut rather than ending on it.
- Respect the audio's rhythm: a pause in the delivery is a subtitle boundary, and a subtitle that outlives the line it translates makes the actor look dubbed.
- Do not subtitle over burned-in text or the lower third; move the cue to the top of the frame instead (`Forced Narratives`).

## Condensation

Reaching the reading budget is a craft, not deletion. In order of what to cut first:

1. **Fillers and hesitations** — "well", "you know", "I mean" — unless characterizing.
2. **Redundancy with the picture.** If the character points at a door and says "look at that door", the door is visible.
3. **Vocatives and repeated names.** Address terms repeat far more in speech than reading tolerates.
4. **Information already given** in the previous subtitle.
5. **Syntactic compression**: shorter synonyms, active voice, dropped subordination.
6. Last: content. Cutting a plot point is a decision to flag, not a compression technique.

What never goes: a negation, a number, a name introduced for the first time, or the punchline of a joke.

## File Formats

| Format | Timecode shape | Notes |
|---|---|---|
| SRT | `00:01:23,456` (comma) | Sequential index per cue; no styling; the universal interchange format |
| WebVTT | `00:01:23.456` (period) | Requires the `WEBVTT` header line; supports cue settings (position, line, align) and CSS-ish styling |
| TTML / DFXP | XML | Broadcast and streaming delivery; carries styling and regions; the strictest to validate |
| EBU-STL | Binary, `.stl` | European broadcast; fixed character sets that can lose target-language characters |
| SCC / CEA-608 | Frame-based | US broadcast captions; 32-character lines, limited character set, no accents in the base spec |
| ASS / SSA | `0:01:23.45` | Fansub and karaoke heritage; full positioning and styling, poorly supported by players |

Converting SRT to VTT is not only the separator: the header must be added, indices may be dropped, and any `<font>` styling must be rewritten. Converting to a broadcast format can lose characters the target needs — check the character set before promising the target language.

## Frame Rates and Drift

- Timecodes are frame-based even when written as milliseconds. Common rates: 23.976, 24, 25 (PAL), 29.97 drop-frame, 30.
- **Progressive drift means a rate mismatch, not a sync offset.** A constant offset shifts every cue by the same amount; a mismatch grows linearly, so the end of the film is minutes out.
- The fix is a **ratio scale on every timestamp**, not an offset. Converting 25 fps material to 23.976: multiply by 25 ÷ 23.976 ≈ 1.0427. The reverse (film to PAL) is the classic 4% speed-up.
- Drop-frame (29.97) timecode skips numbers, not frames — never convert it by arithmetic on the displayed timecode.
- Verify sync at the **start, middle and end** of the file. Checking only the opening scene is how drift ships.

## Translating an Existing Subtitle File

- Keep the cue structure: indices and timecodes stay, text changes. Re-segmenting is a separate, chargeable job that requires the video.
- **Expansion breaks the reading budget silently.** A German or Spanish target of an English subtitle file usually exceeds 17 CPS on a third of the cues; every cue must be re-measured against `n ÷ cps` and condensed, not just translated.
- Never merge or split cues without the video: a merge that crosses a shot change or a speaker change creates a defect nobody can see in the text file.
- Recheck the cues around numbers and names, which are where a condensed target most often loses information.

## Captions and SDH

Subtitles assume the viewer hears the audio; captions and SDH (subtitles for the deaf and hard of hearing) do not.

- Speaker identification when the speaker is off screen or ambiguous, in the target's convention (a name and colon, or a dash).
- Non-speech audio that carries meaning, in brackets: `[door slams]`, `[phone rings]`. Not every sound — only the ones a hearing viewer uses.
- Music: a note symbol for lyrics, and a bracketed description for score that matters (`[tense music]`).
- Do not clean up disfluency in SDH the way you would in a subtitle: stammering, accents rendered in text, and interruptions are information for this viewer.
- Positioning matters more: move the caption when it covers a speaker's mouth, since lip-reading is part of the audience's comprehension.

## Forced Narratives and On-Screen Text

A **forced narrative** is a subtitle that appears even when the viewer is watching in the original language: foreign dialogue, signs, letters, texts and titles that carry plot. They are a separate file or a flagged subset, they are positioned near the text they translate rather than at the bottom, and they are the item most often missing from a delivery. List them explicitly in the brief.

Burned-in text in the picture cannot be moved: the subtitle moves instead, usually to the top of the frame.

## Songs

Three defensible treatments, chosen once per title and applied consistently: **leave untranslated** when the song is atmosphere; **translate literally** with a note when the lyrics carry plot; **translate singably** — matching syllable count, stress and rhyme — when the song will be dubbed or performed. Singable translation is a different craft with a different rate, and it is quoted separately (`transcreation.md`).

Mark lyrics with the target's convention (music note, italics) and keep line breaks aligned with musical phrases.

## Dubbing and Voice-Over

- **Lip sync has three levels**, and the brief must say which is being paid for: *phonetic sync* (matching visible labials — p, b, m — and open vowels at the start and end of a line), *rhythmic sync* (matching the number of syllables and the pauses), and *loose sync* (matching only the line's duration).
- The visible constraint is that a closed-lip consonant on camera must be a closed-lip consonant in the target. That is what makes a dub look right, and it routinely overrides the literal wording.
- **Voice-over (UN style)** — used for documentary and news — starts about two seconds after the original voice and ends before it, leaving the original audible at both ends. The target is condensed to fit that window, typically shorter than the original.
- Dubbing scripts carry more than dialogue: character names, timecodes per line, take numbers, and annotations for reactions and off-screen lines. Deliver in the studio's template, not as prose.
- **"Dubbese"** — target text that keeps the source's syntax and idioms because it fit the mouth — is the characteristic failure mode. The test is whether a native would ever say the line with the television off.
- Numbers, names and brand pronunciation need a pronunciation guide for the voice talent; supply it with the script.

## Audio Description

A separate craft, commissioned separately: a script describing visual information, written to fit the gaps in the dialogue, then recorded or synthesized. Translating an existing audio-description script means re-fitting it to the same gaps, so the expansion rules of dubbing apply, not those of subtitling.

## Review Against the Picture

The final pass runs with the video playing, never in the text editor. Check: every cue readable at its duration, no cue crossing a cut, no cue covering burned-in text, speaker changes correct, forced narratives present, names and numbers correct, and the last cue not orphaned over the credits.

## What To Write Down

- The client or platform's numeric spec — CPS, characters per line, minimum and maximum duration, gap, file format, whether SDH and forced narratives are included — is an **`artifacts/subtitle-spec-<client>.md`**, born as its own file, with its `## Boxes` line naming the client, in the same turn. Those numbers decide every file for that client and are the ones a delivery is rejected over.
- A delivered title is a row in **`deliveries/<year>.md`**; note the running time in the word-count cell (`92 min`) so the row stays comparable with word-based jobs.
- Character names, place names and recurring in-universe terms go in the pair's **glossary** — a series is where inconsistency is most visible, because the audience watches ten episodes in a week.
