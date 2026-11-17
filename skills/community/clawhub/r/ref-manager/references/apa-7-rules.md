# APA 7th Edition Citation Rules

Conventions used by this skill. The formatter is in `scripts/apa.py`.

## Author formatting

- **English**: `Family, G. G.` — surname first, then initials of given names. Multiple authors are joined with `, ` and the final one with ` & `.
  - `Smith, J.`, `Smith, J. & Doe, A.`, `Smith, J., Doe, A., & Lee, B.`
- **Chinese**: full name kept as-is, authors joined with `、`.
  - `张三、李四`
- Up to 20 authors are listed. Beyond 20, keep the first 19, then `...`, then the last author.

## Date

- Journal / book / report: `(2020)`.
- Web page with a full date: `(2020, May 1)`.

## Reference types

### Journal article (JOUR)

- English: `Author, A. (2020). Title of article. *Journal Name*, 12(3), 100-110. https://doi.org/10.xxxx`
- Chinese: `作者. (2020). 文章标题. 《期刊名》, 12(3), 100-110. https://doi.org/10.xxxx`

The journal name and volume number are italic in print. In flat text (Excel / RIS notes) italics are omitted.

### Book (BOOK)

`Author, A. (2020). *Title of book*. Publisher. https://doi.org/...`

### Book section / chapter (CHAP)

`Author, A. (2020). Title of chapter. In E. Editor (Ed.), *Title of book* (pp. 100-110). Publisher.`

### Web page / electronic (ELEC)

`Author, A. (2020, May 1). *Title of page*. Site Name. https://url`

## DOI rule

When a DOI exists, it is always shown as a full URL: `https://doi.org/<DOI>`. This applies to both print and online sources.

## No-date rule

If the year cannot be determined and cannot be recovered, use `(n.d.)`. Do not guess a year.

## Note on this skill

The `.xlsx` and RIS `N1`/XML `<note>` fields store the APA citation as plain text (no italics markup), so the citation can be copied directly.
