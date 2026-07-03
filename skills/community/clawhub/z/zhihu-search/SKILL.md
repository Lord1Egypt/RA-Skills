---
name: zhihu-search
description: 知乎内容抓取（搜索/读问答/抓专栏/看评论/看热榜）。默认走 API 路径 (`zhihu-fetch.py`)，仅单篇专栏正文走 SPA HTML 解析（不渲染浏览器）。前置：注入 cookie 到 `$SKILL/data/cookies.txt`。
version: 1.1.0
emoji: "📚"
homepage: https://github.com/excalibursssooo/zhihu-search
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
    envVars:
      - name: ZHIHU_COOKIE_FILE
        required: false
        description: 知乎登录 cookies 路径。默认 $SKILL/data/cookies.txt；老的 /tmp/zhihu/cookies.txt 也自动兼容。
      - name: ZHIHU_DATA_DIR
        required: false
        description: skill 运行时数据目录（覆盖默认 $SKILL/data/）。给 docker / CI 用。
      - name: ZHIHU_LOG
        required: false
        description: keepalive.py 日志路径（cron 用）。默认 $SKILL/data/state/cron.log。
      - name: SKILL
        required: false
        description: skill 根目录绝对路径，命令示例里用得到（agent 自填）。
    primaryEnv: ZHIHU_COOKIE_FILE
---

# zhihu-search

## ⚡ 30 秒上手 (给 LLM agent 用)

```bash
# 1. 定义 skill 路径 (一行 export, 全程只用 $SKILL)
export SKILL=/path/to/zhihu-search    # 你 clone 的位置

# 2. 一行拿到某主题的 top 问答摘要:
python3 $SKILL/zhihu-fetch.py quick "AI 热点" --compact --md-out /tmp/out.md

# 3. 看热榜:
python3 $SKILL/zhihu-fetch.py hotlist --compact --md-out /tmp/hot.md

# (可选) 验证登录态 + 路径:
python3 $SKILL/keepalive.py paths
```

`quick <topic>` 自动完成:
1. 用主题 + 自动扩展关键词 (如 "AI 热点 资讯"/"AI 热点 新闻") 并发搜索
2. 跨关键词去重, 按命中数 + 访问量排序
3. 抓 top N 问题 × top M 答案
4. 输出紧凑 markdown

关键 flag:
- `--compact`: 答案 head=300/tail=100 字符 (≈70% token 节省)
- `--md-out PATH`: 输出到文件, 避免 stdout 占 context
- `--quiet`: 只写文件, 不打印正文

**当前共 11 个命令**: `search` / `batch-search` / `quick` / `answers` / `extract` / `qa-batch` / `article` / `column-articles` / `comments` / `hotlist` / `paths`

**agent 须知**：不要 `read` zhihu-fetch.py / keepalive.py 源码 —— 看完本文档就会用。

## 路径选择

| 场景 | 用 | 为什么 |
|---|---|---|
| 批量抓数据（搜索/答案/专栏/热榜/评论） | **API** (`zhihu-fetch.py`) | ~30-50KB/页，零噪声 |
| 单篇专栏正文 | SPA HTML 解析（`article` 命令） | 知乎 article API 10003 拒绝, 必须从 `js-initialData` 取 |
| 浏览器交互（点赞/评论/渲染/过验证） | ab 浏览器 | 必须 JS（本 skill 暂不覆盖） |

**原则**：能用 API 就用 API，需要 JS 解析才用 ab 浏览器。

## 前置

| 文件 | 职责 |
|---|---|
| `keepalive.py` | 登录态持久化 (ab daemon + cookie/state 续期) |
| `zhihu-fetch.py` | API 数据抓取（11 个命令，见下） |
| `paths.py` | 路径统一管理 (env 覆盖 + 自包含 + 老路径兼容) |
| `$SKILL/data/cookies.txt` | 用户注入的 cookie（`z_c0` `d_c0` `__zse_ck` `_xsrf`，`chmod 600`）|

## 工作流

### 0. 首次 setup（一次性）

