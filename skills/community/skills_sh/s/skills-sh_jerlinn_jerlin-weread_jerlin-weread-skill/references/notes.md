# notes — 笔记/划线

`weread.sh notebooks -h` / `bookmarks -h` / `best-bookmarks -h` / `underlines -h` / `read-reviews -h` / `my-reviews -h` / `review-detail -h`

## 两种口径

统计口径 = reviewCount + noteCount + bookmarkCount → 回答「有多少笔记」
导出口径 = 划线内容 + 想法/点评内容 → 回答「导出笔记」。书签只计数，不可导出。

## 语义陷阱

- `noteCount` = 划线/高亮条数，不是总笔记数。总笔记数须 reviewCount + noteCount + bookmarkCount。
- `reviewCount` 已含划线想法、书评、书摘。计算总数时不得再加「点评数」，否则重复。
- `notebooks` 不返回 `highlightCount`。用户说「高亮数/划线数」→ 对应 `noteCount`。
- `my-reviews` 参数是小写 `bookid`，不是 `bookId`。
- `notebooks` 的 reviewCount 不可拆分为「划线想法」和「个人点评」的独立数量；如需明细须调 `my-reviews`。
- `read-reviews` 的 reviews 数组内 count 服务端上限 20，超过自动截断。

## 分页

`notebooks` 用游标分页（count + lastSort）。首次只传 count；hasMore=1 时取末条 sort 值作下次 lastSort。

## 查询链路

热门划线及想法：best-bookmarks（原文+人数）→ 取 range → read-reviews（该划线下想法）→ review-detail（完整详情含评论/点赞）

underlines 只有热度统计（人数/得分），不含划线文本，仅用于「X 人划线」标签。

## 工作流

- 无 bookId：`notebooks` 遍历至 hasMore=0，按统计口径排序。
- 有 bookId 问内容：并发调 `bookmarks`（划线）+ `my-reviews`（想法/点评），按 chapters 分组。
- 用户要书签内容：当前不可导出，只有统计数量。划线 ≠ 书签。
- 热门划线：按上述查询链路。

## 输出格式

概览：编号列表，每本含书名、作者、总笔记数、想法/点评数、划线数、书签数、阅读进度。
单本：按章节分组。划线用 `>` 标原文；想法/点评区分划线想法、章节点评、整本书评，能关联时放对应划线下方。
