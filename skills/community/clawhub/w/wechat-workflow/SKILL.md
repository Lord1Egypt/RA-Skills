---
name: wechat-workflow
description: "微信公众号虾发布工作流 — AI 生成封面图 + 内容创作（去AI味+爆款结构）+ 一键发布草稿箱 + 搜狗验证收录 + 数据追踪 + 选题建议。全链路自动化。"
metadata:
  openclaw:
    emoji: "📱"
    requires:
      env:
        - WECHAT_APP_ID
        - WECHAT_APP_SECRET
      bins:
        - wenyan
---

# 微信公众号虾发布工作流

微信公众号运营完整工作台。从选题到发布的全流程自动化工具包。

## 核心能力

| 能力 | 说明 |
|------|------|
| AI 封面生成 | 一键生成封面图，保存到 `assets/cover.jpg` |
| 内容创作 | **推荐使用 khazix-writer skill**（卡兹克风格，含完整四层自检体系） |
| 一键发布 | Markdown → 微信公众号草稿箱，支持多主题+代码高亮 |
| 搜狗验证 | 自动用搜狗微信搜索验证文章收录状态 |
| 数据追踪 | 追踪多篇文章收录状态、查询次数 |
| 选题建议 | 基于已发布内容给出下一篇文章方向和候选标题 |

## 整合 khazix-writer

**khazix-writer**（卡兹克风格写作skill）是内容创作的核心引擎，**wechat-workflow** 负责发布和分发。

**完整工作流：**
```
用户给选题/素材
    ↓
khazix-writer 生成文章（四层自检通过）
    ↓
添加 frontmatter（title + cover）
    ↓
wechat-workflow 发布到草稿箱
    ↓
搜狗验证收录
    ↓
monitor.py 追踪数据
```

**khazix-writer 安装：** `git clone https://github.com/KKKKhazix/khazix-skills` 到 skills 目录

**触发词：** 写文章、写稿子、帮我写、续写、扩写、公众号文章、长文、出稿、按我的风格写

## 依赖声明

- **Node.js / npm**：必须。用于运行 `@wenyan-md/cli`
- **wenyan**：必须。若未安装，脚本会自动执行 `npm install -g @wenyan-md/cli`
- **Python 3**：必须。运行所有管理脚本
- **image_generate 工具**：推荐。用于生成封面图（由 OpenClaw 内置提供，无需安装）

> ⚠️ 自动安装说明：首次运行发布脚本时，若检测到 `wenyan` 命令不存在，会自动从 npm registry 下载并全局安装 `@wenyan-md/cli`。这需要网络连接和写入系统 npm 目录的权限。

## 运行时文件写入

| 文件 | 用途 |
|------|------|
| `~/.openclaw/workspace/secrets.json` | 存储微信公众号 AppID/AppSecret（可选，TOOLS.md 也支持） |
| `~/.openclaw/workspace/wechat-monitor.json` | 文章追踪状态数据 |

## 外部网络调用

| 端点 | 用途 |
|------|------|
| `api.weixin.qq.com` | 发布文章到微信公众号草稿箱 |
| `weixin.sogou.com` | 验证文章是否被搜狗索引收录 |
| `ifconfig.me` | 用户自行查询公网 IP（用于配置微信白名单） |

## 快速开始

**一句话完成全流程：**

> 「帮我写一篇关于 XX 的公众号文章并发布」

→ AI 自动完成：生成封面 + 写稿（去AI味） + 发布草稿箱 + 搜狗验证 + 加入追踪

**手动分步操作：**

1. **生成封面图**（用 `image_generate` 工具）
2. **写文章**（参考下方写作规范）
3. **发布**：`python -X utf8 scripts/publish_and_verify.py <文章.md>`
4. **追踪**：`python -X utf8 scripts/monitor.py add "标题"`
5. **查看状态**：`python -X utf8 scripts/monitor.py status`

## 凭证配置

### 方式 1：secrets.json（推荐）

```bash
python scripts/add.py wechat "微信公众号" appid=YOUR_APPID appsecret=YOUR_APPSECRET
```

### 方式 2：TOOLS.md

```markdown
## WeChat Official Account

export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
```

> 优先从 `secrets.json` 读取，若不存在则 fallback 到 TOOLS.md。

**IP 白名单**：运行前需将本机公网 IP（`curl ifconfig.me` 查询）添加到微信公众号后台 → 开发 → 基本配置 → IP 白名单。

## 写作规范

参考 `references/` 目录：

- **爆款方法论.md** — 标题创作五种类型 + 结构原则
- **写作技巧.md** — 四大内容结构 + 开头结尾写法
- **去AI味指南.md** — 卡兹克风格核心规则 + 四层自检体系（推荐优先使用 khazix-writer skill）

## 脚本说明

### publish_and_verify.py — 发布 + 验证

```bash
python -X utf8 scripts/publish_and_verify.py <文章.md> [主题] [高亮]
```

**frontmatter 格式（必填）：**
```markdown
---
title: 文章标题
cover: ./assets/cover.jpg
---
```

### search_article.py — 独立搜索

```bash
python -X utf8 scripts/search_article.py "文章标题"
```

### monitor.py — 追踪 + 建议

```bash
python -X utf8 scripts/monitor.py add "标题"         # 添加追踪
python -X utf8 scripts/monitor.py check "标题"         # 检查收录
python -X utf8 scripts/monitor.py status               # 列表
python -X utf8 scripts/monitor.py recommend           # 选题建议
```

### add.py / get.py / remove.py / list.py — 凭证管理

```bash
# 添加凭证
python -X utf8 scripts/add.py wechat "微信公众号" appid=YOUR_APPID appsecret=YOUR_APPSECRET

# 获取凭证（完整值，仅本地）
python -X utf8 scripts/get.py wechat appid

# 列举所有凭证（脱敏）
python -X utf8 scripts/list.py

# 删除凭证
python -X utf8 scripts/remove.py wechat
```

## 故障排查

| 问题 | 解决方法 |
|------|---------|
| 发布失败：invalid ip | 将 `curl ifconfig.me` 的 IP 加入微信公众号后台白名单 |
| 发布失败：未能找到文章封面 | 确保 frontmatter 有 `title` 和 `cover` 字段 |
| 搜狗查不到文章 | 新文章需等待 24-72 小时被索引 |
| Python 编码错误 | 加 `python -X utf8` 运行所有脚本 |

## 文件结构

```
wechat-workflow/
├── _meta.json
├── SKILL.md
├── scripts/
│   ├── publish_and_verify.py   # 发布 + 搜狗验证
│   ├── search_article.py      # 独立搜索
│   ├── monitor.py             # 数据追踪 + 选题建议
│   ├── add.py                 # 添加凭证
│   ├── get.py                  # 获取凭证（完整值）
│   ├── remove.py               # 删除凭证
│   └── list.py                 # 列举凭证（脱敏）
└── references/
    ├── 爆款方法论.md
    ├── 写作技巧.md
    └── 去AI味指南.md
```

## 技能整合说明

### 已废弃
~~wechat-publisher~~ — 功能已合并到 wechat-workflow，安装了请卸载。

### 公众号内容全家桶
```
khazix-writer（写作风格 + 四层自检）
    ↓
wechat-workflow（封面 + 发布 + 验证 + 追踪）
```

### 其他公众号技能定位
- **xiawei**：飞书文档 → 公众号，可与 wechat-workflow 共存
- **gongzhonghaoxieshou**：传播学驱动多平台（公众号/小红书/知乎）
- **khazix-writer**：卡兹克风格深度长文

两个公众号写作技能定位不同，可按需选用。
