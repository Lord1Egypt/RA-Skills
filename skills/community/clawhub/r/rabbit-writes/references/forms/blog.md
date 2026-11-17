# Form: blog

**Register:** `blog`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

A public post on a site the writer controls, found by search or a link rather than delivered. It is the neutral default of the whole register set: every rule runs at full strength except the two that describe a conversation, so a document with no strong form signal lands here and gets the strictest reading that is not extra strict.

If the piece is delivered to subscribers, it is a newsletter and `forms/substack.md` applies. If it is arguing rather than explaining, `forms/essay.md` applies. If it is mostly code and API surface, `forms/technical-blog.md` applies.

## Slots

- **Title.** One line, naming what the reader gets.
- **Opening.** The thing the post is about, in the first two sentences. A reader who arrived from a search result is deciding whether this page answers their question, and they decide fast.
- **Body.** Sections with headers past roughly 800 words. Below that the prose carries it.
- **Close.** What follows, or what to do next. Optional, and an absent one beats a manufactured one.

## Bands

| Purpose | Band |
|---|---|
| A short post, one point | 500 to 900 words, no headers |
| A standard post | 900 to 2,000 words, headers |
| Past 2,000 words | it needs a contents block or it needs splitting |

Paragraphs vary. Three to five sentences is the middle of the range and the range is what matters, since uniform paragraph length runs at full strength in this register.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "In today's fast-paced world" and every variant that opens on the state of the world.
- "Whether you're a beginner or an experienced developer."
- "Let's dive in."
- "But what does this actually mean?" as a section header.
- A closing section that summarizes the post under a header naming it a conclusion.
- Three sections of equal length under three headers of equal grammatical shape.
- A list of five things where the fifth exists to make it five.

## What the mechanical layer sees here

Everything runs. This register relaxes nothing and skips only wall-of-text replies and curly quotes, so a scan under `blog` is the closest the engine gets to reporting on prose without a context allowance. That is why it is the default: a document that has not been identified gets read strictly rather than leniently, and a wrong guess costs a false report instead of a missed one.

A post of this length clears the reliability floor, so burstiness, type-token ratio, and paragraph spread all mean something here.
