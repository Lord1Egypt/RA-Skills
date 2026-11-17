# Form: abstract

**Register:** `academic`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

The paper in one paragraph, for a reader deciding whether to read the rest and for the far larger number who will read nothing else. It is the most-read and least-revised part of most papers, which is the whole argument for treating it as a form rather than as a summary written last.

It is not an introduction. An introduction sets up what follows and depends on it. An abstract replaces the paper for most of its readers, so a number the reader needs is in it even if that number lives on page eleven.

## Slots

Two shapes, and the venue picks. **Structured** abstracts label the slots (Background, Methods, Results, Conclusions) and are the norm in medicine and health. **Unstructured** abstracts run them together as one paragraph and are the norm elsewhere. The slots are the same either way.

- **Context.** One or two sentences. What is known and where it stops.
- **Objective.** What this work set out to settle, stated as a question or an aim.
- **Methods.** Design, setting, participants or data, and scale. Enough that a reader can judge whether the finding could hold.
- **Results.** The finding, with the actual numbers and their uncertainty. Not a promise that results were obtained.
- **Conclusion.** What follows, at the strength the evidence supports and no further.

Keywords sit below and are chosen for how somebody would search, not for how the authors think about the work.

## Bands

| Purpose | Band |
|---|---|
| A journal abstract | 150 to 300 words, and the venue's cap is hard |
| A structured clinical abstract | 250 to 350 words under labelled headings |
| A conference abstract standing alone | 300 to 500 words, and then it is the whole submission |

One paragraph, no citations, no abbreviations that are not defined in it, and no reference to figures or tables in the paper. Those four are conventions strong enough to read as errors when broken.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "This paper presents" and "In this study, we investigate" as the opening, which spends the scarcest sentences in the paper on scaffolding.
- "Results will be discussed" and "The implications are discussed." Discuss them here.
- "Significant improvements were observed" with no effect size, no interval, and no baseline.
- "A novel approach" where the novelty is not stated.
- An abstract that describes the structure of the paper instead of its findings.
- A citation, which an abstract carries alone and cannot resolve.
- An undefined abbreviation, which a search result renders unreadable.
- A conclusion stronger than the results slot supports, which is the most common defect in the form and the easiest to check: read the two sentences next to each other.

## What the mechanical layer sees here

An abstract sits at or under the reliability floor `scan.py` reports, so burstiness, type-token ratio, and paragraph spread describe very little here. Ignore them and read the numbers instead.

What still applies is the `academic` register's vocabulary handling and the `formal` extra-strict cells on promotional language and significance inflation. Those two are worth the strictness in this form more than anywhere else in the register: an abstract is where a paper is most tempted to overclaim, because it is the part that gets read.

`verify.py` is the tool for the one check that matters here. Run it against the paper with facts checked rather than allowed. It compares numbers, dates, and quotations as multisets in both directions, so a figure that appears in the abstract but not in the paper is reported, and that is the failure this form invites.