```bash
# Chrome 登录 zhihu.com → F12 → Network → 任意请求 → 复制 Cookie 请求头
# 粘到 $SKILL/data/cookies.txt (k=v; k=v; 格式)
echo "_xsrf=xxx; d_c0=xxx; z_c0=xxx; ..." > $SKILL/data/cookies.txt
chmod 600 $SKILL/data/cookies.txt

# 之后每次任务开头验证 (跑一次 hotlist 看是否返数据):
python3 $SKILL/zhihu-fetch.py hotlist --limit 3
python3 $SKILL/zhihu-fetch.py paths          # 查看当前路径配置
```

### 1. API 抓数据（默认走这条）

```bash
$SKILL/zhihu-fetch.py search "Transformer" --type question --limit 25   # 搜索 (type: question/column/people/topic/zvideo)
$SKILL/zhihu-fetch.py batch-search "大模型" "LLM" ... --limit 25        # 多关键词并发 + 去重
$SKILL/zhihu-fetch.py quick "政治活动" --compact --md-out out.md        # ⭐ 一键主题摘要 (推荐)
$SKILL/zhihu-fetch.py answers 498275802 --limit 20                       # 问题答案
$SKILL/zhihu-fetch.py extract $SKILL/data/answers/<qid>.json --top 3 [--compact]    # JSON → markdown
$SKILL/zhihu-fetch.py qa-batch "qid:title" ... --top 3 [--compact] --md-out out.md  # 多问题精读 → 单 md
$SKILL/zhihu-fetch.py article "https://zhuanlan.zhihu.com/p/<id>"       # 专栏（URL 或纯 id）
$SKILL/zhihu-fetch.py column-articles c_1297485212247425024 --limit 20  # 专栏内文章列表 (API)
$SKILL/zhihu-fetch.py comments 2050463219832164626 --limit 20           # 答案评论 (绕开 comment_v5 反爬)
$SKILL/zhihu-fetch.py hotlist [--compact] [--md-out out.md] --limit 30  # 热榜
$SKILL/zhihu-fetch.py paths                                              # 打印当前路径配置
```

注意: 上面命令前的 `$SKILL` 来自 30 秒上手部分的 export. 不要用 `$S` (没定义).

### 2. ab 浏览器（仅必要时，本 skill 暂未覆盖）

```bash
python3 $SKILL/keepalive.py open "https://www.zhihu.com/question/<id>"
ab eval "..."                    # 取 DOM
ab screenshot /tmp/screenshot.png
```

### 3. 自动保活（推荐装）

```bash
python3 $SKILL/keepalive.py install-cron   # 每天 9:00 续 z_c0 (1-2 周服务端滑窗)
```

## 新增能力（专栏文章列表 + 答案评论）

| 命令 | API 端点 | 用途 | 示例 |
|---|---|---|---|
| `column-articles <c_id>` | `/api/v4/columns/<c_id>/articles` | 拿专栏内所有文章 id + 标题 + 时间 + 摘要 | `column-articles c_1297485212247425024` |
| `comments <aid>` | `/api/v4/answers/<aid>/comments` | 拿某答案下的评论 (含作者/时间/赞数) | `comments 2050463219832164626` |

**典型工作流**：`search --type column` 找专栏 → `column-articles` 列文章 → `article <id>` 抓全文
**典型工作流 2**：`answers <qid>` 拿 top 答案 → 取 `id` → `comments <aid>` 看评论区

⚠️ **评论 API 重要陷阱**：知乎有 2 套评论 API：
- ❌ `/api/v4/comment_v5/answers/<aid>/root_comment` —— 新版，**对部分账号只返 totals 数字不返 data 内容** (反爬)
- ✅ `/api/v4/answers/<aid>/comments` —— 老版 (本 skill 用这个)，**完整返数据**

## 📁 数据路径 (skill 自包含)

所有运行时数据(cookies / 抓取结果)统一在 `$SKILL/data/` 子目录,skill 本身可 git clone 即用:

