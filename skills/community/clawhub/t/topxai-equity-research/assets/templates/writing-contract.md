# <Report name> · Writing contract (every writing agent must follow it)

> Template. When several agents write chapters, save as `research/<report-id>/WRITING-CONTRACT.md`. Read it fully before
> writing and check against it when finished.
> The full rules are in `references/quality-bar.md`.
> If you have a mechanical gate for the assembled draft, run it before audit (`references/pipeline/03-writing.md`).

## 1. What this report argues
The one-sentence claim (with its per-share impact) and the value bridge, copied from the kickoff brief; every section lands
on one input of the bridge. New facts F1-F3 each get a section in Part 1. The opposing side must be written too (the
strongest opposing arguments are in `debate-bull.md` and `debate-bear.md`), and so must management's account
(`notes-statements.md`). The report form is in `references/pipeline/03-writing.md`.

## 2. Number discipline (a violation means rewrite)
1. Every number comes only from this report's `data-*.json`, `notes-*.md` and `calc/model-vN-output.txt`. Do not write
   numbers from memory and do not look up numbers yourself.
2. Every key number and every quotation carries a footnote `[^label]`: publisher, document, page / section / table, date,
   URL, and the grade [A]-[D] at the end. Body paragraphs carry no grade tags (a grade column in a table is fine). Own
   calculations say "this report's calculation" and point to Appendix D. Take the location from the notes; if the notes
   have none, send it back to the editor.
3. A bare number is not a sentence. Put a comparison in the same sentence (year on year, quarter on quarter, against peers,
   against its own history). But two or three numbers per sentence at most; the rest goes into a table or a note.
4. Formulas and intermediate values for derived numbers go in Appendix D. The body gives only the result.
5. Write an unresolved conflict as `⟦OPEN: conflict N⟧` and keep going. Do not choose a version. This report's open conflicts:
   - Conflict 1 ...
6. A superseded value may appear only as a correction ("v1 gave X; that was wrong because Y"), never as a live argument.
7. Do not smooth over a contradiction in the sources. If notes disagree, send it back to the editor. Do not pick one in the
   text.
8. State definition pitfalls explicitly (known for this report: ...).

9. Exhibits are screenshots made with `scripts/exhibit.py`; the title states the conclusion; the source gives the page or
   section and says the red box was added.
10. No internal codes in the text (J1 / X1 / G1 / E1-E5 / model section numbers / note and model file names).

## 3. Style
- Headline formula: a declarative sentence that carries a conclusion and a number. No questions, no suspense, and no
  "we found" openings.
- Banned: meta-commentary ("it is worth noting", "interestingly"), empty transitions, addressing the reader, and explainer
  tone. "This report argues" appears at most once per chapter.
- The first sentence of each paragraph is its conclusion. Use trader's vocabulary (basis, exposure, realisation,
  settlement, implied, payload).
- Write plainly. Remove filler, hype and templated phrasing; avoid triplets that share an opening and sentences that end on
  a flourish.

## 4. Compliance (a violation sends the whole chapter back)
- No signature or description of how the text was produced anywhere in the text; the credit wording is in
  `assets/disclaimer.md`.
- Do not present the report as personalised investment advice. Write decision content as "scenario -> what is observed
  (with a threshold) -> what that means for the research view". No buy or sell instruction wording.
- Do not invent ratings, sales or market shares. If a figure cannot be found, write "not available" and say why.

## 5. Delivery format
File name `parts/pNN-<chapter>.md`. Write the skeleton first, then fill it section by section. The message back to the
editor is at most 120 words.
