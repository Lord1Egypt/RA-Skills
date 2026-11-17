# Citation style: Chicago 17

**Applies to:** history, art history, theology, and much of the humanities and trade publishing. The author-date variant also serves parts of the physical and social sciences.

A citation file supplies formats. Only the source supplies facts. Every field in every pattern below comes from the work being cited, and a field that cannot be filled from the source is left out rather than guessed at.

Seventeenth edition. Chicago is two systems in one manual, and choosing between them is the first decision rather than a detail. **Notes and bibliography** uses numbered footnotes or endnotes with a bibliography, and it suits sources that are documents rather than data. **Author-date** uses parenthetical citations with a reference list, and it reads like APA with different punctuation. A document uses one or the other, never both.

## In-text

**Notes and bibliography.** A superscript numeral in the text, after the punctuation, pointing at a note.

| Case | Form |
|---|---|
| First full note | `<n>. <Firstname Lastname>, *<Title of the Book>* (<City>: <Publisher>, <year>), <page>.` |
| Shortened note, later | `<n>. <Lastname>, *<Short Title>*, <page>.` |
| Article, first note | `<n>. <Firstname Lastname>, "<Title of the Article>," *<Journal Name>* <volume>, no. <issue> (<year>): <page>, https://doi.org/<doi>.` |
| Two or three authors | `<Firstname Lastname>, <Firstname Lastname>, and <Firstname Lastname>` |
| Four or more | `<Firstname Lastname> et al.` |

The shortened note is the norm after the first mention. `Ibid.` was discouraged in the seventeenth edition in favour of the shortened form, which survives a later edit that inserts a note between two others.

**Author-date.** Parenthetical, with a comma before the page.

| Case | Form |
|---|---|
| One author | `(<Lastname> <year>, <page>)` |
| Two or three | `(<Lastname>, <Lastname>, and <Lastname> <year>, <page>)` |
| Four or more | `(<Lastname> et al. <year>, <page>)` |
| Author in prose | `<Lastname> (<year>, <page>) argues ...` |

No comma between the author and the year, which is the difference a reader notices first between this and APA.

## Reference entries

Asterisks in the patterns below mark the span that is italicized. The forms given are bibliography entries, with the author inverted and the elements separated by periods. For an author-date reference list, move the year to directly after the author and drop it from the end.

| Source type | Pattern |
|---|---|
| `journal-article` | `<Lastname>, <Firstname>. "<Title of the Article>." *<Journal Name>* <volume>, no. <issue> (<year>): <first>-<last>. https://doi.org/<doi>.` |
| `book` | `<Lastname>, <Firstname>. *<Title of the Book>*. <n>th ed. <City>: <Publisher>, <year>.` |
| `book-chapter` | `<Lastname>, <Firstname>. "<Title of the Chapter>." In *<Title of the Book>*, edited by <Firstname Lastname>, <first>-<last>. <City>: <Publisher>, <year>.` |
| `conference-paper` | `<Lastname>, <Firstname>. "<Title of the Paper>." Paper presented at <Conference Name>, <City>, <Month> <day>-<day>, <year>.` |
| `preprint` | `<Lastname>, <Firstname>. "<Title of the Preprint>." Preprint, submitted <Month> <day>, <year>. <URL>.` |
| `web-page` | `<Lastname>, <Firstname>. "<Title of the Page>." <Site Name>. Last modified <Month> <day>, <year>. <URL>.` |
| `dataset` | `<Lastname>, <Firstname>. "<Title of the Dataset>." Version <n>. <Publisher>, <year>. https://doi.org/<doi>.` |
| `software` | `<Lastname>, <Firstname>. *<Title of the Software>*. Version <n>. <Publisher>, <year>. <URL>.` |
| `standard` | `<Organization>. *<Title of the Standard>*. <Standard Designation> <number>. <City>: <Organization>, <year>.` |
| `report` | `<Lastname>, <Firstname>. *<Title of the Report>*. Report no. <number>. <City>: <Publisher>, <year>.` |
| `thesis` | `<Lastname>, <Firstname>. "<Title of the Thesis>." <PhD diss. or master's thesis>, <University>, <year>.` |

A bibliography lists everything consulted. A reference list under author-date lists only what is cited. The distinction is real and the two are not interchangeable, which is the error a citation manager makes when the output style is switched but the document is not.

Up to ten authors are listed in a bibliography entry, and past ten the first seven are listed followed by `et al.`

`standard` is the row that carries RFCs, ISO and IEC standards, and government publications, with the issuing body as the author.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "Ibid." repeated down a page, which the seventeenth edition discourages and which breaks the moment a note is inserted above it.
- A comma between the author and the year in an author-date citation.
- Notes and a parenthetical author-date citation in the same document.
- A full note repeated at every mention where a shortened one belongs.
- A bibliography labeled as a reference list, or a reference list containing works never cited.
- "op. cit." and "loc. cit.", which the manual dropped.
- A URL with no access or modification date on a page that has one.
- An accessed date on a source with a stable publication date, which Chicago does not require.

## What this style does not decide

Which of the two systems a publisher wants. That is the publisher's call and it changes the document's punctuation throughout, so it is settled before drafting rather than at submission. Whether notes go at the foot of the page or the end of the chapter. How much of a bibliography a trade publisher will print. Whether a source consulted but not cited belongs in the list, which depends on which system is in use.

It also does not decide anything about the prose around the citation. Register, hedging, and the argument itself belong to the form file and the voice profile.

## What the mechanical layer sees here

Nothing in this engine validates a citation. There is no check that a DOI resolves, that a shortened note matches a full one, or that a cited work exists, and the absence is deliberate: the guardrail against inventing a source is the editor's, and a green scan on a fabricated reference would be worse than no check at all.

One engine behaviour is worth knowing in this style specifically. Chicago quotes titles inside its entries, and `verify.py` extracts quotations and compares them between a document and its rewrite as a multiset. A rewrite that drops a quoted title from a note fails the fact check, which is the check doing its job on the element this style puts the most weight on.
