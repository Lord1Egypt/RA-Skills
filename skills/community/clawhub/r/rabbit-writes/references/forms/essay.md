# Form: essay

**Register:** `formal`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

An essay is the form where structure is the argument. Nothing else here rewards ordering as much, and nothing else punishes a missing one as visibly.

## Slots

- **Title.** One line. It names the claim or the question, not the topic.
- **Opening.** The claim, the question, or the thing that makes the question worth asking. One of the three, and the voice decides which.
- **Body.** Sections in an order that a reader could not shuffle without losing the argument. This is the test the form is built around, and it is the one to run before anything else: if the paragraphs could be reordered and the piece would read the same, there is no argument in it, only a list of observations about one subject.
- **Turn.** The place where the strongest objection gets stated in its own words and answered. Optional in a short essay and essential in a long one.
- **Close.** What follows from the argument. Not a summary of it.

Headers earn their place past roughly 1,200 words, or wherever a reader would reasonably want to leave and come back. Below that they usually mark a structure that the prose should have carried on its own, and a reader who needs a header to know where the argument turned is a reader the argument lost.

## Bands

| Purpose | Band |
|---|---|
| A short argument, one claim | 800 to 1,500 words, no headers |
| A full essay | 1,500 to 4,000 words, headers where the argument turns |
| A chapter | no cap, and the section structure is part of the outline |

Paragraphs vary hard. An essay is the form where uniform paragraph length reads worst, because a paragraph is a unit of thought here rather than a unit of layout, and thoughts are not the same size.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "In this essay, I will argue that." The essay is the argument. Announcing it spends the opening on scaffolding.
- "In conclusion" and "To sum up."
- "It is important to note that" and "It is worth mentioning that."
- The five-paragraph shape: an intro that states three points, three paragraphs that state them again, a conclusion that states them a third time.
- A section per subtopic where the subtopics have no order between them. That is a survey with essay formatting on it.
- A rhetorical question opening every section.
- Headers on a 900-word piece.
- An objection raised only in a form weak enough to knock down.

## What the mechanical layer sees here

This is the one form where the mechanical layer has enough text to say something. An essay clears the reliability floor comfortably, so burstiness, sentence-length variation, and paragraph spread are all measuring something real, and the uniform-paragraph rule runs at full strength here where the tolerance matrix skips it in `docs` and `chat`.

The `formal` rung's extra-strict cells apply, and the one to watch is significance inflation. An essay that keeps telling the reader a point is surprising has stopped making the point.

Where the voice has a fingerprint, `attain.py --plan` gives a per-paragraph sentence shape. Read it as a band and never as a script: hitting the median on every sentence is the uniformity the shape target exists to break.
