# Short-fiction rules (modern Shunn)

Operational checklist for one short story in the modern edition of William Shunn's short-fiction guide. This file is not Shunn's article and must not be pasted into a submission.

This is not the novel spec. Do not add chapters, parts, a prologue page, or an epilogue page. Shunn's novel notes live separately at <https://www.shunn.net/format/novels/>. If the manuscript has those divisions, stop.

Source to trust when this note and a market disagree, in order: the market's guidelines, then the live short-fiction guide at <https://format.ms/story> (same text at <https://www.shunn.net/format/story/>). Guide text last updated 13 July 2026. Shunn's article is © William Shunn, CC BY-NC-ND 4.0: copy, distribute, and display for non-commercial purposes only, with credit and without alteration. Do not reproduce it in a submission or in this skill's output. He says not to put a copyright notice on your own manuscript.

## Page and type

- Fresh white page. No color, no border, no decoration, no watermark.
- Margins: 1 inch left, right, top, and bottom.
- Black type only. 12 point.
- Font: Courier New, 12 point. This is the writer's standing preference. Shunn's modern specimen is Times New Roman, and he still allows Courier New; do not switch it back unless the writer asks. Do not use a sans-serif. Do not use Times New Roman, Georgia, Garamond, Calibri, or Arial.
- The story is double-spaced (line spacing 2.0), including dialogue. Not 1.15, not 1.5, not triple.
- Left aligned. The right edge stays ragged. Full justification is for typeset books, not submissions.
- First line of every story paragraph indents 0.5 inch.
- No extra space between paragraphs. Indent is the only paragraph signal.
- One space between sentences. Never two.
- Emphasis is italics. Do not underline unless that one market's guidelines still demand underline.
- A dash is two hyphens (`--`) with no spaces on either side. Do not convert them to a single em dash. In Courier an em dash is hard to tell from a hyphen. A hyphen inside a compound word stays one hyphen.
- Curly quotes, double and single. A leading apostrophe (`'em`, `'tis`, `'twas`, `'cause`, `'round`, `'90s`) is an apostrophe, not an opening single quote.
- Dialogue stays inside quotation marks. Start a new paragraph when the speaker changes.
- Do not bold, small-cap, color, or enlarge anything, including the title.

## Page 1

Upper left, single-spaced, in this order:

1. Legal name, with preferred pronouns in parentheses on that same line if the writer wants them (`Jane Doe (she/her)`).
2. Street address, then city, region, postal code. More than one address line is fine.
3. Phone number.
4. Email.
5. A blank line, then a professional writing affiliation, only if it is relevant to this market (for example `Active member, SFWA` on a science-fiction submission). Leave it off for markets that will not care.

Any of those may be omitted when the writer feels unsafe sharing them. Most top markets ask for all of the contact block. Never invent values, and never reuse the sample address from Shunn's article.

Upper right, on the same line as the legal name: an approximate word count, lowercase, `about 1,500 words`.

- Count words in the story body only (not the title, byline, contact block, `#`, or `END`).
- Round to the nearest hundred. 1,507 rounds to 1,500. Halves round away from zero (1,550 → 1,600).
- Always the nearest hundred. This skill has no nearest-500 / novella / novel count.

Do not print a Social Security number, taxpayer ID, or any other tax identifier.

No running header on page 1. No page number on page 1. No footer. No copyright line. No separate title page.

## Title and byline

- The story's full title, centered, on its own line, a third to halfway down the first page. This skill aims at 40% of the text area (the page height minus the 1-inch top and bottom margins), so the gap above the title is the editor's note space. Do not measure the fraction from the paper edge: on A4 that pushes the title below halfway down. Do not move the title up under the address.
- That placement happens once, on page 1. Do not repeat it for chapters. There are no chapters.
- Title is the same 12-point roman type as the story. Not bold, not all caps unless that is truly the title.
- One double-spaced line below the title, then the byline, centered: `by Jane Doe`. The word `by` is lowercase.
- The byline is the published name. The legal name at the top is the name on a check. They can differ. If they are identical, both still appear.
- Two more double-spaced lines, then the first paragraph of the story.

## Pages 2 onward

- Running header, flush right, upper right, in the top margin. This skill places it 0.5 inch from the top edge.
- Pattern, spaces around the slashes: `Surname / Keyword / 2`
- Surname is the surname from the **byline**.
- Keyword is one or two words from the story title. Shunn's sample title "Proper Manuscript Format" uses `Format`. The script's default for three or more significant words is the last significant word; override `header_keyword` when that is weak.
- Page numbers start at 1 and first show on page 2. The same header runs for the rest of the story. It does not restart per chapter, because there are no chapters.
- The header does not appear on page 1.

## Scene breaks and ending

- Scene break inside the one story: `#` centered on its own line, not indented. Not a blank line. Not the word "Chapter."
- `END`, centered, after the last line, is optional.
- Then stop. No copyright line, no author bio in the file unless the market asked for a bio as a separate document.

## Before sending

- Read the story again for typos.
- If a physical copy is actually required: plain white paper, one side only.
- If the market's rules differ from this list, follow the market.

## What the emitter checks

`scripts/format_manuscript.py` fails the file when any of these are true:

- The story contains a chapter, part, book, prologue, or epilogue heading, or the front matter asks for a novel or novella.
- Margins are not 1 inch, or the page size is not the requested Letter or A4 size.
- A font other than Courier New appears, or type is not 12 point black.
- Any run is bold or underlined, or any paragraph is justified.
- Page 1 is not a different first page, or the first-page header contains text.
- The later-page header is missing `Surname / Keyword /` plus a PAGE field, or is not flush right.
- A body paragraph is missing the 0.5 inch first-line indent or double spacing.
- A scene break is not exactly a centered `#`.
- A straight quote or a double space remains in the document text.
- The word-count line does not match the body count rounded to the nearest 100.
- The text contains a Social Security pattern, or a paragraph begins with `Copyright`.
- The title's estimated position falls outside a third to halfway down page 1, unless the contact block is so long that the range is impossible.
