# README self-check

Run through before delivering a draft, restructure, or audit. Every item is yes or no. Fix every no once, re-check once, stop — a third pass rarely finds anything new.

## Structure

1. Do the first two sentences say what the project is and why it exists, before any badge, sponsor content, or hero image?
2. Does installation come right after the pitch, not buried past several other sections?
3. Is there a working, copy-pasteable path from "clone/install" to "it's running" — not just a list of prerequisites?
4. Is license the last section (or close to it), and short — name plus link, not restated terms?
5. If there's a table of contents, does the document actually need one (optional at roughly 1,500+ words, expected at 2,500+)? If it's under 1,500, is the TOC adding scroll instead of saving it?
6. Is anything promotional (sponsors, badges beyond the header row, a hero image) sitting between the top of the file and the real description? If so, move it down or cut it.

## Craft

7. Is sentence length actually varied, or does every sentence run the same shape? Read a section aloud — uniform cadence is the tell.
8. Are paragraphs short (2–3 sentences)? Any single paragraph over ~60 words should probably split.
9. Does every link use `[text](url)` — no bare URLs, no "click here"?
10. Does link text name the destination in a couple of words?
11. If there's a headline number or performance claim, does the document say what it doesn't cover, or is it asserted with no caveat?
12. Are badges typed and wired to something real (license, version, stars, chat, build), rather than a row padded out to look established?
13. Do the numbers agree with each other everywhere they appear? (A stat badged at the top should match the same stat if it's restated in body text.)

## Accuracy

14. Does every install command, dependency, and version number actually match the project as it exists right now — nothing invented or assumed?
15. Does the license section name the license the project actually uses (check for a `LICENSE` file rather than guessing)? `readme_check.py` now does half of this for you: run on a real path, it walks up to the repository root for a `LICENSE`, `LICENCE`, `UNLICENSE`, `COPYING` file or `LICENSES/` directory and reports the mismatch either way. It cannot tell you whether the section names the *right* license, only whether there is a file to name.
16. Are code examples runnable as written, not simplified to the point of being wrong?

## Voice

17. Did you read `voices/<name>.md` itself, not only run the script against `voices/<name>.rules.json`? The JSON is the subset a regex can decide. A clean scan means the floor was met, not that the document sounds like anyone.
18. Does this read like the person publishing it, or like a chatbot's idea of an open-source project? Read the pitch aloud against a paragraph they wrote.
19. Are the profile's hard nos actually absent (punctuation bans, banned words, sentence and paragraph caps), including inside headings, table cells, and badge alt text?
20. Does the document follow the profile's judgment rules, the ones no regex covers: how it orders an argument, how it calibrates certainty, how much warmth it carries, and whatever its own final check asks?
21. Where a profile rule and the medium genuinely disagree (warmth, signposting, first person, humor in front of strangers), did you surface the tradeoff for the user instead of quietly resolving it in either direction?
22. Did the voice change the structure? It shouldn't have. Pitch first, install early, license last and short holds regardless of who is writing.
23. Is anything here a habit borrowed from correspondence rather than documentation (a greeting, a sign-off, "hope this helps")? Cut it.

## Before delivering

24. For an audit: are findings ordered by impact (safety first, structural second, voice third, fingerprint and craft fourth), each pointing at a real line or section — not a generic list that could apply to any README?
25. Did you run `python3 {baseDir}/scripts/readme_check.py <file>`, clear every P0, and either fix or consciously keep each P1?
