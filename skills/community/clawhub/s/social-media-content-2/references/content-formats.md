# Content types, hooks and templates

## Content types

| Type | Purpose | Example angle |
|---|---|---|
| Educate | trust, saves | "3 mistakes in X and the fix" |
| Story | connection | what went wrong, what changed, the lesson |
| Proof | conversion | result with real numbers, a case study, before/after (real only) |
| Opinion | reach, debate | a clear stance with reasons, not outrage |
| Behind the scenes | humanise | how it is made, a day in the work |
| Offer | sales | who it is for, what they get, price or next step, deadline only if real |
| Community | loyalty | questions, polls, user content (with permission), FAQs |

Mix by the strategy's pillars (see `content-strategy`); do not make everything an offer.

## Hook patterns (adapt, do not copy verbatim)

- Result first: "We cut reply time from 4 hours to 30 seconds. Here is how."
- Mistake: "The biggest mistake in [topic] is [specific]."
- Contrast: "Everyone says X. The data says Y."
- Question the reader is already asking: "Why do customers leave at checkout?"
- Number and promise: "5 checks before you publish a post."
- Story opener: "Last Tuesday at 2 AM, a customer wrote to us..."
- Myth: "You do not need [expensive thing] to [result]."

Rules: promise only what the post delivers; avoid fake urgency; no all-caps shouting; test 2 hooks when stakes are high.

## Post templates

**Instagram caption.** Hook line. 2 to 4 short lines of value. One example or number. CTA ("Save this for later" if it is reference material). 3 to 5 relevant hashtags or keywords if the brand uses them.

**Carousel (7 to 10 slides).** Slide 1 promise (big text, 6 to 9 words). Slides 2 to N-1: one point per slide, a headline plus 1 to 2 lines. Last slide: recap and one CTA. Write alt text and a caption that adds, not repeats.

**LinkedIn post.** Line 1 to 2: the hook. Context in 2 to 3 short paragraphs. The insight or steps (3 to 5 bullets at most). The takeaway. A question or soft CTA. No hashtag wall.

**X thread.** Post 1: a hook that stands alone and states the payoff. Posts 2 to N: one point each, a concrete example per point. Last: recap and one action. Keep each post under the limit (`thread` command).

**Short video caption.** One line that adds a keyword and a question; on-screen text carries the hook (script it with `short-form-video-scripts`).

**Community reply.** Acknowledge the specific point, answer or ask one clarifying question, move helpful detail to DM only when private data is involved. Match the brand voice; never argue with trolls; escalate complaints and safety issues to a human.

## Repurposing matrix (one source, many pieces)

| Source piece | Output | Change of angle |
|---|---|---|
| 10-minute video | Reel/Short clip, carousel of the steps, X thread, LinkedIn story, quote graphic, 2 community questions | each uses a different moment or takeaway |
| Blog article | thread, carousel, LinkedIn post, newsletter teaser, FAQ replies | lead with the strongest insight, not the intro |
| Case study | proof post, "what we learned" story, short testimonial video (with consent) | numbers and the customer's words (real, permitted) |
| Product update | announcement post, "how to use" short, behind-the-scenes post | benefit first, feature second |

## Content pack JSON

The pack format is described at the top of `scripts/content_tools.py`: one object per post with `platform`, `format`, `text`, `hashtags`, `media` (with `alt`), `cta`, `link`, `notes`. Keep placeholders such as `[X%]` visible in the text so they cannot be posted by mistake; the check will not catch them, so search for `[` before delivering.

## Test ideas (when the user wants to learn what works)

Change one thing per test: hook wording, format (carousel vs Reel), CTA type, posting time, length. Run the same test across at least 5 to 8 posts before concluding, compare saves, shares, comments and clicks rather than likes alone, and record results (use the `analytics` skill if available).
