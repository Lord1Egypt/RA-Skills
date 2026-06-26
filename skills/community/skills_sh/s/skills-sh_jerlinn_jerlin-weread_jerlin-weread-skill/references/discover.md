# discover — 发现推荐好书

`weread.sh recommend -h` / `weread.sh similar -h`

路由：无参数泛推荐 → recommend；有 bookId → similar；有关键词 → search。

翻页：recommend 用 searchIdx 作为下次 maxIdx；similar 用最后一条 idx 作为 maxIdx，带上 sessionId。
