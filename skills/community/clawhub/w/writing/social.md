# Social and Short Form — Posts, Threads, Bios, Comments

Scope: text written into a feed, where the competing content is one thumb-flick away and the format imposes hard limits. Growth strategy and campaign planning are `content-marketing`; conversion copy is `copywriting`.

**Before writing under a brand or a client's account**, read its `style-sheets/<context>.md` — claim boundaries, banned words, hashtag policy and who approves. Read `## Formats` in `~/Clawic/data/writing/memory.md` for the user's own channel habits.

## What Short Form Actually Costs

The constraint is not length; it is that the first line is the whole audition. Feeds truncate, previews collapse, and the reader is not obligated to expand anything.

- **Line 1 carries the payload**, not the setup. Put the claim, the number, or the result there — whatever survives being the only thing read.
- **No throat-clearing.** "I've been thinking about..." and "Here's a thread on..." spend the only line you were guaranteed.
- **One idea.** A post with two ideas gets engagement on the easier one and teaches nobody anything.
- **It must work with all formatting stripped.** Line breaks, bold and emoji render differently across clients and some strip them entirely.
- **Write for the reader who does not know you.** Feeds surface posts to strangers; a post that requires context from your last one is invisible to most of the people who see it.

## Channel Specs

| Channel | Hard limits | Where it truncates | Shape that works |
|---|---|---|---|
| X post | 280 characters on a standard account | Long posts collapse behind "Show more" | One claim, no link in the first post if reach matters to the user |
| X thread | 280 per post | Post 1 is what most people see | Post 1 works alone; one idea per post; last post states the takeaway, not "follow me" |
| LinkedIn post | Long posts allowed; the feed collapses behind "see more" after roughly the first three lines, and the break point differs on mobile and desktop | Before the fold | Payload in line 1, one-sentence paragraphs, one ask at the end |
| Comment or reply | Platform-dependent | Rarely | Add a fact or a disagreement; agreement with no addition is noise |
| Bio | 160 chars (X), ~220 (LinkedIn headline), varies elsewhere | At the limit, mid-word | Role → proof → current work, in that order |
| Anything else | Check the platform's own limit before writing to it | — | Line 1 payload, one idea, one ask |

Character limits change. When a post is near a limit, count it rather than trusting the number here, and record any limit that surprised you in that channel's `style-sheets/<context>.md`.

## Threads

- **Post 1 is the whole pitch.** If it does not work as a standalone post, the thread does not exist.
- One idea per post, and each post should be quotable alone — quoting a single post is how threads travel.
- Number them only if the count is fixed and stated in post 1. An unnumbered thread can be extended; a numbered one cannot without looking rushed.
- The last post lands the consequence. "Follow me for more" converts worse than a genuinely useful final line and costs the credibility of everything above it.
- A thread longer than about eight posts is an article that has been chopped up. Write the post, link it (`posts.md`).

## Bios

- Three lengths, agreeing with each other: 25 words, 50 words, 100 words. Store all three in `artifacts/bios.md`; they go out of date together and updating one is how they diverge.
- Order: what you do now → the proof someone would recognise → the hook. Past titles go last or nowhere.
- Third person for conference and byline use, first person for platform profiles. Keep both versions.
- No adjectives about yourself. "Experienced", "passionate" and "results-driven" are read as filler by every reader, including hiring managers.
- Update on the event, not on a schedule: new role, new project, new book. A bio naming a job you left is the most common professional writing error there is.

## Tone in Public

- The register that works is the user's real one, slightly tightened. A performed voice is detectable and it does not sustain.
- Disagree with the argument, name the person only if you are also citing them fairly. Subtweeting reads as cowardice to everyone who recognises the target.
- Never post at the peak of an emotion. The draft is fine; the send is the problem.
- Anything that could be read as speaking for an employer needs the employer's style sheet, not the user's voice (`voice.md`).
- Corrections are posted in the same thread, not edited in place without a note, whenever a fact changed.

## What Not to Do

| Habit | Why it fails |
|---|---|
| Engagement bait ("agree?", "thoughts?") | Attracts replies with no content and trains the audience to stop reading |
| Hashtag stacking | Reads as spam on every major platform; two topical tags is the ceiling where tags work at all |
| Reposting the same text across channels unchanged | Each channel's fold and register differ; the copy that works everywhere works nowhere |
| A thread with the payoff in the last post | Most readers never reach it; the payoff is the hook |
| Screenshots of text without alt text or a transcript | Unreadable to a portion of the audience and to search |
| Quote-posting to dunk | Amplifies the thing being criticised; the sample it reaches is mostly hostile |
| Automated cross-posting | Broken formatting and dead previews mark the account as unattended |

**When a channel convention is learned or a post format is settled** — a fold that cut a post short, a limit that bit, a structure that consistently works — write it to `## Formats` in `memory.md`, or to the channel's `style-sheets/<context>.md` if it is a brand or client rule. **A bio, standing intro, or reusable post template goes to `artifacts/<kebab-name>.md`** with its `## Boxes` line, in the same turn (`memory-template.md`).
