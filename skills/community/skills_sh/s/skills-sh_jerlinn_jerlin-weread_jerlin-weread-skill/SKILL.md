---
name: jerlin-weread-skill
description: 微信读书助手 — 搜索书籍、管理书架、查看笔记划线、浏览书评、阅读统计、发现推荐好书
author: jerlin
---

# WeRead — 微信读书助手

所有接口通过 `scripts/weread.sh` 调用。脚本处理鉴权和参数平铺。查看子命令列表：`weread.sh -h`；查看某个子命令的参数和回包字段：`weread.sh <subcmd> -h`。

## 能力路由

| 用户意图 | 子命令 | 领域知识 |
|----------|--------|---------|
| 搜书/找书 | `search` | `references/search.md` |
| 书籍详情/章节/进度 | `book-info` `chapters` `progress` | `references/book.md` |
| 书架 | `shelf` | `references/shelf.md` |
| 阅读统计/时长/偏好 | `readdata` | `references/readdata.md` |
| 笔记/划线/想法 | `notebooks` `bookmarks` `my-reviews` | `references/notes.md` |
| 热门划线/划线下想法 | `best-bookmarks` `read-reviews` `underlines` `review-detail` | `references/notes.md` |
| 公开点评 | `reviews` | `references/review.md` |
| 推荐好书 | `recommend` `similar` | `references/discover.md` |
| 用户阅读概况 | (组合) | `references/profile.md` |
| 阅读画像 | (组合 + AskUser) | `references/reading-profile.md` |

CRITICAL: 调用任何接口前，先阅读对应 reference 确认字段含义、计数口径和工作流。回包字段名和直觉含义冲突时，服从 reference 说明。

## 鉴权

- 环境变量 `$WEREAD_API_KEY`，格式 `wrk-xxxxxxxx`
- 未设置时提示用户：`export WEREAD_API_KEY=<你的apikey>`
- API Key 绑定用户身份（vid），无需手动传

## 通用规则

1. `errcode` 非 0 表示错误，给出中文提示。回包出现 `upgrade_info` 时按其 message 指引完成升级后重试。
2. 用户输入书名时，先调 `weread.sh search` 获取 bookId，再执行后续操作。
3. 对话中记住已查询的 bookId，后续操作无需用户重复提供。
4. 列表用编号展示方便选择。展示回包信息时，字段禁止直接翻译，参考 reference 中的说明。
5. 时间戳展示为 YYYY-MM-DD 格式，不得直接展示原始数字。
6. 阅读时长单位为秒，展示时转为「X 小时 Y 分钟」。

## 深度链接

展示书籍、章节、划线等内容时，回包字段足以构造链接的，附上跳转链接方便用户在 App 中打开。

| 场景 | URL Schema |
|------|-----------|
| 打开书籍 | `weread://reading?bId={bookId}` |
| 跳转章节 | `weread://reading?bId={bookId}&chapterUid={chapterUid}` |
| 跳转划线位置 | `weread://bestbookmark?bookId={bookId}&chapterUid={chapterUid}&rangeStart={rangeStart}&rangeEnd={rangeEnd}&userVid={userVid}` |

range 解析：划线接口返回的 range 格式为 `起始-结束`（如 `900-2004`），拆分后分别填入 rangeStart 和 rangeEnd。

划线位置链接的生成条件：回包同时包含 chapterUid 和 range。整本书评或无法定位到划线的点评不生成此链接。userVid 从上下文获取或省略。
 