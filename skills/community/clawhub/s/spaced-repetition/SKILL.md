---
name: Spaced Repetition
slug: spaced-repetition
version: 1.0.0
homepage: https://clawic.com/skills/spaced-repetition
description: Scheduling review of material at expanding intervals to optimize long-term retention.
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Mechanism: retrieval is the active ingredient

Spacing is the schedule; retrieval is the drug. Spacing rereading barely beats massed rereading; the retention gain lives in forcing recall, then checking.

- Active recall first, feedback second: the act of pulling the answer out (not reading it) is what consolidates. A card where you peek before trying is a reread, not a review.
- Testing effect size: retrieval beats rereading by ~2x at a one-week delay, and the gap widens as the delay grows (Roediger/Karpicke). The longer the gap, the more retrieval pays.
- Desirable difficulty: a review you struggle slightly to recall consolidates more than one that is instant. A card always answered in <1s is over-reviewed; one you always fail is under-learned or badly written.
- Recognition vs recall: multiple-choice and "looks familiar" build familiarity, not retrievability. Build cards that demand production (type the answer, say it aloud), not yes/no recognition.
- Recollection, not familiarity, is the goal: SR defeats the illusion of knowing (you reread, it feels known, you cannot produce it). The proof of learning is reproducing the answer unaided.
- No retrieval, no spacing benefit: passive re-exposure on a spaced schedule (re-reading notes every few days) yields a fraction of the gain. If you cannot make yourself retrieve, the schedule is wasted.
- Feedback must be honest: grade against the real answer before marking known. Self-flattery ("I basically had it") is the silent killer; the curve punishes lenient grading within a week.

## The forgetting curve and interval ladder

- Curve shape: steepest in the first 24h. Nonsense-syllable retention drops to ~33% within a day and ~25% within a month (Ebbinghaus); real meaningful material decays slower, but the early-steep shape holds.
- The first review is the highest-leverage: skipping day-1 review loses the most. The schedule front-loads reviews because that is where decay is fastest.
- Expanding beats equal spacing for a fixed review budget: 1, 3, 7, 14, 28 beats 5, 5, 5, 5, 5. Expanding catches early decay, then spends reviews where decay has slowed.
- A typical first ladder (SM-2-ish): 1d -> 3d -> 7d -> 14d -> 28d -> 60d -> 120d. Not a law; the algorithm adjusts the next interval from your grade.
- The interval is a prediction of when you are about to forget, not a target to hit. Shorter-than-expected means you forgot, the interval was too long. Longer-than-expected and still easy means intervals are too short.
- "About to forget" is the review moment: reviewing when recall is effortful but successful consolidates best. Reviewing when recall is instant wastes a slot; reviewing after you have forgotten relearns, does not reinforce.
- Do not pre-empt the schedule: reviewing early "to be safe" collapses intervals and multiplies load. Trust the algorithm; if retention is off, fix the target or the card, not the timing.

## Algorithms: SM-2 vs FSRS

