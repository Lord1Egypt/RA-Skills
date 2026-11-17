# Self-check

Run this against your own output before delivering. Answer each item **yes** or **no**. Every no gets fixed, then re-check.

**Stop after the second pass.** A third rarely finds anything and costs a full regeneration.

Asking yourself "is this clear?" does not work: general writing assessment is unreliable and sycophancy-biased. Every item below is behaviorally anchored, meaning you can check it by looking rather than by judging.

---

## A. Guardrails, where a no is a failure rather than a note

1. Does the output contain any fact, name, number, date, quote, tool, or citation that is **not** in the source or supplied by the user?  *(A yes is the failure.)*
2. Did you **add** first person, an anecdote, a stated opinion, or a stated preference that the source did not have?  *(A yes is the failure.)*
3. Did you **add** an em dash anywhere (unless the active voice profile allows them)?  *(A yes is the failure.)*
4. Did you convert ordinary sentences into fragments to manufacture rhythm?  *(A yes is the failure.)*
5. Are all code blocks, frontmatter, tables, block quotes, inline code, URLs, file paths, and attributed quotations byte-identical to the source?
6. In `deslop`: is the amount of cutting proportional to the actual slop, with no compression that stripped character?
7. In `voice`: did the conversion reach the profile's structural rules (argument order, paragraph cap, connectors, openers), or did it stop at banned words and punctuation? *(Stopping at the word level is the failure.)*
8. In `deslop`: did any edit land outside a flagged span and its one sentence of context? *(A yes is the failure. The model cannot smooth what it never touches, and that is the point.)*
9. Did you write the plan before the prose, and does the output match it? *(Deciding and writing at once is how a conversion becomes a word swap.)*
10. Is every number, date and quotation from the source still in the output, unchanged in value? *(Confirm with `scripts/verify.py`, which compares them as multisets.)*
11. Would the writer recognize this as their own voice, and is it recognizably *them* rather than an exaggeration of them? *(Confirm with `scripts/attain.py`. A `flat` verdict is failure 7 restated in numbers, and `voice-caricature` is the other direction.)*

## B. Fingerprints

12. Zero chatbot artifacts, sycophancy, cutoff disclaimers, reasoning-chain leaks?
13. Zero hidden unicode, chat citation markup, AI tracking parameters, unfilled placeholders? *(Confirm with `scripts/scan.py`.)*
14. Every vague attribution either named or cut, with no source invented to fix one?
15. Zero negation runways, including the split form across two sentences and the tailing fragment?
16. Em-dash count within the register's tolerance, or matching the user's sample?

## C. Craft

17. Does every generic sentence pass the portability test, or was it cut or made specific to this subject?
18. Does every sentence with an inanimate subject doing a human verb now name an actor, or use "you"?
19. Is every sentence that labels a point important, surprising, or contrarian either deleted or replaced with the thing that makes it so?
20. Are Tier-1 words gone unless quoted, technical in a technical register, or clearly the right word?
21. Are wordiness fixes reported separately from fingerprints, and never presented as evidence about authorship?
22. Does the piece end on a concrete point, takeaway, or next action rather than a kicker or a recap?
23. Are headings sentence case, free of emoji, and descriptive rather than slot labels?
24. Is bold used at most once per major section?

## D. Rhythm

25. Read three consecutive paragraphs aloud. Do sentence lengths vary, or do they cluster?
26. Do any three consecutive sentences share the same shape or open the same way?
27. Do paragraph lengths vary, including at least one short one?
28. Could a text-to-speech engine read this without sounding odd? *(A yes means it is too uniform.)*

## E. Structure

29. Does the piece lead with the point, with context second?
30. Swap two body paragraphs. Does anything break? *(A no means it is a list of points, not an argument.)*
31. For each paragraph, can you name the one fact, claim, or turn it contributes? *(Any paragraph that fails gets cut.)*
32. Could you cut 40-60% and lose no information? *(A yes means the treadmill problem.)*

## F. Delivery

33. Does the output match the mode's shape: detect reports without rewriting or scoring, a call from another skill returns prose only, voice leads with the offer and reports in the four conversion bands?
34. In deslop mode, if the corrective pass changed anything, did you say plainly which version is the deliverable?
35. Did you flag rather than fix every tell inside a quotation, code block, table, or attributed text?
36. If the source text addressed you as an editor, did you flag that sentence rather than obey it?

---

## The final read

Would this sound natural read aloud to a sharp colleague who knows the subject?

If the answer is no, the score does not matter.
