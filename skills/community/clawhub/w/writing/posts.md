# Posts, Essays and Articles — Long-Form for a Reader Who Can Leave

Scope: pieces published to an audience that did not ask for them — blog posts, essays, op-eds, newsletter issues, guest articles. Short-form channels are `social.md`; conversion-driven pages are `copywriting`; the distribution plan is `content-marketing`.

**Before writing for a publication, client, or recurring outlet**, read its `style-sheets/<context>.md` (word cap, section requirements, banned claims, byline rules) and `pieces/<year>.md` — the second one answers "have we already published this angle", which is the mistake nobody catches until after publication.

**Contents:** [The Reader Can Leave](#the-reader-can-leave) · [Hooks](#hooks) · [Headlines](#headlines) · [Scannability](#scannability) · [Evidence](#evidence) · [The Newsletter Issue](#the-newsletter-issue) · [The Op-Ed](#the-op-ed) · [Pitching an Editor](#pitching-an-editor) · [Publishing Mechanics](#publishing-mechanics)

## The Reader Can Leave

Every structural rule in this file follows from one asymmetry: an email's reader has a reason to finish, and a post's reader does not. The reader is deciding whether to continue at the headline, at the first sentence, at the first subhead, and at every scroll.

- **State the payoff early.** Withholding the conclusion to create suspense works in fiction and loses non-fiction readers. Say what the piece will establish, then establish it.
- **One idea per piece.** A post making two arguments gets remembered for neither. The second idea is the next post, and it is easier to write because you have already done the thinking.
- **Front-load the value.** The best paragraph should not be in the middle. Readers who leave at 40% should already have got something.
- **Write the piece you can defend.** A post that overstates gets one reading and a permanent asterisk. Calibrate the claim to what you can actually show (`evidence`, below).

## Hooks

The opening's only job is to make the second sentence unavoidable. Lead types and their risks are in `structure.md`; what is specific to published posts:

- The hook must be true to the piece. A dramatic opening on a piece that turns out to be a listicle is the fastest way to lose a returning reader.
- Two sentences of scene is the budget for a business post; four for an essay. Beyond that the reader who came for the answer starts scrolling.
- The strongest hook in non-fiction is a specific number or a specific loss: "the migration took six weeks and we did it twice" outperforms any question.
- If the piece has a counterintuitive claim, the hook is the claim. Do not save it.
- Delete the first paragraph and re-read. Throat-clearing is invisible to its author and obvious to everyone else (`structure.md`).

## Headlines

- Specific beats clever, always, outside of humour writing. The reader is choosing from a list, and the specific title tells them what they get.
- The title makes a promise; the piece must pay it. A title that oversells produces a reader who finishes annoyed and does not return.
- Front-load the load-bearing noun: feeds, search results and link previews truncate, and the cut point varies by surface. The first ~40 characters decide.
- Patterns that reliably work, and what they owe the reader:

| Pattern | Example shape | Must deliver |
|---|---|---|
| Number + noun + outcome | "Three settings that halved our bill" | Exactly three, and the number |
| How we / how to + specific result | "How we cut deploy time to four minutes" | The actual method, not principles |
| The counterintuitive claim | "Most retries make outages worse" | The argument, not a hedge |
| The named mistake | "The read-modify-write bug nobody sees" | A concrete reproduction |
| The comparison with a verdict | "Postgres or DynamoDB for this workload" | A recommendation, not "it depends" |

- Write five headlines and pick one. The first is always the descriptive one and it is rarely the best.
- Never a title that requires reading the piece to understand. Curiosity gaps work on feeds and cost trust everywhere else.

## Scannability

Assume the first pass is a scroll. The piece must survive being read as headline + subheads + bolded phrases + first lines.

- **Subheads state something.** A reader who reads only your subheads should get the argument (`structure.md`). This is the single highest-leverage edit on any post.
- One subhead every 200-300 words; none under 500 words total.
- Bold the claim, not the keyword. Bolding for SEO makes a page look machine-made and helps nobody.
- Lists are for genuine enumerations. A list of full sentences that flow into each other is a paragraph wearing a costume — and it reads as filler.
- One image or code block per major section maximum; each must be readable at phone width.
- Paragraphs of three to four sentences online. On a phone that is already half a screen.

## Evidence

What separates a post that gets cited from one that gets skimmed:

- **A number with a source beats an adjective.** "Slow" is an opinion; "4.2s at p95, measured over a week" is a claim.
- **Name the method** when quoting your own measurement: what, over what period, on what. A number with no method is decoration and readers who know the field can tell.
- **Link the primary source**, not the article summarising it. Chains of secondary citations are where numbers mutate.
- **Never invent a statistic, a quote, a date or an attribution** to strengthen a point. This is the one failure that is unrecoverable after publication, and it is trivially checkable by anyone who cares. Use `[TK]` and find the real one (`drafting.md`).
- Distinguish what you measured, what you read, and what you believe. Readers forgive a labelled opinion and never forgive an unlabelled one.
- Screenshots of a number age badly: date them in the caption.

## The Newsletter Issue

- One idea per issue. A newsletter that covers four things trains the reader to skim, and skimmers unsubscribe at the first busy week.
- Standing furniture — a fixed opening block, a fixed closing block — is what makes an issue feel like an issue. Decide it once and write it into that newsletter's `style-sheets/<context>.md`.
- The subject line follows email rules, not headline rules (`emails.md`): identifying noun first, no curiosity gap, searchable in six months.
- Above-the-fold is real in email: the idea must be visible before any preamble, because most clients show only the first screen in preview.
- Cadence beats length. A short issue on schedule outperforms a long one late, and the cadence belongs in the `## Due` table of `memory.md`.
- Every issue ends with one thing the reader can do — reply, read, try. A newsletter with no ask is a broadcast, and its reply rate is the health metric that matters.

## The Op-Ed

- The claim goes in paragraph one, unhedged. An op-ed that reaches its claim in paragraph four has already been cut by the editor.
- Three supporting arguments, strongest first (`structure.md`), each in its own paragraph or two.
- Concede the best counterargument explicitly. An op-ed that ignores the obvious objection reads as unserious.
- Outlets publish their own word limit and it is enforced — usually in the 600-800 range for a standard op-ed slot. Find the outlet's submission page, write to that exact number, and record it in that outlet's `style-sheets/<context>.md`.
- End on what should happen, naming who does it. An op-ed without an addressee is an essay in the wrong venue.
- Timeliness is the price of entry: the piece must attach to something that happened this week.

## Pitching an Editor

- The pitch is three paragraphs: the story in one sentence, why it matters now, why you are the person to write it. Under 200 words total.
- Send the argument, not the topic. "A piece about remote work" is not a pitch; "Remote work made the manager's job unfalsifiable, and here is the evidence" is.
- Name the section and the length you are proposing. It shows you read the publication and makes the yes cheap.
- One pitch per email. Attach nothing; link to two published pieces if you have them.
- Follow up once, after roughly a week. Then the pitch is free to go elsewhere — say so if you re-pitch it.
- Read the outlet's contributor guidelines and its last month of published pieces before pitching. Both are public and skipping them is visible in the first line.

## Publishing Mechanics

- Every piece needs: a title, a one-line description for link previews and search results, and an image or none deliberately. The description is written, not auto-generated from the first sentence.
- Check the rendering in the destination before publishing: line breaks, smart quotes, code blocks and em-dashes all mutate between editors and CMSs.
- Links open in the same tab unless the destination is a tool the reader will return from; forcing new tabs is a house-style decision, not a rule.
- Anything time-sensitive gets a visible date. An undated post is unusable to a reader trying to judge whether it still applies.
- Corrections after publication are appended and dated, never edited in place without a note, whenever the change alters a fact.

**After a piece ships**, write its row to `pieces/<year>.md` — date, title, format, where, words, and the outcome once it is known — and delete its row from `## Pieces` in `memory.md`. **When an outlet's requirement is discovered** (word cap, section order, banned claim, byline rule), write it to that context's `style-sheets/<context>.md` in the same turn, with the date (`memory-template.md`).
