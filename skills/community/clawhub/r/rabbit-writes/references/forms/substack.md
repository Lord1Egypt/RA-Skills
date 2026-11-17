# Form: substack

**Register:** `informal`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

Covers a newsletter issue and a personal blog post: public long-form with a named person behind it, arriving in an inbox or a feed rather than being searched for. The reader did not go looking for this, which is what separates it from an essay: the opening has to earn the next paragraph, and the writer is a person the reader subscribed to rather than an author they are evaluating.

## Slots

- **Title.** One line. It can be a hook here in a way it cannot be in an essay.
- **Standfirst.** One or two lines under the title saying what the reader gets. Optional, and the voice decides whether it exists at all.
- **Opening.** Concrete before abstract. A specific thing that happened, a number, a case, and then the idea it is an instance of. This is the form's main structural rule and it is the one most often skipped.
- **Body.** Sections, with headers that a reader skimming in an email client can navigate by.
- **Close.** What the reader should think or do. It may be personal here in a way it is not in an essay.
- **Subscribe or share line.** At most one, at the end, and it is a slot the register explicitly tolerates: the `informal` rung allows a single social endorsement closer where `blog` reports it. Two is the tell.

## Bands

| Purpose | Band |
|---|---|
| A short issue, one idea | 600 to 1,200 words |
| A standard issue | 1,200 to 2,500 words, headers throughout |
| A long piece | past 2,500 words, and it needs a standfirst saying so |

Paragraphs run short. Two to four sentences, because a large share of readers are in an email client on a phone, and the airiness that fragments an argument on a printed page helps here.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "Let's dive in" and "Let's unpack this."
- "Here's the thing:" as a paragraph opener, especially more than once.
- "I've been thinking a lot about X lately" as an opening, where nothing specific follows.
- "But here's what nobody tells you."
- More than one subscribe, share, or restack ask in a single issue.
- A one-sentence paragraph used three times in a row for emphasis. That is a cadence, not a rhythm, and it is the strongest structural tell in this form.
- Bold on a phrase in every paragraph.
- A rhetorical question as the title and again as the first line.

## Why the LinkedIn tolerances do not apply here

`forms/linkedin.md` sits on its own register, and that register relaxes bold hooks, two em dashes per post, and one or two emoji at the end of a heading. Those tolerances are about a feed that truncates a post after three lines and a platform where those marks are the local convention. None of that is true of an inbox. A newsletter is read in full or not at all, so the hook does its work in the title and the standfirst rather than in the typography, and `informal` keeps the em-dash rate and the emoji rules at full strength.

What `informal` does relax is the argument-adjacent set: one rhetorical question as a hook, one subscribe line, subjectless fragments, and copula avoidance, because a friendly public voice legitimately uses all four.

## What the mechanical layer sees here

A newsletter issue clears the reliability floor, so the stylometrics mean something and the uniform-paragraph rule runs at full strength. Two things worth checking beyond the scan. Tracking parameters, because a link pasted from a chat window carries them and the whole list receives it. And the fact check in `verify.py` after any edit pass, because a number that shifted in editing goes out to every subscriber at once and cannot be pulled back.
