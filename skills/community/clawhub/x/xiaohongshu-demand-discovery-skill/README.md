# Xiaohongshu Demand Discovery Skill

一个面向 OpenClaw 的小红书需求发现采集 Skill。

它可以基于「求推荐、避雷、平替、真实测评、后悔买、怎么选」这类需求型关键词，自动搜索小红书近期高互动笔记，抓取笔记详情和评论区内容，并输出结构化数据，方便后续交给 LLM 或产品经理 Agent 做用户需求分析。

> 本项目基于 `xiaohongshu-skill v1.0.2` 二次开发。  
> 当前定位是「数据采集层」，不是完整 SaaS，也不是最终的 LLM 分析工具。

---

## 核心功能

- 小红书扫码登录
- 登录状态检查
- 关键词搜索笔记
- 按「最多评论 / 最多点赞 / 最新」等方式排序
- 按发布时间筛选，例如一周内
- 获取笔记详情
- 加载笔记评论
- 清洗评论数据
- 匿名化作者信息
- 输出 JSONL / JSON / Markdown 报告
- 新增 `demand-discovery` 需求发现采集模式

---

## 需求发现模式

新增命令：

```bash
python -m scripts demand-discovery
```

默认会使用一组需求型关键词，例如：

```text
求推荐
避雷
平替
真实测评
后悔买
踩坑
好用吗
怎么选
值不值得买
学生党
新手必备
替代品
不好用
怎么解决
```

执行流程：

```text
需求型关键词
↓
小红书搜索
↓
筛选近期内容
↓
按最多评论排序
↓
抓取高互动笔记
↓
加载评论
↓
清洗与匿名化
↓
输出结构化数据
```

---

## 安装依赖

建议使用 Python 3.10+。

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

Linux / WSL 环境如缺少浏览器系统依赖，可继续运行：

```bash
python -m playwright install-deps chromium
```

---

## 安装到 OpenClaw

安装本地 Skill 时，请安装解压后的项目文件夹，不要直接安装 zip。

```bash
openclaw skills install "<本地项目文件夹路径>" --as xhs-demand
```

示例：

```bash
openclaw skills install "C:\Users\YourName\Documents\xhs-demand-skill" --as xhs-demand
```

检查是否安装成功：

```bash
openclaw skills list
openclaw skills check
openclaw skills info xhs-demand
```

---

## 登录小红书

第一次使用前，需要扫码登录：

```bash
python -m scripts qrcode --headless=false
```

检查登录状态：

```bash
python -m scripts check-login
```

如果 cookie 失效，重新扫码登录即可。

---


## 常用参数

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--keywords` | 手动指定关键词，多个关键词用英文逗号分隔 | 内置关键词 |
| `--keywords-file` | 从文本文件读取关键词 | 无 |
| `--days` | 尽量保留最近 N 天的笔记 | `3` |
| `--search-publish-time` | 搜索发布时间筛选 | `一周内` |
| `--sort-by` | 搜索排序方式 | `最多评论` |
| `--note-type` | 笔记类型：不限 / 视频 / 图文 | `不限` |
| `--posts-per-keyword` | 每个关键词保存多少条笔记 | `3` |
| `--search-limit` | 每个关键词搜索返回数量 | `8` |
| `--max-comments` | 每条笔记最多保存多少条评论 | `20` |
| `--output-dir` | 输出目录 | `data/demand_discovery/<timestamp>/` |
| `--timezone` | 时间过滤时区 | `Asia/Shanghai` |
| `--headless` | 是否无头运行浏览器 | 视命令配置 |

---

## 输出文件

默认输出目录：

```text
data/demand_discovery/<timestamp>/
```

每次运行会生成一个新的时间戳目录。

主要输出：

```text
notes_clean.jsonl
comments_clean.jsonl
collection_summary.json
collector_report.md
```

说明：

- `notes_clean.jsonl`：笔记级别数据
- `comments_clean.jsonl`：评论级别数据，适合后续喂给 LLM 分析
- `collection_summary.json`：机器可读的采集总结
- `collector_report.md`：人类可读的采集报告

---

## 在 OpenClaw 中使用

安装完成后，可以直接在 OpenClaw 中用自然语言调用：

```text
使用 xhs-demand 跑一次小红书需求发现采集。先做小规模测试，只搜索“求推荐”，抓 1 条笔记，每条最多 5 条评论，打开浏览器运行。
```

也可以指定多个关键词：

```text
使用 xhs-demand 的 demand-discovery 功能，关键词为“求推荐,避雷,平替”，每个关键词抓 2 条笔记，每条最多抓 10 条评论，headless=false。
```

---

## 适合场景

- 小红书用户需求发现
- 评论区痛点采集
- 产品机会探索
- 竞品评论研究
- 内容选题研究
- 给 LLM / Agent 提供结构化输入数据

---

## 安全边界

本项目仅用于学习、研究、内部产品验证和小规模公开内容采集。

请注意：

- 只采集公开可访问内容
- 不绕过登录、验证码或平台风控
- 触发验证码时应停止并人工处理
- 不保存真实用户名、昵称、头像、主页链接
- 作者信息会被匿名化为 `author_hash`
- 不进行自动点赞、评论、收藏、发布等互动操作
- 不建议进行大规模高频采集

---

## 项目定位

这个 Skill 是「小红书需求发现数据采集层」。

完整工作流可以是：

```text
xhs-demand 采集小红书笔记和评论
↓
comments_clean.jsonl / notes_clean.jsonl
↓
LLM 需求分析 Agent
↓
产品经理 Agent
↓
需求洞察报告 / 产品机会分析 / 内容选题建议
```

当前项目只负责第一步：采集、清洗和结构化保存。

---
