# 口语 → 命令

按顺序命中即停。没说的枚举用默认，不要自己加大 `--limit`。

| 用户说法 | 命令 |
| --- | --- |
| 热搜、热榜、今天什么火、实时热搜 | `hot-cli.js` |
| 文娱 / 娱乐热搜 | `hot-cli.js --category fun` |
| 社会热搜 | `--category social` |
| 体育热搜 | `--category sportnav` |
| 生活热搜 | `--category lifenav` |
| ACG / 动漫 / 游戏热搜 | `--category gamenav` |
| 科技热搜 | `--category technologynav` |
| 搜微博、综合、随便看看 | `search-cli.js --search-type 1` |
| 最新、实时、刚刚发的 | `--search-type 2` |
| 搜用户、搜账号、找博主 | `--search-type 3` |
| 搜视频 | `--search-type 4` |
| 热门微博 | `--search-type 5` |
| 搜话题 | `--search-type 6` |
| 搜超话 | `--search-type 7` |
| 这条微博的评论、留言、按热度 | `comment-cli.js --sort 0` |
| 评论按时间、最新评论 | `--sort 1` |

没给关键词就追问，不要替用户填词。没给微博链接就追问，不要拿搜索结果里的第一条自动去拉评论，除非用户明确说「用刚才那条」。
