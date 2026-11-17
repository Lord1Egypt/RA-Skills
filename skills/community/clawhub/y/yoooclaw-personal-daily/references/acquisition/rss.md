# RSS 获取

仅在所选平台生成 reference 已设置 `acquisition=rss` 时读取本文件。

从 [`references/rss/domestic.md`](../rss/domestic.md) 和 [`references/rss/international.md`](../rss/international.md) 读取全部固定源。将本 Skill 的目录解析为绝对路径，把清单中的全部 URL 作为位置参数执行一次：

```bash
python3 <SKILL绝对路径>/scripts/fetch_rss.py <RSS_URL...> --limit 10 --workers 4
```

同时检查退出状态和 JSON：退出状态为 0 且顶层 `ok=true` 才表示至少一个源成功。逐项读取 `feeds`；`ok=false` 的项记录为该源失败。不要把源 URL 替换为未列入清单的站点。

合并所有成功源的条目，按规范化后的链接去重；链接为空时按“来源名 + 标题”去重。只保留发布时间落在宿主时区当天、且标题或摘要语义匹配至少一个搜索组的条目。每组最多保留 5 个候选。

所有源都失败时回复“RSS 新闻获取失败，请检查网络后重试”，然后停止，不输出空日报。部分源失败时继续，并记录国内、海外和总计的“成功源数/源数”以及失败源名，供最终结果简短披露。

**完成条件：** 至少一个源返回 `ok=true`；每个候选都匹配至少一个搜索组并记录来源、链接和发布时间，且候选已经过当日时间和去重检查；失败源已记录。
