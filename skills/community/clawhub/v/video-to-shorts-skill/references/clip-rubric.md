# Clip rubric

How to find the moments worth clipping in a transcript, score them and trim them. Score every
candidate; don't trust a first impression.

## Hard gates

Fail any one and the candidate is out, however good the line.

1. **The first sentence works with no context.** No "that", "he", "like I said", "so the second
   thing" pointing at something the viewer never saw. Start later if you have to.
2. **One complete idea.** It resolves, or stops on a deliberate cliffhanger at a natural beat.
3. **Length within limits** (below).
4. **No intro, outro, sponsor read, housekeeping or long crosstalk.**
5. **No music or footage the user doesn't own** in the window, especially in clips over 60 s.

## Score (0 to 100)

| Criterion | Points | What earns them |
|---|---|---|
| Hook | 25 | The first 3 seconds hold the most surprising, contrarian, high-stakes or specific line. It opens a question. |
| Stands alone | 20 | A stranger gets who, what and why without the episode. |
| Payoff or turn | 20 | A reveal, punchline, reversal, concrete takeaway or emotional peak before the end. |
| Emotion and energy | 15 | Laughter, conviction, disagreement, a vivid story, a voice that rises. |
| Specifics | 10 | Numbers, names, a concrete example, a small story with stakes. |
| Ending | 10 | Ends on a strong last line with no trailing filler; makes people watch again. |

- **70 and up:** ship.
- **55 to 69:** show the user as "maybe".
- **Below 55:** drop.

## Lengths

| | Length |
|---|---|
| Default target | 25 to 45 s |
| Allowed | 15 to 60 s |
| Story or explainer scoring 85+ | up to 90 s, if the payoff lands after 45 s |
| Any music or footage that isn't the user's | 60 s at most (YouTube blocks longer Shorts with a Content ID claim) |
| Hard limits | YouTube Shorts 3 min, TikTok through the API 3 min for everyone, Reels 15 min |

Over 40 seconds: put a turn or a new question around 15 and 30 seconds so people stay.

## Where to start and end

- **Start on the strongest line.** Speakers warm up ("I think one of the things that's been
  interesting is..."). Cut the warm-up when the clip still makes sense without it; if it doesn't,
  keep it short and let the on-screen hook carry the first seconds.
- **Don't repeat the hook.** If the hook text says "Save the crew, not the mission", the first
  spoken line shouldn't say the same words a second later.
- **End on the last strong sentence.** Drop "so yeah", "anyway", "and that's kind of it".
- **Snap to word edges.** Use the word timings in `transcript.json`; never cut mid-word.

## The hook text

The on-screen line for the first 3 seconds.

- 3 to 8 words, the clip's promise or tension in plain words.
- Specific beats clever: "Astronauts train so nothing surprises them" beats "This blew my mind".
- True to the clip. No bait the clip doesn't pay off, no words the speaker didn't mean.

## Spread across a batch

- No overlapping clips.
- Clips from across the whole video, not all from the first ten minutes.
- One clip per sub-topic unless both score 85+.

## Example

From the NASA interview in `examples/nasa-interview/` (public domain), three of the candidates:

| Clip | Window | Score | Why |
|---|---|---|---|
| Groundhog Day | 8:14 to 8:45 | 86 | Starts on the analogy ("if folks have seen that older movie..."), vivid, clear payoff |
| Safe path home | 3:38 to 3:54 | 82 | Quotable line, stands alone, concrete stakes; two "kind of"s cut |
| Curse our names | 1:15 to 1:40 | 76 | Funny, human, short; starts on "we're hopeful", skipping the warm-up |
| Training balance | 0:46 to 1:10 | 48 | Dropped: abstract, no payoff, opens with "And so" |
