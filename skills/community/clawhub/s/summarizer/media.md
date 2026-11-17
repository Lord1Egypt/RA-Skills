# Video, Audio, and Slides

Scope: podcasts, YouTube videos, lectures, webinars, conference talks, earnings calls, audiobooks, voice memos, and slide decks. The common problem is a low information density per minute and a transcript that is not what anyone said.

**Before summarizing recurring media** (a podcast series, a lecture course, a weekly webinar), read `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index) for prior episodes and `glossary.md` for the speaker names and jargon the transcriber will get wrong.

**Contents:** [Density](#density) · [What to Cut Wholesale](#what-to-cut-wholesale) · [Timestamps](#timestamps) · [ASR Errors](#asr-errors) · [Spoken vs Written Structure](#spoken-vs-written-structure) · [By Format](#by-format) · [Slide Decks](#slide-decks) · [Quoting](#quoting) · [Output Shapes](#output-shapes)

## Density

Spoken content runs at roughly 130-160 words per minute of conversational speech, 110-140 for a prepared talk. Two consequences:

- **Runtime converts to words**: a 90-minute podcast is ~11,700-14,400 words — a `long-sources.md` job, not a single read.
- **The compression ratio understates the cut.** A 300-word summary of a 90-minute episode is ~2.3% by words but is keeping perhaps four ideas out of an hour and a half. Set expectations in the header with runtime, not just word count.

Prepared, scripted material (a documentary, a conference talk) has far higher density than a conversation. An unscripted two-host podcast can carry its entire content in ten minutes of the ninety.

## What to Cut Wholesale

These deletions cost nothing and typically remove 30-50% of an episode before any judgment is applied — filler alone accounts for 20-40% (`meetings.md`), sponsor, intro and housekeeping segments for the rest:

| Segment | Signature |
|---|---|
| Cold open and intro music narration | "Welcome back to…", theme description |
| Sponsor reads and ad breaks | Product pitch with a discount code; frequently mid-roll and repeated |
| Housekeeping | Subscribe requests, Patreon, merch, "link in the description" |
| Guest introduction read from a bio | Compresses to one clause: name, role, why they are qualified |
| Small talk and rapport | Weather, travel, mutual compliments |
| Filler and false starts | "um", "you know", restarts, backchannel ("mm-hmm") |
| Recaps of the previous episode | Already covered if the user follows the series (`recurring.md`) |
| Q&A logistics | "Can everyone hear me", "we'll take questions at the end" |
| Outro and credits | Full section |

What survives the cut is the answer to the interview question, the argument, the numbers, and the disagreement.

## Timestamps

Timestamps are the one structural advantage this genre has over documents — they make a claim verifiable in ten seconds instead of a re-listen.

- **Attach a timestamp to anything quotable, contested, numeric, or actionable.** Not to every line: a summary that is 40% timestamps is an index.
- Format `[HH:MM:SS]` for anything over an hour, `[MM:SS]` below.
- **Chapter markers, when the source has them, are free structure** — use them as the semantic chunk boundaries for `long-sources.md` instead of inventing your own.
- **Timestamps in an edited re-upload drift.** If the source may have been re-cut, say the timestamps refer to the version you were given.
- For a video where the payload is visual (a demo, a chart on screen), the timestamp is the summary of that segment; describing a diagram in prose usually costs more words than it saves.

## ASR Errors

Automatic transcripts fail in predictable places, and those places are exactly the high-information tokens.

| Error class | Example | Handling |
|---|---|---|
| Proper nouns | Product, company, and person names come out phonetically | Repair against `glossary.md`; add new recurring names in the same turn |
| Technical terms and acronyms | Domain jargon rendered as common words | Check that the sentence makes sense in the domain; nonsense means a mis-transcription, not a novel claim |
| Numbers | "fifteen fifty" as a year, a price, or two numbers | Normalize to digits only when context makes the magnitude unambiguous |
| Homophone pairs | "affect/effect", "their/there", "cite/site" | Harmless in prose, dangerous in a legal or technical claim |
| Missing negation | "can" and "can't" collapse in fast speech | Any surprising claim gets re-read at its timestamp before it enters the summary |
| Speaker diarization | Labels swap, overlapping speech merges | Same rules as `meetings.md` — anchor on names spoken aloud |
| Punctuation and sentence boundaries | Run-on paragraphs with no structure | Do not treat a paragraph break as a topic boundary; there are none |

**Never build a summary claim on a sentence that reads oddly.** An ASR artifact that produces a striking statement is the most common source of a confidently wrong media summary.

## Spoken vs Written Structure

Speech has no paragraphs, no headings, and no revision — which changes how to find the content.

- **The point follows a verbal marker**, not a position: "so the point is", "what I'd say is", "the thing people miss", "here's the takeaway". Scanning for these markers is more productive than reading linearly.
- **Speakers repeat their thesis** two or three times in different words. Repetition marks importance, unlike in edited prose where it marks bad editing.
- **The last five minutes carry the summary** the speaker made themselves — useful as a check on your ranking, not as your output.
- **Digressions can be entire subjects** with no signposting; a topic that returns after twenty minutes is one subject, not two.
- **Nothing is retracted cleanly.** A speaker who corrects themselves twenty minutes later leaves both versions in the transcript; the later one wins and the summary carries only it.

## By Format

| Format | The reader wants | Cut hardest |
|---|---|---|
| Interview podcast | The guest's claims and the one thing they said that nobody else says | Host's questions, rapport, sponsor reads |
| Two-host discussion | The disagreement and any concrete recommendation | Everything else; density is lowest here |
| Conference talk | The thesis, the evidence, the demo result | Introduction, self-promotion, live-demo troubleshooting |
| Lecture | Definitions, the derivation, the worked example | Administrative announcements, repetition for note-taking |
| Webinar / product demo | What the product does, limits, price, availability | Company history, customer-logo slides |
| Earnings call | Guidance, and the analyst Q&A — where the unscripted content is | Prepared remarks, which restate the release (`data.md`) |
| Audiobook / narrated nonfiction | Same as a book (`long-sources.md`) | Nothing genre-specific; use chapter marks as chunks |
| Voice memo | The instruction or decision the speaker recorded | Thinking-out-loud preamble |
| Anything else | The thesis and the evidence | Introductions, outros, and sponsor content |

## Slide Decks

- **Speaker notes, when present, are the real content**; the slides are prompts. Summarize notes first.
- **A bulleted slide is already a summary** — re-bulleting it is reformatting (SKILL.md Traps). Convert to the claim it stands for.
- **Charts and diagrams**: state what the chart shows and its axes; if precise values are needed and no data table exists, read them as approximate and say so (`data.md`).
- **Appendix slides carry the substance** in most business decks — the numbers deliberately left out of the main flow.
- **Slide count is not a proxy for content**: a 60-slide deck often carries five claims.

## Quoting

- A verbatim quote goes in quotation marks with the speaker, the timestamp, and no editing beyond removing filler — and removed filler is marked with an ellipsis.
- **Never repair a quote's grammar silently.** Speech is ungrammatical; a cleaned-up quote is a paraphrase wearing quotation marks.
- Paraphrase is the default; quote only where the exact wording is the point (a commitment, an admission, a number, a memorable formulation).
- For a public figure or a published source, an inaccurate quote is a reputational problem for whoever ships the summary, which is why the timestamp travels with it.

## Output Shapes

**Episode or talk:**
```
<Title> — <speaker(s)>, <runtime>, <date>. Source: <transcript type: official | ASR>.

Thesis: <one sentence>
Points:
- <claim> [MM:SS]
- <claim with number, copied> [MM:SS]
Disagreement: <if the format had one, who held which side>
Worth playing: <timestamp ranges where the audio beats the summary>
Omitted: <sponsors, digressions — one line>
```

**Lecture or course session** adds `Definitions:` and `Worked example: [MM:SS]`, both of which are what a student returns for.

**After summarizing media**, register the episode in `## Sources` in `~/Clawic/data/summarizer/memory.md` with its runtime, transcript type, and date; write the summary with its timestamps to `summaries/<show>-<episode>.md` when `store_summaries: full` — timestamps are the reason these summaries get re-opened; add every speaker name and term the transcript mangled to `glossary.md` in the same turn, so the next episode transcribes cleanly; and if the user follows the series on a cadence, add its row to `## Due`. Formats and thresholds: `memory-template.md`.
