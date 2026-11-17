# Form: research-paper

**Register:** `academic`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

A report of original work, written for people who will judge whether the conclusion follows from the evidence and whether they could do it again. Both audiences matter and they read different sections: a reviewer reads methods, a citing author reads the discussion, and almost everybody reads only the abstract.

The IMRaD shape below is the default in the sciences. Where a journal publishes its own required structure, that structure wins outright, and a paper is graded against the venue rather than against this file.

## Slots

- **Title.** The finding or the question, with the system studied in it. Searchable, because that is how it will be found.
- **Abstract.** Its own form. `forms/abstract.md` has the slots and the constraints.
- **Introduction.** What is known, what is not, and what this paper does about the gap. It ends with the contribution stated plainly. It is not a literature review, and a paper whose introduction surveys the field has usually mislabeled `forms/literature-review.md`.
- **Methods.** Enough for somebody with the same access to repeat it. Instruments, versions, sample sizes, exclusions, and the decisions made where the protocol met something it did not cover. Written so a reader can find a flaw, which is the opposite of writing so they cannot.
- **Results.** What was found, with the uncertainty attached. No interpretation. The discipline of this slot is what lets a reader accept a measurement and reject the reading of it.
- **Discussion.** What the results mean, what else could explain them, and how this sits against prior work. The alternative explanations are the slot, not a courtesy.
- **Limitations.** What the design could not see. Stated by the authors, or supplied later by a reviewer in less friendly terms.
- **Conclusion.** What follows. Often a paragraph of the discussion rather than its own section.
- **Data and code availability, funding, conflicts, author contributions.** Governed by the venue.
- **References.** A citation style applies. `references/citations/` has the four, and `ieee` or `apa7` covers most venues.

## Bands

| Purpose | Band |
|---|---|
| A short report or letter | 1,500 to 3,000 words |
| A full research article | 4,000 to 8,000 words plus references |
| A methods or systems paper | as long as the method, with the rest in supplementary material |

Word limits come from the venue and they are hard. Where this file and a call for papers disagree, the call wins.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "To the best of our knowledge, this is the first" where a fifteen-minute search finds three.
- "The results clearly demonstrate" attached to a marginal effect.
- "Further research is needed" as a closing sentence with no statement of what research.
- "It is well known that" in front of a claim that needs the citation it is avoiding.
- "Due to space constraints" covering an omission the reader needed.
- Interpretation smuggled into the results section, so a reader who rejects the reading has to disentangle it from the measurement.
- A limitations section listing only limitations that do not threaten the conclusion.
- An introduction that reviews the field for two pages and states the contribution in the last sentence.
- A discussion that restates the results in the same order with different verbs.

## What the mechanical layer sees here

This is the register the `academic` column was built for, and it was calibrated against 19 open-access papers rather than assembled from intuition. `docs/academic-corpus/README.md` has the method and `PROOF.md` has the numbers.

The three vocabulary tiers run in partial mode with this register's own exemption list, which drops `paradigm` and `transformation` on top of the shared technical list, because each carries a sense here it does not carry in a blog post. `crucial` and `holistic` were candidates and were rejected: the first is an intensifier everywhere, and the second turned out to be one paper using it eleven times rather than a fact about the register.

Confidence calibration relaxes to two hits, because `Notably,` and `Importantly,` are discourse markers here and fired on 14 of the 19 papers. Low burstiness and trigram repetition are skipped outright: papers genuinely have even sentence lengths, and a paper repeats a construct's name for precision, which is the one thing a reader must not have to disentangle.

Two things run at full strength on purpose. The `formal` extra-strict cells apply to promotional language, significance inflation, generic conclusions, boilerplate, and future-narrative closers, because overclaiming is this register's characteristic sin. And the clarity rules do too: `utilize`, `in terms of`, and `it is important to note that` fired on 14 of 19 papers, and academic writing being full of them is a fact about academic writing rather than a reason to stop reporting it.

One known false positive, published rather than hidden. `vague-attribution` is a P0 fingerprint and fires on `research suggests` and `studies show`, which appeared in 6 of the 19 papers. In a paper those phrases carry a citation the engine cannot see. A fingerprint P0 is never muffled per register, so this one is reported and read rather than suppressed.
