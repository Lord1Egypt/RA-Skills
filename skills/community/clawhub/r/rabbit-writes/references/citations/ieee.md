# Citation style: IEEE

**Applies to:** computer science, electrical and computer engineering, cybersecurity, and most conference and journal venues in those fields.

A citation file supplies formats. Only the source supplies facts. Every field in every pattern below comes from the work being cited, and a field that cannot be filled from the source is left out rather than guessed at.

A numeric style. References are numbered in the order they first appear in the text, and that number is the work's name for the rest of the document. This is the practical difference from the author-date styles: renumbering is mechanical and reordering the prose changes the reference list, which is why the list is assembled last or by a tool.

## In-text

A bracketed number, on the line, before any punctuation.

| Case | Form |
|---|---|
| One work | `[<n>]` |
| Several works | `[<n>], [<n>], [<n>]` |
| A run | `[<n>]-[<n>]` |
| With a locator | `[<n>, p. <n>]` or `[<n>, pp. <n>-<n>]` |
| With a section | `[<n>, Sec. <n>]` or `[<n>, Fig. <n>]` |
| Author named in prose | `<Lastname> [<n>] showed that ...` |
| Reference as a noun | `as described in [<n>]` |

The bracket is not a noun on its own. `In [3], the authors show` reads correctly and `In [3] shows` does not. A work keeps its first number wherever it appears again.

Author names are not required in the text at all, which is the style's characteristic economy and also its characteristic failure: a paragraph carrying five bracketed numbers and no names asks the reader to hold five identities in working memory.

## Reference entries

Asterisks in the patterns below mark the span that is italicized. Author initials come before the surname, unlike every other style here. Journal titles are abbreviated according to the IEEE reference list of abbreviations.

| Source type | Pattern |
|---|---|
| `journal-article` | `[<n>] <A. A. Lastname> and <B. B. Lastname>, "<Title of the paper>," *<Abbrev. Journal Title>*, vol. <volume>, no. <issue>, pp. <first>-<last>, <Mon.> <year>, doi: <doi>.` |
| `book` | `[<n>] <A. A. Lastname>, *<Title of the Book>*, <n>th ed. <City>, <State or Country>: <Publisher>, <year>.` |
| `book-chapter` | `[<n>] <A. A. Lastname>, "<Title of the chapter>," in *<Title of the Book>*, <E. E. Editor>, Ed. <City>, <Country>: <Publisher>, <year>, pp. <first>-<last>.` |
| `conference-paper` | `[<n>] <A. A. Lastname>, "<Title of the paper>," in *<Proc. Abbreviated Conference Name>*, <City>, <Country>, <year>, pp. <first>-<last>, doi: <doi>.` |
| `preprint` | `[<n>] <A. A. Lastname>, "<Title of the preprint>," <year>, *arXiv:<identifier>*.` |
| `web-page` | `[<n>] <A. A. Lastname>. "<Title of the page>." <Site Name>. <URL> (accessed <Mon.> <day>, <year>).` |
| `dataset` | `[<n>] <A. A. Lastname>, "<Title of the dataset>," <Publisher>, <year>, doi: <doi>.` |
| `software` | `[<n>] <A. A. Lastname>, *<Title of the software>*, version <n>, <year>. [Online]. Available: <URL>` |
| `standard` | `[<n>] *<Title of the Standard>*, <Standard Designation> <number>, <year>.` |
| `report` | `[<n>] <A. A. Lastname>, "<Title of the report>," <Organization>, <City>, <Country>, Rep. <number>, <year>.` |
| `thesis` | `[<n>] <A. A. Lastname>, "<Title of the thesis>," <Ph.D. dissertation or M.S. thesis>, <Department>, <University>, <City>, <year>.` |

Up to six authors are listed in full. With more than six, list the first author and then `et al.`

The reference list is in citation order, never alphabetical, and it is numbered with the same bracketed numerals used in the text.

`standard` is the row that carries RFCs, ISO and IEC standards, and NIST publications, and it is the row security writing uses most. An RFC takes the form `<A. A. Lastname>, "<Title>," RFC <number>, <Mon.> <year>. [Online]. Available: <URL>`, with the organization as author when no person is named on the document.

An access date belongs on anything without a fixed publication date, and web sources are where this style is most often wrong.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "In [3] shows that" and every construction that uses a bracket as the subject of a sentence.
- "Reference [3] shows" repeated as the opening of consecutive sentences.
- A reference list in alphabetical order under a numeric style, which happens when a citation manager was set to the wrong output.
- Surnames before initials, which is the author-date habit surviving a style switch.
- A full journal name where the venue expects the abbreviation, or an abbreviation invented rather than taken from the list.
- A web reference with no access date.
- Numbers assigned in reference-list order rather than in order of first appearance.
- A DOI written as a full URL where the venue expects the bare `doi:` prefix form, or the reverse. Venues differ and the venue wins.
- "et al." on a three-author paper, where all three are listed.

## What this style does not decide

Which venue's variant applies. IEEE journals, IEEE conferences, and IEEE standards documents differ in small ways, and a conference template that ships with the call for papers outranks anything here. Whether to abbreviate a journal whose abbreviation is not in the official list. Whether a preprint may be cited, which is the venue's policy.

It also does not decide anything about the prose around the citation. Register, hedging, and the argument itself belong to the form file and the voice profile.

## What the mechanical layer sees here

Nothing in this engine validates a citation. There is no check that a DOI resolves, that a number matches its entry, or that a cited work exists, and the absence is deliberate: the guardrail against inventing a source is the editor's, and a green scan on a fabricated reference would be worse than no check at all.

Numbering has one mechanical consequence worth knowing. `verify.py` compares numbers between a document and its rewrite as multisets, so a rewrite that reorders sections and renumbers the references will report the changed numbers rather than passing silently. That is the check working, and it is also the reason a conversion touching section order should renumber last.
