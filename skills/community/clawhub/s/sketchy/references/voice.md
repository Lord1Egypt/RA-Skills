# Voice

Read before writing any word on a page. The voice is deadpan: a clerk at a careful post office who knows the numbers are real and finds the situation a little funny. It states, it does not sell.

## Rules

| Rule | Example | Why |
|---|---|---|
| Short declaratives and imperatives | "Divide by the old number." | a slide is read in seconds |
| Two clauses, turned with a colon or a period | "Plan, not promise: dashed until it happens." | the turn carries the point |
| The title states the point | "Churn halved after we cut the setup call" | a topic label wastes the biggest type on the page |
| Second person for instructions | "Photograph the whole receipt." | the reader is the one doing it |
| The joke goes next to the number, never inside it | "Payback in 28 months. The lease runs for 60." | the figure must survive being quoted alone |
| One dry line per page at most | a kicker or the line under a figure | two jokes make a routine |
| Concrete nouns over abstractions | "a full laptop drive every five hours", not "significant data growth" | the reader can picture it |
| Say who | "Finance closed the ledger on 3 Oct." | numbers without owners invite doubt |
| American spelling in English, unless the user writes otherwise | color, center, program | one spelling per artifact |

## Twenty lines in the voice

Write your own, in this register. These show the shape.

**Business**
1. Revenue rose 12%. Costs rose 3%. The spreadsheet looks pleased with itself.
2. Under plan by €184,000. Finance has checked twice and will check again.
3. Two deals lost on price. Both customers sent a polite note.
4. On time 97.1% of the time. The other 2.9% wrote in.
5. Payback in 28 months. The lease runs for 60.
6. Signed by five directors. One of them read the appendix.
7. Forecast, not promise: dashed until it happens.

**Teaching**
8. Divide by the old number. Everyone forgets this once.
9. Draw the bucket first. The formula is about the bucket.
10. Three steps. The second one is where it goes wrong.
11. Wrong, but popular. Here is why it feels right.
12. Try it on paper before you try it on the exam.
13. Check: what changed, and by how much?

**Tech**
14. The disk filled at 03:12. Nobody was awake to be surprised.
15. Checkout was down for 41 minutes. The status page stayed green for 38 of them.
16. Retries tripled the load. The fix was to retry less.
17. Build time down from 14 minutes to 6. Nobody misses the wait.
18. One cache, three owners, no name on the ticket.
19. The test passes on every machine except the one that matters.
20. Version 2 ships on 3 Nov. Version 1 retires the same day, quietly.

## By element

| Element | Form | Examples |
|---|---|---|
| Title | the point, 3 to 9 words, no final period | We delivered more, for less |
| Kicker (`.sk-kicker`) | a short label; the CSS sets capitals; `·` separates parts | Q3 · July to September |
| Body line | one or two sentences, 40 words per slide at most | Three numbers, two problems, one ask. |
| Button | short sentence-case verb phrase, says what happens | Start, Show the math, Next page, Sign it, Keep it, Try again |
| Main action | the one `.is-accent` button, named for its outcome | Approve the lease |
| Stamp | 1 to 3 words, a state or a verdict; CSS sets capitals | Delivered, Overdue, On budget, Not yet, Returned |
| Red-pen note on a drawing | lowercase, terse, 1 to 4 words, points at one place | here, too late, the old one, carry the 1, now! |
| Drawing label | lowercase noun, sits on the thing | old price, new price, the queue |
| Source line | where and when, no `§` (the engine adds it) | Billing export, 1 Oct 2026 |
| Disclosure | the distortion and its factor | Trucks drawn 3x life size. Distances to scale. |
| Speaker notes | full spoken sentences: what you will say, not what the slide shows | "Pause here. Ask who has seen this happen." |
| Cover foot | one dry line of provenance | Prepared by finance. Figures as of 3 Oct; opinions as of today. |

Exclamation marks appear only in red-pen notes on drawings ("now!"), never in titles, body text or buttons.

## Avoid

| Avoid | Instead |
|---|---|
| Hype words: `seamless, powerful, unleash, revolutionary, effortless, delve, robust, elevate` and their cousins (game-changer, unlock, supercharge) | the plain verb and a number |
| "Let's dive in", "In today's fast-paced world", "Key takeaways", "Without further ado" | start with the point |
| Exclamation marks in prose; "Thank you!" | Thank you. Questions? |
| Emoji anywhere | a sketch or a stamp |
| Rhetorical question titles ("Why does churn matter?") | the answer as the title |
| Dashes used as pauses | a comma, a colon, or a new sentence |
| Puns on the brand name, jokes inside figures | a dry line beside the figure |
| Vague quantifiers ("significant", "many", "a lot") | the number, with its unit |
| Passive voice that hides the owner ("mistakes were made") | name the team and the date |

## Other languages

Same voice in every language: short, concrete, dry, with the number beside the joke. Write in the user's language from the start; do not translate an English draft line by line.

**German**
- Quotation marks „so“, decimal comma, space before %: 97,1 %. Dates: 25. Okt. 2026; on stamps 25. OKT. 2026.
- Thousands: a period (1.240.600) or a narrow no-break space (U+202F). With `<html lang="de">`, `data-count` reads the decimal comma and both separators and keeps them while it counts.
- Pick `Sie` or `du` once, from the audience, and keep it.
- Compound nouns make long titles: shorten rather than shrink, and let the linter catch overflow. `text-transform: uppercase` turns ß into SS on stamps; check that the word still reads.
- Kicker and stamp examples: Q3 · Juli bis September; Zugestellt, Überfällig, Im Budget.

**Arabic**
- Set `<html lang="ar" dir="rtl">`. Grid layouts mirror (in `split`, the picture column moves right), but the corner overlays are pinned to physical sides: `.sk-corner` stays top left, `.sk-source` bottom right. Look at every screenshot.
- The bundled Caveat and Courier Prime have no Arabic glyphs; Arabic text falls back to a system font and loses the handwriting. For a real Arabic deck, ship a theme that sets `--sk-font-hand` to an openly licensed Arabic hand font bundled locally (`themes-and-templates.md`).
- Remove letter-spacing on Arabic stamps and kickers (`style="letter-spacing:0"`): spacing breaks the joined letters.
- Keep figures in Western digits (0 to 9) when they use `.sk-figure` or `data-count`: Courier Prime has no Eastern Arabic digits and the counter reads only 0 to 9.
- Arabic punctuation (، ؟) and more line height for diacritics: check titles for clipped marks.

## Glyph coverage

Caveat is bundled for Latin, Latin Extended and Cyrillic: German, French, Spanish, Polish, Turkish, Czech, Russian, Ukrainian, Bulgarian and the rest. Courier Prime covers Latin and Latin Extended, so Cyrillic words inside `.sk-figure` or a receipt fall back; keep the record to digits and Latin units there. Both include `± × − € £ ¢ § ·` and the curly quotes. Greek letters and math symbols (`Σ Δ π ≈ → ✓`) and any other script come from a system font in a different hand: use them sparingly (one Σ in a math margin is fine), or write the word ("about", "to", "done"). Check the screenshots every time the language or a symbol is new.
