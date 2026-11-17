# Condensing and line-break rules

Subtitles are a reading aid, not a record. Condense only after timing is
fixed, only the cues the `--todo` file lists, and only as much as
`chars_to_cut` asks for. A cut of a few characters is usually one word.

## What to remove first

1. Fillers and hedges: "you know", "basically", "I mean", "like", "sort of",
   "actually", "so" at the start; 那个、就是、然后、其实、对吧.
2. False starts and repeated words: "I— I think" → "I think".
3. Redundant addressing and tags: "All right, Mark, this is cool" →
   "Mark, this is cool"; "..., right?" when the question is clear.
4. Long forms with a short equivalent: "in order to" → "to", "at this point
   in time" → "now", "a lot of" → "many".
5. Restated content the picture already shows.

## What never to change

- Names, numbers, dates, units, product names.
- Negations ("not", "never", 不、没) and modal strength ("must" vs "may").
- Who says what. Do not move words across a speaker change.
- The meaning of a joke or a key line. If it cannot be shortened safely,
  leave the cue over the limit and say so.
- Verbatim, legal, medical and archival transcripts: do not condense at all.

## Line breaks

When a cue needs two lines:

- Break after punctuation, or before a conjunction or preposition.
- Do not split an article from its noun, an adjective from its noun, a first
  name from a last name, or a verb from its particle ("turn / on").
- Prefer a bottom-heavy shape: the longer line underneath.
- Chinese/Japanese: break at punctuation or between phrases, never inside a
  word; full-width punctuation at a line end is allowed.

## Splitting a cue

A cue too long for two lines is split into two cues at a sentence or clause
boundary. Each part must make sense on its own. Without word timings, let
`apply` share the time by character count; with them, set the split time to
when the second part starts being spoken.
