# shelf — 书架管理

`weread.sh shelf -h`

## 概念映射

albums = 专辑 = 有声书，三者同义。书架含电子书（books）、专辑（albums）、文章收藏（mp）。

## 数量计算

书架总数 = `books.length + albums.length + (mp 非空 ? 1 : 0)`

唯一合法公式。禁用 bookCount 等服务端内部计数字段。

按类型拆分仅当用户明确限定：电子书 = `books.length`，有声书 = `albums.length`。

## 公开/私密计算

遍历实际返回条目分组计数：

- 私密 = `books[].secret==1` + `albums[].albumInfoExtra.secret==1` + (mp 非空 ? 1 : 0)
- 公开 = `books[].secret==0` + `albums[].albumInfoExtra.secret==0`

不得使用未出现在数组中的补丁项。

## 输出规则

首句给出书架总数。展示分类构成时，各分类数量相加必须等于总数。

## Gotchas

- 回答书架数量时，albums 和 mp 必须计入总数，禁止用「另外还有」「此外」等措辞将它们排除在总数之外。
- 不要遍历 books 逐个调 `weread.sh book-info` 判断有声书。`book-info` 不返回 format 字段，且效率极低。直接用 albums 字段。
- mp 只是文章收藏目录入口，不包含具体文章内容。