- SM-2 (Anki's legacy engine, from SuperMemo, 1987): each grade multiplies the interval by an ease factor; ease drifts up on "easy", down on "hard". No target retention; the schedule is a heuristic.
- SM-2 weakness: ease inflates on early easy cards then never recovers, producing absurd intervals (a card "known" after three easy taps lands at a 6-month interval you will actually fail). Interval explosion is the tell.
- FSRS (Free Spaced Repetition Scheduler): optimizes to a desired retention (default 0.9) via 19 parameters fit to your personal review history. Replaces SM-2 in Anki as of ~2024; strictly better once you have ~1k reviews logged to fit on.
- FSRS needs history: on a fresh profile with <1000 reviews it falls back to defaults; the fit improves as data accumulates. Do not judge FSRS on the first week.
- Set desired retention to 0.9 unless you have a reason. 0.85 = fewer reviews, more forgetting; 0.95+ = review load balloons. 0.97 costs ~2x the reviews of 0.90 (FSRS).
- Retention target is the lever, not the interval: decide how much you can afford to forget, set the target, let the algorithm produce the intervals. Hand-tuning intervals per card is the #1000's rabbit hole.
- Re-grade on actual recall, not difficulty feeling: marking "hard" because you disliked the question inflates load. Mark hard only when recall was slow or partial, not when the card annoys you.
- Migration: SM-2 -> FSRS re-estimates intervals from history; expect some cards to jump shorter (they were over-scheduled) and some longer (under-scheduled). Let it settle a month before judging.

## Card design

- One atomic fact per card: a card with three things to recall fails as one. If you miss one, you fail all three and cannot tell which. Split into three cards; review cost is the same, signal is clean.
- Minimum information: the question should be answerable in a word or short phrase. A paragraph on the answer side means you are not testing recall, you are re-reading.
- Cloze (fill-the-blank) for facts inside a sentence; Q&A for concepts needing a produced answer. Cloze is faster to author and good for lists and definitions; Q&A for anything where the blank gives away the answer.
- Context-sufficiency: the card must make sense without the deck around it. A card that reads "the third one" only works in its original list; six months later it is opaque. Write the full question on the card.
- Avoid yes/no and "did you understand": recognition, not recall. "Is X true?" lets familiarity pass. Force production: "What is X?"
- Reverse cards for bidirectional facts: capital -> country and country -> capital are two cards. Language, names, and pairs need both directions or you build one-way recall.
- Interference kills: near-synonyms (two foreign words for "big"), adjacent numbers (cranial nerves), similar formulas. If you keep confusing two cards, they interfere: merge, distinguish with a mnemonic, or stagger them apart.
- Images where they earn it: anatomy, maps, diagrams. A labeled image beats a sentence for spatial and visual facts. Do not decorate; an image earns its place only if recall depends on it.
- Do not copy textbook paragraphs as cards: they fail the atomic test and you will suspend them within a month. Pre-process: read, understand, then write 5-10 atomic cards capturing what you would want to recall in a year.
- Source on the card: tag with origin so you can fix it when it is wrong. A card with no source cannot be audited; six months later you will not know if you misremembered the fact or the source did.

## Review economy and target retention

- The marginal-retention curve is steep above 0.9: each 1% of desired retention above 0.90 adds ~10% more reviews (FSRS). 0.97 is roughly double the load of 0.90 for ~7% more remembered.
- Sustainable new-card rate: 10-20 new/day for a serious learner; each new card generates ~7-10 reviews over its first month. 50 new/day buries you within weeks.
- The steady state: at 0.9 retention with steady additions, daily reviews settle around 7-10x your daily new-card count. 20 new/day -> ~140-200 reviews/day at equilibrium.
- Backlog is the failure mode: missing days compounds. A 3-day miss on a 150/day habit = 450 backlogged, which you will rush-grade (lenient, useless) or abandon. Daily, even if short, beats binge.
- Cap reviews if you must, never new cards: cutting new cards keeps the deck from growing; cutting reviews lets the backlog rot. If overloaded, freeze new cards and grind reviews to zero first.
- Review time budget: a mature card takes ~5-8s; a new or failed card 15-30s. 100 mature reviews ~10-15 min; 100 new or failing ~30-40 min. Budget by composition, not count.
- Grade honestly even when slow: a review you got right-but-slow is "hard", not "good". Lenient grading under time pressure is the main reason decks silently rot.

## Leeches, ease hell, and failure modes

- Leech: a card you fail repeatedly. Anki flags at 8 lapses by default. A leech means the card is broken, not that you are dumb; fix or kill it.
- Leech fixes, in order: rewrite it smaller, add a mnemonic, add an image, split it. If it still leeches after a rewrite, suspend it: one bad card drains disproportionate time.
- Ease hell (SM-2): ease factor driven to its 1.3 floor by repeated "hard" grades, so intervals barely grow and the card reviews daily forever. Symptom: a card you have seen 30 times still at a 1-day interval.
- Ease hell fix: reset the ease (Anki: set due date + reset, or migrate to FSRS which has no ease floor). The root cause is usually a badly-written card or chronic lenient-then-panicked grading; fix the card.
- The lenient-grade trap: marking "good" on a slow recall to keep the deck moving inflates intervals, then you fail the card a week later, hammer ease, enter hell. Grade by recall quality, not by desired speed.
- Over-learning a failed card: re-learning it 5x the same day does not help retention; it trains short-term memory. One clean recall, then let the schedule carry it.
- Deck bloat: pre-made decks of 10k cards feel like progress; the math says you will never review them all. The #1 adds cards they have already engaged with, not decks to "cover later".
- Suspended-card debt: suspending instead of deleting accumulates a graveyard you will never revisit. Periodically delete, not just suspend.

## When spaced repetition is the wrong tool

- Physical skills (serving a tennis ball, intubation): SR schedules recall of facts, not motor patterns. Motor learning needs massed, varied, feedback-driven practice, not spaced recall.
- Procedures you use daily: if you do it every day, the job is the review; adding SR cards for it is overhead. SR is for things you would otherwise forget.
- Understanding vs facts: SR holds facts and definitions; it does not build conceptual understanding. Learn the concept first (problems, explanation), then SR the facts you must recall cold.
- Anything you can look up faster than recall: a rarely-used API endpoint you will always have docs for is not worth a card. SR costs review time; spend it on what must be in your head.
- Near-term, then discard: material for a one-off task (a client's internal jargon for a 2-week project) does not deserve lifelong retention. Use it, drop it.
- Massive, rapidly-changing sets: a 5000-card med-school deck you will relearn on rotation is borderline; maintenance cost can exceed value. Prefer fewer, high-yield cards.

## Habit and daily load

- Daily, not "when I have time": the schedule assumes consistency. Two days on, five off collapses intervals and spikes load; the algorithm cannot fit your forgetting.
- One deck, one habit: reviewing across 8 small decks in scattered sessions erodes the habit. Consolidate into a daily review you do at a fixed time.
- Review before adding: new cards compete for today's time with due reviews. Clear due first, then add new within your budget.
- Mobile for reviews, desktop for adding: the friction of card creation belongs at a desk where you think; review is a 5-second-per-card loop you do anywhere.
- Set a daily new-card ceiling and hold it for months: the temptation after a motivated weekend is to add 100; that is borrowing reviews from future-you at interest.
- Audit the deck quarterly: delete leeches, rewrite confusing cards, check retention stats. A deck that is never audited decays toward a pile of cards you fail and ignore.
- Do not review when exhausted: a tired review is a lenient review. Better to halve the load than to speed-grade 300 cards into uselessness.

## Situations

| Situation | Play |
|---|---|
| 500+ reviews backlogged | Freeze new cards, set a review cap you will actually do daily, grind to zero over 1-2 weeks. Do not binge-grade. |
| Failed the same card 4 times today | It is a leech in the making. Rewrite it smaller or split it; if still failing, suspend. |
| Learning a language with 50 near-synonyms | They will interfere. Add a distinguishing context to each card, or batch one synonym at a time over weeks. |
| Exam in 3 days | SR will not save you. Massed practice plus practice questions now; feed what stuck into SR after. |
| A card whose answer is a paragraph | It is not a card, it is a note. Break into 5-8 atomic cards or delete it. |
| Reviews take >45 min/day | Lower desired retention to 0.85, cut new cards, or accept it. Load is a function of deck size and target. |
| Want to learn to intubate | Wrong tool. Massed, supervised motor practice with feedback; SR only for the facts around it. |
| Switching SM-2 to FSRS | Enable FSRS, let it optimize on existing history, keep retention at 0.9, wait a month before judging intervals. |
| Two cards you keep swapping answers to | Interference. Merge into one card, add a distinguishing mnemonic, or stagger them. |
| Just added 80 new cards in a day | Stop. You borrowed ~600 future reviews at interest. Cap at 10-20/day for the next week to absorb. |

## Where camps disagree

- **SM-2 vs FSRS**: SM-2 is simple, universal, no fit needed; FSRS optimizes to a retention target and beats SM-2 on review economy once you have ~1k+ reviews to fit on. FSRS wins for anyone with history; SM-2 only wins on a brand-new profile or a tool that does not support FSRS.
- **Cloze vs Q&A**: cloze wins for speed and lists (definitions, facts inside sentences); Q&A wins for concepts where the blank would cue the answer and for anything requiring a produced explanation. The line is whether the blank leaks the answer.
- **Pre-made decks vs self-made**: pre-made wins for bounded, high-consensus material (a country-capital deck, a drug-name deck); self-made wins for anything conceptual, because authoring is part of learning. Pre-made decks fail when the learner never engaged with the material first.
- **Cap daily reviews vs unlimited**: capping prevents burnout and the backlog death-spiral but truncates the schedule; unlimited stays on schedule but can overwhelm. Cap when load threatens the habit; uncap when you can sustain it daily.
- **Recognition vs recall grading**: recognition (flip-and-nod) is fast and lenient, builds familiarity; recall (produce before flipping) is slower, builds retrievability. Recall wins for anything you must produce; recognition is acceptable only for things you must merely recognize.

## Related Skills

Install with `clawhub install <slug>` if the user confirms:
- `anki` - the dominant SR app: FSRS, deck options, card templates, add-ons
- `memory` - the cognitive substrate: encoding, consolidation, the testing effect in depth
- `learning` - broader learning strategy SR plugs into; when to reach for SR vs alternatives
- `flashcards` - card authoring at scale: cloze design, shared decks, classroom use
- `notes` - the source material; atomic notes feed atomic cards
