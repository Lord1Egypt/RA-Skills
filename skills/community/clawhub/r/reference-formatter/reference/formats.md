# Citation Format Reference

Detailed formatting rules for each supported citation style.

---

## APA 7th Edition

### Journal Article
```
Author, A. A., & Author, B. B. (Year). Title of article. *Title of Periodical, Volume*(Issue), pp-pp. https://doi.org/xxxx
```
- Authors: Last name, Initials. Use "&" before last author. Up to 20 authors listed.
- Year in parentheses, followed by period.
- Article title: Sentence case (only first word and proper nouns capitalized). No italics, no quotes.
- Journal name: *Italicized*, Title Case. Followed by comma.
- Volume: *Italicized*. Issue in parentheses (not italicized). Comma, then page range.
- DOI: as hyperlink (https://doi.org/...). No period after DOI. No "Retrieved from" unless no DOI.

### Book
```
Author, A. A. (Year). *Title of book: Subtitle*. Publisher.
```
- Book title: *Italicized*, sentence case.
- Publisher name only (no "Inc.", "Ltd.", etc.)

### Book Chapter
```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), *Title of book* (pp. xx-xx). Publisher.
```

### Conference Paper
```
Author, A. A. (Year, Month). Title of paper. Paper presented at *Conference Name*, Location.
```
- For published proceedings, treat as book chapter or journal article.

### Webpage
```
Author, A. A. (Year, Month Day). Title of page. Site Name. https://url
```
- If no date: (n.d.)
- Include retrieval date only for dynamic/unarchived content: Retrieved Month Day, Year, from https://url

### Dissertation/Thesis
```
Author, A. A. (Year). *Title of dissertation* [Doctoral dissertation/Master's thesis, Institution]. Database Name.
```

---

## GB/T 7714-2015 (中国国家标准)

### 期刊论文
```
作者. 题名[J]. 刊名, 年, 卷(期): 起页-止页.
```
- 作者之间用逗号分隔，超过3人用", 等"或", et al"
- 题名后加文献类型标识：[J]期刊、[M]专著、[C]论文集、[D]学位论文、[EB/OL]电子资源

### 专著
```
作者. 书名[M]. 出版地: 出版社, 年.
```

### 学位论文
```
作者. 题名[D]. 保存地: 保存单位, 年.
```

### 电子资源
```
作者. 题名[EB/OL]. (发布日期)[引用日期]. 获取和访问路径.
```

### 英文文献（中文语境）
```
AUTHOR A, AUTHOR B. Title[J]. Journal, Year, Volume(Issue): Pages.
```
- 英文作者全大写，名用缩写

---

## MLA 9th Edition

### Journal Article
```
Author, FirstName. "Title of Article." *Journal Name*, vol. X, no. X, Year, pp. xx-xx. Database, DOI.
```
- First author inverted (Last, First), others normal order
- Article title in "double quotes"
- "vol." and "no." abbreviations
- Container system: journal is container 1, database is container 2

### Book
```
Author, FirstName. *Title of Book*. Publisher, Year.
```

---

## Common Reference Type Detection

| Pattern | Type |
|---------|------|
| Contains DOI + volume/issue | Journal Article |
| Has publisher + no DOI/volume | Book |
| Contains "In" + editor + "pp." | Book Chapter |
| URL + no journal metadata | Webpage |
| Contains "[D]" or "dissertation" | Thesis |
| Conference/congress/symposium + location | Conference Paper |

## Multi-Language Handling

- Chinese references: Format with Chinese punctuation（。，；：）per GB/T 7714
- English references: Format per target style
- Mixed lists: Separate Chinese and English sections per GB/T 7714 convention; keep unified per APA/MLA
