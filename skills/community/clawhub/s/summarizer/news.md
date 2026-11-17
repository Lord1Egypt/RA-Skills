# Articles, Press Releases, and Journalism

Scope: one news article, blog post, press release, wire story, op-ed, or magazine feature at a time. Several sources on one story is `multi-source.md`; a scheduled feed of them is the `digest` skill.

**Before summarizing an article about a story the user follows**, read `~/Clawic/data/summarizer/glossary.md` for the organization, person, and product names already pinned — the same entity written two ways across two stories reads as two entities — and `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index) for what was already reported: a re-announcement is only visible against the earlier item and its event date.

**Contents:** [The One Genre Where Lead-First Is Right](#the-one-genre-where-lead-first-is-right) · [The Five Slots](#the-five-slots) · [Press Releases](#press-releases) · [Padding to Delete](#padding-to-delete) · [Sourcing and Certainty](#sourcing-and-certainty) · [Opinion and Analysis](#opinion-and-analysis) · [Blog Posts and Long-Form](#blog-posts-and-long-form) · [Numbers in News](#numbers-in-news) · [Output Shapes](#output-shapes)

## The One Genre Where Lead-First Is Right

News is written in the inverted pyramid: the most important facts first, descending to background, so an editor can cut from the bottom. This is the only genre in this skill where reading the opening and stopping is a defensible strategy.

- **The first two paragraphs usually contain the entire summary.** The rest is quotes, context, and history.
- **Cut from the bottom, not from the middle.** The tail of a news story is designed to be removable.
- **Exception: the feature and the magazine profile** invert this — they open with an anecdotal scene and bury the thesis a third of the way in. If the first paragraph is a scene rather than a fact, the pyramid does not apply and you read for the "nut graf", the paragraph that states what the story is about.
- **Exception: the correction or update note**, usually at the top or the bottom, which can invalidate the body. Always check both ends.

## The Five Slots

Every news summary answers these, and states plainly which ones the article did not answer.

| Slot | Note |
|---|---|
| What happened | The event, not the reaction to it |
| Who | Named entities; a company's action is not its CEO's statement |
| When | The event date, which is often not the publication date — a story published today about last month's filing is not news of today |
| Why it matters / why now | The trigger; without it a reader cannot judge relevance |
| What is next | The pending decision, deadline, or scheduled event — usually the only actionable line |

An unanswered slot is stated: "the article does not say when the change takes effect" is more useful than silence, because it tells the reader not to keep looking.

## Press Releases

A press release is an interested party's summary of itself. Treat every claim as attributed (SKILL.md Rule 4) and expect a fixed structure.

| Element | Handling |
|---|---|
| Headline and subhead | The claim the issuer wants repeated; never state it in your own voice |
| Boilerplate ("About <Company>") | Delete entirely |
| Executive quotes | Almost never contain information; delete unless a quote makes a commitment or a number |
| Superlatives ("leading", "revolutionary", "first-ever") | Delete; if a "first" is load-bearing, say who claims it |
| Numbers | Keep with their basis; growth rates without a base are a red flag worth noting |
| What is absent | Price, availability date, capacity limits, and who the customer is are the four most commonly omitted facts |
| Embargo or forward-looking note | Status travels with the claim |

A useful press-release summary is often three lines: what was announced, what it costs and when it is available, and what the release does not say.

## Padding to Delete

| Padding | Why it exists |
|---|---|
| Background paragraphs recapping earlier coverage | Written for readers arriving cold |
| "According to a statement" boilerplate | Attribution can be compressed, not the attribution itself |
| Reaction quotes that add no fact | Column inches |
| Stock-price movement in a non-financial story | Reflex |
| SEO restatement of the headline in paragraph one | Search optimization |
| Related-links and newsletter interruptions | Advertising |
| Speculation attributed to unnamed "observers" | Filler; if there is a named analyst with a number, keep that |

## Sourcing and Certainty

Compression flattens sourcing, which is exactly what determines how much weight a reader should put on a claim.

| Article says | Summary says |
|---|---|
| "according to two people familiar with the matter" | "reported on the basis of anonymous sources" |
| "the company confirmed" | "confirmed by the company" |
| "the filing shows" | "per the filing" — documentary, the strongest form here |
| "sources say the company may" | Keep both the sourcing and the modal; this is a rumor |
| "the company did not respond to a request for comment" | Keep — it tells the reader the account is one-sided |
| Reporting another outlet's reporting | Name the original outlet; a chain of aggregation is one source, not three |
| Update or correction appended | Report the corrected version and note that it was corrected |
| Anything else | Carry the article's own sourcing phrase, compressed but not removed |

## Opinion and Analysis

- **Separate the reported facts from the argument.** An op-ed's factual claims can be summarized as facts; its conclusions are summarized as the author's position.
- **Name the author and their affiliation** when the affiliation is relevant to the argument — an industry-association byline is part of the content.
- **The strongest counter-argument the piece addresses** is worth a line; it is what distinguishes an argued piece from an assertion.
- Never merge an op-ed's conclusion into a news summary of the same event.

## Blog Posts and Long-Form

- **Technical blog posts** front-load context and bury the result; the summary leads with the outcome and the numbers. Code blocks are referenced, not reproduced.
- **The "we migrated X to Y" genre**: the summary is the before/after numbers, the reason, and the thing that went wrong — not the narrative.
- **Company engineering blogs** are recruiting material as well as documentation; scale claims are attributed.
- **Newsletters** frequently bundle several unrelated items; treat each item as a separate source and summarize the ones that match the user's interest, naming how many you skipped.

## Numbers in News

- Journalism routinely reports relative change without a base ("up 40%"). Say "up 40% from an unstated base" rather than repeating a number that cannot be interpreted.
- Round numbers in headlines are usually rounded in the body too — keep the body's figure.
- A poll needs its N, its field dates, and its margin of error; without them the summary says so (`data.md`).
- Currency conversions in the article are the article's, at its own date — keep the original currency alongside.

## Output Shapes

**Single article, brief:**
```
<What happened> — <who>, <when it happened>, per <outlet>, <publication date>.
Why now: <trigger>
Next: <pending decision, deadline, or scheduled event>
Not stated: <the slot the article left empty, if it matters>
```

**Press release, brief:**
```
<Issuer> announced <what>. Available <when>, priced <what, with currency>.
Claimed: <the issuer's headline claim, attributed>
Not stated: <price | availability | capacity | customers>
```

**After summarizing an article the user is tracking**, register it in `## Sources` in `~/Clawic/data/summarizer/memory.md` with outlet, publication date, and event date so a later edition can dedup against it (`recurring.md`); write the summary to `summaries/<topic>-<date>.md` when `store_summaries: full`; and add any organization, person, or product name that will recur to `glossary.md`. Formats and thresholds: `memory-template.md`.
