# Citation style: APA 7

**Applies to:** psychology, education, social sciences, health sciences, business, and most journals that do not specify another style.

A citation file supplies formats. Only the source supplies facts. Every field in every pattern below comes from the work being cited, and a field that cannot be filled from the source is left out rather than guessed at.

Seventh edition, published 2019. The changes from the sixth that most often survive as errors: publisher location is gone, `Retrieved from` is gone except where a retrieval date is genuinely needed, `doi:` is replaced by the full `https://doi.org/` form, and three-or-more-author works use `et al.` from the first citation rather than the second.

## In-text

Author and date, in either order. The parenthetical form puts both in parentheses and the narrative form puts the author in the sentence.

| Case | Parenthetical | Narrative |
|---|---|---|
| One author | `(<Lastname>, <year>)` | `<Lastname> (<year>)` |
| Two authors | `(<Lastname> & <Lastname>, <year>)` | `<Lastname> and <Lastname> (<year>)` |
| Three or more | `(<Lastname> et al., <year>)` | `<Lastname> et al. (<year>)` |
| Group author, first use | `(<Full Group Name> [<ABBR>], <year>)` | `<Full Group Name> (<ABBR>, <year>)` |
| Group author, later | `(<ABBR>, <year>)` | `<ABBR> (<year>)` |
| No date | `(<Lastname>, n.d.)` | `<Lastname> (n.d.)` |
| Secondary source | `(<Original Author>, <year>, as cited in <Lastname>, <year>)` | see left |

The ampersand belongs inside parentheses and the word `and` belongs in running prose. Two authors are both named every time, with no `et al.` shortening.

A direct quotation carries a locator: `(<Lastname>, <year>, p. <n>)`, or `pp. <n>-<n>` for a range, or `para. <n>` where the source has no pages. A paraphrase does not require one and is better with it when the source is long.

A secondary citation is a last resort. Read the original where it can be read, and cite it directly.

## Reference entries

Asterisks in the patterns below mark the span that is italicized. Titles of articles and chapters are in sentence case. Titles of journals are in title case.

| Source type | Pattern |
|---|---|
| `journal-article` | `<Lastname>, <A. A.>, & <Lastname>, <B. B.> (<year>). <Title of the article>. *<Journal Title>*, *<volume>*(<issue>), <first>-<last>. https://doi.org/<doi>` |
| `book` | `<Lastname>, <A. A.> (<year>). *<Title of the book>* (<n>th ed.). <Publisher>.` |
| `book-chapter` | `<Lastname>, <A. A.> (<year>). <Title of the chapter>. In <E. E. Editor> (Ed.), *<Title of the book>* (pp. <first>-<last>). <Publisher>.` |
| `conference-paper` | `<Lastname>, <A. A.> (<year>, <Month> <day>-<day>). *<Title of the paper>* [Paper presentation]. <Conference Name>, <City>, <Country>. <URL>` |
| `preprint` | `<Lastname>, <A. A.> (<year>). *<Title of the preprint>*. <Repository Name>. https://doi.org/<doi>` |
| `web-page` | `<Lastname>, <A. A.> (<year>, <Month> <day>). *<Title of the page>*. <Site Name>. <URL>` |
| `dataset` | `<Lastname>, <A. A.> (<year>). *<Title of the data set>* (Version <n>) [Data set]. <Publisher>. https://doi.org/<doi>` |
| `software` | `<Lastname>, <A. A.> (<year>). *<Title of the software>* (Version <n>) [Computer software]. <Publisher>. <URL>` |
| `standard` | `<Organization>. (<year>). *<Title of the standard>* (Standard No. <number>). <URL>` |
| `report` | `<Organization>. (<year>). *<Title of the report>* (Report No. <number>). <Publisher>. <URL>` |
| `thesis` | `<Lastname>, <A. A.> (<year>). *<Title of the thesis>* [<Doctoral dissertation or Master's thesis>, <University Name>]. <Repository Name>. <URL>` |

Up to 20 authors are listed. Past 20, list the first 19, then an ellipsis, then the final author, and no ampersand.

The reference list is alphabetical by the first author's surname, double spaced, with a hanging indent. An issue number is included when the journal has one. A DOI is included whenever one exists, in the `https://doi.org/` form, and a URL takes its place only when there is no DOI.

A retrieval date appears only for a page whose content is designed to change and is not archived, in the form `Retrieved <Month> <day>, <year>, from <URL>`. It is not the default and adding it everywhere is the sixth-edition habit.

`standard` is the row that carries RFCs, ISO and IEC standards, and NIST publications. Cite the issuing organization as the author and give the document number in the parenthetical slot.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "Retrieved from https://" in front of a URL, which the seventh edition dropped.
- "doi:10.1000/xyz" instead of the full https form.
- A publisher location, which the seventh edition dropped.
- "et al." on a two-author work.
- An ampersand in running prose, or the word "and" inside a parenthetical citation.
- A reference list entry with no corresponding in-text citation, which is a bibliography pretending to be a reference list. APA lists only what is cited.
- An in-text citation with no reference entry. This is the direction that matters, and it is the one a reader checks.
- A page number attached to a paraphrase of an entire work.
- Title case on an article title, or sentence case on a journal title.
- A retrieval date on a stable, dated web page.

## What this style does not decide

Whether the journal wants the reference list alphabetized or numbered, since some APA-adjacent journals number. Whether preprints are citable at all, which is the field's call and not the manual's. How a name that does not split into given and family parts should be rendered, which is the author's call and should follow how they publish. What counts as a source worth citing.

It also does not decide anything about the prose around the citation. Register, hedging, and the argument itself belong to the form file and the voice profile.

## What the mechanical layer sees here

Nothing in this engine validates a citation. There is no check that a DOI resolves, that a year is right, or that a cited work exists, and the absence is deliberate: the guardrail against inventing a source is the editor's, and a green scan on a fabricated reference would be worse than no check at all.

Two engine behaviours do apply. `verify.py` compares numbers, dates, and quotations between a document and its rewrite as multisets, so a rewrite that drops a citation year or a page range fails the fact check rather than passing quietly. And `citation-leak` is a different finding entirely, about chat markup pasted from a model's output, not about scholarly citation. A document that quotes those markers to describe them raises it at P0 by design.
