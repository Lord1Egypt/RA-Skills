---
name: today-news-task
version: 1.0.0
description: "抓取国内门户页面并汇总热点资讯。Use When 需要国内外热点与科技数码的要闻摘录。且可选择是否将结果推送到负一屏。"
license: MIT
---

# Today News Task 

今日热点资讯

本技能目录下带有 **`fetch_url.py`**，执行时应用 **`exec`** 调用 Python，不要优先依赖内置 `web_fetch`/`browser` 去拉下表门户。

## 抓取命令（优先使用）

在含 `SKILL.md` 与 `fetch_url.py` 的目录执行（路径按实际部署替换）：

```bash
python fetch_url.py <URL>
```

示例：

```bash
python fetch_url.py https://news.sina.com.cn/
```

对下表**每个入口**依次执行，将输出中的标题/链接摘录进汇总；某站失败可换同域子栏目 URL 再跑。

**备选：** 若环境允许，亦可尝试 `web_fetch`；与 `fetch_url` 二选一成功即可，不必重复。

**兜底：** 多条门户入口无法访问时，可对 **百度搜索**的结果页再跑 `fetch_url.py`（或允许的其他搜索页），并在对应条目「来源」中标为搜索页/转载站。

## 推荐门户与入口

| 站点 | 入口 URL |
|------|----------|
| 新浪新闻 | `https://news.sina.com.cn/` |
| 搜狐新闻 | `https://news.sohu.com/` |
| 网易新闻 | `https://news.163.com/` |
| 观察者网 | `https://www.guancha.cn/` |
| 澎湃新闻 | `https://www.thepaper.cn/` |
| IT之家 | `https://www.ithome.com/` |

## 工作流

1. **检索** — 对每个目标 URL 运行 `python fetch_url.py <URL>`，收集 HTML 中的要闻标题与链接。
2. **筛选** — 去重；丢弃无明确稿件链接的聚合页杂讯；时间以原站为准。
3. **整理** — 按类别整理，每条含标题、要点、来源。
4. **输出** — 使用下方 Markdown 结构。

**说明：** `fetch_url.py` 使用 `UTF-8` 解码且 `errors='ignore'`，若某站为 GBK 等编码可能出现个别乱码，以原站页面为准或再改进脚本。

## 可信度规则

**优先**

- 门户站内标注的原创或首发稿
- 机关通稿在门户的转载（仍标该门户页）

**谨慎**

- 论坛爆料、匿名截图
- 无稳定链接的营销汇总文

## 输出格式

```markdown
## 国内热点

1. [标题](链接)
   要点：…
   来源：… | 时间：xxx

## 国际热点

1. [标题](链接)
   要点：…
   来源：… | 时间：xxx

## 科技与数码

1. [标题](链接)
   要点：…
   来源：… | 时间：xxx
```



## 可选：将结果推送到负一屏

通过技能 `today-task` 完成推送。如果未安装该技能，请到 [ClawHub 国内镜像站](https://cn.clawhub-mirror.com/skills/today-task)（国内优先）或 [ClawHub 官方网站](https://clawhub.ai/skills/today-task) 安装；
授权码未设置时按 `today-task` 自身指引设置。

调用方式：构造 JSON 文件时，按 `today-task` 的说明运行，本技能场景下，JSON 必填字段：

| 字段 | 填写要求 |
|------|----------|
| `schedule_task_id` | 固定写 `0001`（周期性任务 ID；保持稳定，不要漏填，也不要让 today-task 自动生成） |
| `task_name` | 填 `今日热点资讯` |
| `task_result` | 成功时填 `任务已完成`；失败时填一句状态说明 |
| `task_content` | 上方「输出格式」生成的完整 Markdown 文本 |

未列出的字段按 `today-task` 自身指引填写。