```
$SKILL/                              ← skill 根(可 git clone 到任何位置)
├── zhihu-fetch.py
├── keepalive.py
├── paths.py
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
└── data/                            ← 运行时数据 (git 排除)
    ├── .gitkeep
    ├── cookies.txt                  ← 你注入的 cookies (chmod 600)
    ├── cookies-raw.txt              ← 备用: 原始 raw 格式
    ├── state/zhihu.state.json
    ├── hotlist.json
    ├── answers/<qid>.json
    ├── articles/<aid>.{json,md}
    ├── columns/<c_id>.json
    ├── comments/<aid>.json
    └── exports/                     ← 用户 --md-out 显式指定的落盘
```

**路径解析优先级** (从高到低):
1. 环境变量 `ZHIHU_DATA_DIR` (给 docker / CI 用)
2. 环境变量 `ZHIHU_COOKIE_FILE` (单独覆盖 cookie)
3. 老的 `/tmp/zhihu/` (向后兼容, 如果存在)
4. 默认 `$SKILL/data/`

查看当前路径配置:
```bash
python3 $SKILL/zhihu-fetch.py paths
# 或
python3 $SKILL/keepalive.py paths
```

## 关键机制

- **ab daemon cookie 易丢**：每次 ab 启动用临时 user-data-dir（UUID 变），daemon 死 cookie 没。用 `keepalive.py` + `--state` 持久化绕过（本 skill 暂未集成，agent 自行处理）。
- **专栏 article API 已废**：`/api/v4/articles/{id}` 返 10003。脚本走 SPA HTML，正文嵌 `<script id="js-initialData">`（~62KB JSON）。
- **search type 实际值**：`question`/`column`/`people`/`topic`/`zvideo`（注意无 `article`，article 在知乎用 column 搜）。
- **API URL ≠ web URL**：API 返 `api.zhihu.com/...`，脚本已自动转 `www.zhihu.com/...`，无需手工处理。
- **author 字段结构（评论 API）**：`{"role": "normal", "member": {"name": "..."}}` —— 不是直接的 `name`，要 `.member.name`。
- **落盘位置**：`zhihu-fetch.py` 所有默认落盘文件统一在 `$SKILL/data/` 下，绝不写项目 CWD。具体：
  - `hotlist.json` 在 `$SKILL/data/`
  - `answers/<qid>.json` 在 `$SKILL/data/answers/`
  - `articles/<aid>.{json,md}` 在 `$SKILL/data/articles/`
  - `columns/<c_id>.json` 在 `$SKILL/data/columns/`
  - `comments/<aid>.json` 在 `$SKILL/data/comments/`
  - 用户显式 `--md-out` 路径不受此约束

## 边界

- 知乎抓数据 / 操作账号 → 本 skill
- 其他网站 → agent-browser skill

## 数据保留与清理

`$SKILL/data/` 是 git 排除目录（仅在本地存在）。如果想长期保留某个 topic 的抓取结果，建议在调用时显式加 `--md-out /path/to/keep.md`，把摘要拷到自己的目录。原 JSON 缓存可以随时 `rm -rf $SKILL/data/answers $SKILL/data/articles $SKILL/data/columns $SKILL/data/comments` 清理。

## 死胡同

| 尝试 | 结果 |
|---|---|
| 匿名 `ab open` 知乎 | 40362 / 重定向登录 |
| 自动短信登录 | Yidun 滑块拦死 |
| patch `navigator.webdriver` 拖滑块 | 多维检测 |
| `ab --session-name` 指望 auto-save | ab 0.27 不工作 |
| 不指定 `--state` 启动 ab | 临时 user-data-dir UUID 变，cookie 丢 |
| 直接 curl `zhuanlan.zhihu.com/p/xxx` 拿正文 | 仅 HTML 壳，正文在 js-initialData 里 |
| 用 bing `site:zhihu.com` 找内容 | 大部分被过滤 |
| 任何反检测对抗 | 工业级 captcha |
| `/api/v4/comment_v5/answers/<aid>/root_comment` 拿评论 | 部分账号 data 字段为空,仅返 totals 数字 |
| `/api/v4/topics/<t_id>/feeds*` 拿话题下问答 | 10003 拒绝 (知乎已关此端点) |

**唯一可行路径**：借 cookie + API 抓数据 (专栏正文走 SPA HTML 解析兜底)。
