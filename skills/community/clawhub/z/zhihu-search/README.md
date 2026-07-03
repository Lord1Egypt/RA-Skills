# zhihu-search

**知乎内容抓取 skill — 搜索 / 读问答 / 抓专栏 / 看评论 / 看热榜**

零依赖(只要 Python 3 + curl)、自包含(数据全在 skill 目录)、API 优先(80%+ 抓取走 API,0 反爬对抗)。

---

## 安装

**方式一:作为 pi/openclaw skill 安装到 `~/.pi/agent/skills/`**
```bash
git clone https://github.com/excalibursssooo/zhihu-search.git \
  ~/.pi/agent/skills/zhihu-search
```

**方式二:从 ClawHub 安装**
```bash
openclaw skills install zhihu-search
```

**前置依赖**:
- Python 3.8+
- (可选) [agent-browser](https://github.com/vercel-labs/agent-browser) skill 已安装(仅 `article` 命令的 SPA HTML 解析兜底用)
- 知乎账号的 cookies(见下方"快速开始")

---

## 快速开始

### 1. 注入 cookies(一次性)

1. 用 Chrome 登录 https://www.zhihu.com/
2. F12 → Network → 任意请求 → 复制 `Cookie` 请求头完整内容
3. 粘到 `<skill>/data/cookies.txt`(`k=v; k=v;` 格式)

**或者一次性命令行**:
```bash
echo "_xsrf=xxx; d_c0=xxx; z_c0=xxx; ..." > ~/.pi/agent/skills/zhihu-search/data/cookies.txt
chmod 600 ~/.pi/agent/skills/zhihu-search/data/cookies.txt
```

### 2. 验证(3 秒)
```bash
export SKILL=~/.pi/agent/skills/zhihu-search

python3 $SKILL/zhihu-fetch.py paths              # 查看路径配置
python3 $SKILL/zhihu-fetch.py hotlist --limit 3  # 验证 cookie 是否有效
```

### 3. 使用
```bash
# 主题搜 (一键)
python3 $SKILL/zhihu-fetch.py quick "AI 热点" --compact --md-out ai.md

# 单个问题答案
python3 $SKILL/zhihu-fetch.py answers 2050261467174101567 --limit 10

# 热榜
python3 $SKILL/zhihu-fetch.py hotlist --limit 20

# 专栏文章列表 → 抓全文
python3 $SKILL/zhihu-fetch.py column-articles c_1297485212247425024 --limit 10
python3 $SKILL/zhihu-fetch.py article 2039840725727195825

# 答案评论
python3 $SKILL/zhihu-fetch.py comments 2050463219832164626 --limit 20
```

---

## 命令速查

| 命令 | 数据源 | 输出 |
|---|---|---|
| `search <kw> --type question/column/people/topic/zvideo` | API | 搜索结果 |
| `batch-search <kw1> <kw2> ...` | API | 多关键词并发+去重 |
| **`quick <topic> [--compact]`** | API | **⭐ 一键主题摘要** |
| `answers <qid>` | API | 问题答案 (JSON) |
| `extract <json>` | - | answers JSON → markdown |
| `qa-batch <qid:title> ...` | API | 多问题精读 → 单 md |
| `article <p_xxx>` | SPA HTML | 单篇专栏全文 |
| **`column-articles <c_xxx>`** | API | **专栏内文章列表** |
| **`comments <aid>`** | API | **答案评论 (绕开 comment_v5 反爬)** |
| `hotlist [--compact]` | API | 知乎热榜 |
| `paths` | - | 打印当前路径配置 |

**参数 flag**:
- `--compact`: 答案 head=300/tail=100 字符 (~70% token 节省)
- `--md-out PATH`: 输出到文件,避免 stdout 占 context
- `--quiet`: 只写文件,不打印正文
- `--limit N`: 抓取上限
- `--order score|ts|normal`: 评论排序(默认 score)

---

## 数据存储

所有运行时数据(cookies / 抓取结果)在 skill 自己的 `data/` 子目录,**自包含** — 跨设备直接 clone 即可使用。

```
zhihu-search/
├── zhihu-fetch.py            # 主抓取脚本 (10 个命令)
├── keepalive.py              # 登录态管理 (ab daemon)
├── paths.py                  # 路径统一管理
├── SKILL.md                  # openclaw 兼容的 skill 文档
├── README.md                 # 本文件
├── CHANGELOG.md              # 版本日志
├── LICENSE                   # MIT
├── CONTRIBUTING.md           # 贡献指南
├── .gitignore                # 排除 data/ 里的敏感文件
└── data/                     # ⬇ 运行时数据(全部 git 排除)
    ├── .gitkeep
    ├── cookies.txt           # 你注入的 cookies (chmod 600)
    ├── cookies-raw.txt       # 备用: 原始 raw 格式
    ├── state/zhihu.state.json
    ├── answers/<qid>.json
    ├── articles/<aid>.{json,md}
    ├── columns/<c_id>.json
    ├── comments/<aid>.json
    ├── hotlist.json
    └── exports/              # 用户显式 --md-out 的落盘
```

**路径解析优先级**:
1. 环境变量 `ZHIHU_DATA_DIR`(给 docker / CI 用)
2. 环境变量 `ZHIHU_COOKIE_FILE`(单独覆盖 cookie)
3. 老的 `/tmp/zhihu/`(向后兼容)
4. 默认 `<skill>/data/`

查看当前配置:
```bash
python3 $SKILL/zhihu-fetch.py paths
# 或
python3 $SKILL/keepalive.py paths
```

**安全注意**: `data/cookies.txt` 包含你的知乎登录凭证,**不要**分享、提交到 git、或上传到云端。`.gitignore` 已经默认排除,但本地仍需 `chmod 600`。

---

## 设计原则

- **API 优先**: 能用 API 就用 API,需要 JS 解析才用浏览器
- **零对抗**: 不 patch navigator.webdriver / 不拖滑块 / 不做验证码识别
- **cookie 唯一**: 借 cookie + 纯 curl 即可,无需 headless 浏览器
- **自包含**: 数据/状态全在 skill 目录,git clone 到任何位置都能用

---

## 适用 / 不适用

**适合**:
- 个人 / 小团队内容研究
- 找热点话题、热门问答
- 学术研究(短时间样本)
- AI agent 内嵌工具(需要"看看知乎最近什么火"时调用)

**不适用**:
- 商业爬虫服务(需要更复杂的反爬对抗 + 代理 IP 池)
- 24/7 自动监控(cookie 1-2 周过期,需自动续期)
- 1000+ 问题/天的批量抓取(需养号 + IP 轮换)

**明确不会做**:
- 点赞 / 发评论 / 关注(只读)
- 私信 / 通知(隐私敏感)
- 大规模爬取(>500 请求/小时)

---

## 故障排查

| 症状 | 修复 |
|---|---|
| `cookie 不存在` | cookies.txt 没在 skill data 目录;跑 `paths` 看实际位置 |
| `非 JSON 响应` | cookie 失效,重新走"快速开始"第 1 步 |
| `comment_v5 拿不到评论` | skill 已绕开: 用 `/api/v4/answers/<aid>/comments`(本 skill 默认) |
| `在 js-initialData 里找不到 article 对象` | 知乎改版;传错 id(应是 `p_xxx` 不是 `c_xxx`) |
| `topic feeds 10003` | 知乎已关闭该 API,话题下精华问答走不通 |
| `热榜返 0 条` | cookie 失效,重新走"快速开始"第 1 步 |

更多见 [`SKILL.md`](SKILL.md)。

---

## License

MIT — 详见 [LICENSE](LICENSE)。**使用本 skill 须遵守知乎用户协议,不得用于商业转售知乎内容、构建竞品或任何非法用途。**
