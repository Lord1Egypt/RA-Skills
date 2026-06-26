---
name: generate-daily-sports-update
description: 全自动运动科学资讯聚合引擎 — 聚合 55+ 全球顶级来源（PubMed 顶刊、专家博客、穿戴科技），智能去噪、翻译后同步至飞书/Notion。
metadata:
  openclaw.homepage: https://github.com/w2478328197-arch/sports-science-daily
  user-invocable: true
requires.bins:
  - python3
requires.env:
  - FEISHU_APP_ID
  - FEISHU_APP_SECRET
  - FEISHU_RECEIVE_ID
---

# 运动科学日报 — AI Agent 技能

全自动运动科学资讯聚合引擎，聚合 **55+ 全球顶级来源**，智能筛选、翻译后生成中文日报，一键同步至飞书云文档。

## 核心能力

1. **论文抓取** — 监控 **23 本 PubMed 顶刊**（BJSM、Sports Medicine、JSCR、MSSE 等）
2. **专家追踪** — 订阅 **14 位顶级专家** 博客/播客（Huberman、Attia、Nuckols、Dr. Mike、NSCA 等）
3. **行业监测** — 跟踪 **18 个行业源**（The Quantified Scientist、DC Rainmaker、Oura、Garmin、ScienceDaily、ACSM 等）
4. **四层去噪** — 正面词 / 研究词 / 强关键词 / 负面词，配合可信源白名单智能过滤
5. **自动翻译** — Google Translate API 实时翻译标题和摘要
6. **时间排序** — 每个栏目按发布时间降序，最新内容置顶
7. **历史去重** — 本地维护已处理记录，避免重复推送
8. **双平台同步** — 飞书云文档（含消息卡片通知）+ Notion 页面

## 前置条件

- **Python 3.8+**，需安装 `feedparser` 和 `requests`（`pip3 install -r requirements.txt`）
- **飞书应用凭证**（用于云文档同步）：
  - `FEISHU_APP_ID`：飞书应用 ID
  - `FEISHU_APP_SECRET`：飞书应用密钥
  - `FEISHU_RECEIVE_ID`：接收消息卡片的用户/群组 ID
- **（可选）Notion 集成**：
  - `NOTION_TOKEN` 和 `NOTION_PAGE_ID`

## 使用说明

1. **进入项目目录**：
   确保处于 `sports-science-daily` 项目根目录。

2. **运行更新**：
   ```bash
   python3 main.py --days 2
   ```

3. **可用参数**：

   | 参数 | 默认值 | 说明 |
   |------|--------|------|
   | `--days N` | 7 | 回溯天数 |
   | `--no-history` | 关闭 | 强制重新抓取（忽略去重） |
   | `--no-bloggers` | 关闭 | 跳过博主动态，仅抓行业 + 论文 |
   | `--lang LANG` | zh-CN | 输出语言（en、es、ja 等） |

4. **输出**：
   - 本地 Markdown 文件：`YYYY-MM-DD_运动科学日报.md`
   - 飞书云文档（自动创建，含分享链接）
   - 飞书消息卡片推送至配置的接收方
   - 更新 `processed_history.json` 去重记录

5. **「无新内容」情况**：
   若输出显示"🎉 没有发现新内容"，请增大 `--days` 参数或使用 `--no-history`。

## 项目架构

```
main.py                 # CLI 入口 — 调度所有模块
src/
├── config.py           # 全局配置：RSS 源、PubMed 期刊、屏蔽词
├── crawler.py          # 数据抓取：RSS + PubMed API
├── formatter.py        # 报告生成：Markdown 格式化 + 关键词过滤
├── translator.py       # 翻译引擎：Google Translate API
├── history.py          # 去重管理
└── exporters/
    ├── feishu.py       # 飞书云文档同步 + 消息卡片
    └── notion.py       # Notion 页面同步
```

## 安全与隐私

- **外部 API**：PubMed (eutils.ncbi.nlm.nih.gov)、Google Translate、飞书 OpenAPI、Notion API、各类 RSS 源
- **本地文件**：读写 `processed_history.json` 和 `.md` 报告文件
- **无隐私泄露**：仅抓取公开的学术数据和新闻，不涉及任何用户个人身份信息（PII）
