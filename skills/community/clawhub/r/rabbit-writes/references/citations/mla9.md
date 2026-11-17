# Citation style: MLA 9

**Applies to:** literature, languages, cultural studies, film, and most humanities coursework in the United States.

A citation file supplies formats. Only the source supplies facts. Every field in every pattern below comes from the work being cited, and a field that cannot be filled from the source is left out rather than guessed at.

Ninth edition, published 2021. Its organizing idea is not a list of source types but a list of nine core elements assembled in a fixed order, which is why the patterns below look repetitive: they are the same template with different slots filled.

The elements, in order: Author. Title of source. Title of container, Other contributors, Version, Number, Publisher, Publication date, Location. Each ends with a period or a comma as shown, and an element that does not apply is skipped along with its punctuation.

## In-text

Author and location, with no date and no comma between them. This is the difference a reader notices first.

| Case | Parenthetical | In prose |
|---|---|---|
| One author | `(<Lastname> <page>)` | `<Lastname> argues ... (<page>).` |
| Two authors | `(<Lastname> and <Lastname> <page>)` | `<Lastname> and <Lastname> note ... (<page>).` |
| Three or more | `(<Lastname> et al. <page>)` | `<Lastname> et al. observe ... (<page>).` |
| Two works, one author | `(<Lastname>, *<Short Title>* <page>)` | `In *<Short Title>*, <Lastname> ... (<page>).` |
| No author | `("<Short Title>" <page>)` | see left |
| No page numbers | `(<Lastname>)` | `<Lastname> argues ...` |
| Timed media | `(<Lastname> <hh>:<mm>:<ss>)` | see left |

The parenthetical carries only what the sentence does not. Naming the author in prose and again in the parentheses is the most common redundancy in the style.

Page numbers appear with no `p.` or `pp.` A source with no pagination takes no locator at all rather than a paragraph count, unless the source itself numbers paragraphs.

## Reference entries

Asterisks in the patterns below mark the span that is italicized. The list is titled Works Cited and contains only works cited in the text.

| Source type | Pattern |
|---|---|
| `journal-article` | `<Lastname>, <Firstname>. "<Title of the Article>." *<Journal Name>*, vol. <volume>, no. <issue>, <year>, pp. <first>-<last>. *<Database>*, https://doi.org/<doi>.` |
| `book` | `<Lastname>, <Firstname>. *<Title of the Book>*. <n>th ed., <Publisher>, <year>.` |
| `book-chapter` | `<Lastname>, <Firstname>. "<Title of the Chapter>." *<Title of the Book>*, edited by <Firstname Lastname>, <Publisher>, <year>, pp. <first>-<last>.` |
| `conference-paper` | `<Lastname>, <Firstname>. "<Title of the Paper>." *<Proceedings Title>*, edited by <Firstname Lastname>, <Publisher>, <year>, pp. <first>-<last>.` |
| `preprint` | `<Lastname>, <Firstname>. "<Title of the Preprint>." *<Repository Name>*, <day> <Mon.> <year>, <URL>. Preprint.` |
| `web-page` | `<Lastname>, <Firstname>. "<Title of the Page>." *<Site Name>*, <day> <Mon.> <year>, <URL>. Accessed <day> <Mon.> <year>.` |
| `dataset` | `<Lastname>, <Firstname>. *<Title of the Dataset>*. Version <n>, <Publisher>, <year>, https://doi.org/<doi>.` |
| `software` | `<Lastname>, <Firstname>. *<Title of the Software>*. Version <n>, <Publisher>, <year>, <URL>.` |
| `standard` | `<Organization>. *<Title of the Standard>*. <Standard Designation> no. <number>, <Organization>, <year>.` |
| `report` | `<Lastname>, <Firstname>. *<Title of the Report>*. <Publisher>, <year>. Report no. <number>.` |
| `thesis` | `<Lastname>, <Firstname>. *<Title of the Thesis>*. <year>. <University>, <PhD dissertation or MA thesis>.` |

Two authors are given as `<Lastname>, <Firstname>, and <Firstname> <Lastname>`, inverting only the first. Three or more are given as `<Lastname>, <Firstname>, et al.`

The list is alphabetical by the first element of each entry, which is usually the author and is the title when there is none. It uses a hanging indent.

An access date is optional in the ninth edition and is worth including whenever the source has no publication date or is likely to change. Dates are day-month-year with the month abbreviated past May.

`standard` is the row that carries RFCs, ISO and IEC standards, and government publications, with the issuing body as the author.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "p." or "pp." inside a parenthetical citation, which belongs to the other styles.
- A comma between the author and the page number.
- A year in the parenthetical citation, which is the APA habit surviving a style switch.
- "Print" or "Web" at the end of an entry, which the eighth edition dropped.
- A URL carrying "https://" where a publisher's own guidance strips it, which varies and the venue wins.
- A works-cited list containing sources that are never cited, which makes it a bibliography.
- The author's name in prose and again in the parentheses in the same sentence.
- An entry assembled by source type rather than by the nine elements, which is how a container gets left out.

## What this style does not decide

Whether an instructor or journal wants the URL, the access date, or the database name, all of which the ninth edition treats as optional. How to handle a source with no clear container, which the manual asks the writer to reason about rather than look up. Whether a work should be cited at all.

It also does not decide anything about the prose around the citation. Register, hedging, and the argument itself belong to the form file and the voice profile.

## What the mechanical layer sees here

Nothing in this engine validates a citation. There is no check that a DOI resolves, that a container is right, or that a cited work exists, and the absence is deliberate: the guardrail against inventing a source is the editor's, and a green scan on a fabricated reference would be worse than no check at all.

One engine behaviour is worth knowing in this style specifically. MLA quotes the titles of shorter works, and `verify.py` extracts quotations and compares them between a document and its rewrite as a multiset. A rewrite that drops a quoted title from an entry fails the fact check. Dates are the other thing it watches, and it canonicalizes them, so the day-month-year order this style uses compares equal to the same date written any other way rather than reporting as a change.
