# book

`weread.sh book-info -h` / `weread.sh chapters -h` / `weread.sh progress -h`

## 语义陷阱

`book.progress` 是 0-100 整数百分比，1 = 1% 非 100%。仅 progress=100 且 finishTime 存在才算读完，展示带 % 号。

## 跨接口联动

`chapters` 返回的 `chapterUid` 是 `underlines`、`best-bookmarks`、`read-reviews` 的入参。