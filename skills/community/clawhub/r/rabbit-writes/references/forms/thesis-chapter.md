# Form: thesis-chapter

**Register:** `academic`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

One chapter of a longer work, which is what separates it from `forms/research-paper.md`. A paper stands alone. A chapter has a chapter before it and a chapter after it, and most of what goes wrong in the form is a chapter written as though it did not.

The reader is an examiner reading the whole thing in sequence, looking for whether the argument accumulates. That is a different reader from a reviewer, and it is why a thesis tolerates length a journal would cut: the examiner wants the workings.

## Slots

- **Chapter title and number.** Naming the contribution, not the topic.
- **Opening link.** One or two paragraphs saying what the previous chapter established and what this one adds. The slot examiners notice by its absence, because without it a thesis reads as papers bound together.
- **Aim.** What this chapter settles, and which thesis question it serves.
- **Body.** Whatever the chapter's work requires. A methods chapter, a results chapter, and a theory chapter have nothing structurally in common past this point.
- **What this chapter establishes.** Stated as claims the later chapters may now use.
- **Closing link.** What the next chapter does with it.
- **References.** Usually collected at the end of the thesis rather than per chapter, and the institution decides.

A thesis by publication inverts the middle: each chapter is a paper, and the linking material carries the whole burden of making it one argument. The opening and closing link slots stop being courtesies there and become the thesis.

## Bands

| Purpose | Band |
|---|---|
| A literature or theory chapter | 6,000 to 12,000 words |
| A methods chapter | as long as the method, and the detail belongs in appendices |
| A results chapter | as long as the results, one per study or one per question |
| A discussion chapter | 5,000 to 10,000 words, and it is about the thesis rather than about the last chapter |

The institution's regulations outrank every number here, including the total, and they are worth reading before drafting rather than after.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "As mentioned in Chapter 3" used four times in one chapter, which is a sign the material is in the wrong chapter.
- "This chapter will discuss" followed by a table of contents for the chapter.
- "It is beyond the scope of this thesis" covering something a reader will expect.
- Restating the whole literature review in each chapter's introduction.
- A chapter that ends the moment the last result is reported, with nothing saying what it established.
- Hedging every claim to the point that the thesis makes no assertion an examiner could disagree with, which reads as having nothing to defend.
- A methods chapter written in the passive throughout to avoid saying who decided what. Somebody made the call. Say so.
- A discussion chapter that discusses the last results chapter and forgets the first.

## What the mechanical layer sees here

The `academic` register applies, and `docs/academic-corpus/README.md` has how it was calibrated. That corpus is papers rather than theses, which is the honest limit on how much the numbers transfer: a thesis is longer, more hedged, and written over years, so its register drifts within one document in a way a paper's does not.

A chapter clears the reliability floor by a wide margin, so burstiness, type-token ratio, and paragraph spread are all measuring something real. Low burstiness and trigram repetition are skipped in this register, which is right for the reasons the corpus showed, and it does mean the two structural signals most likely to catch a chapter drifting are switched off. Read for that by hand.

The measure worth running on a thesis is the one nothing else here uses. Where the voice has a fingerprint, `attain.py --plan` gives a per-paragraph sentence shape, and running it chapter by chapter shows whether chapter one and chapter six were written by the same person in the same register. Over a document written across three years, they frequently were not.
