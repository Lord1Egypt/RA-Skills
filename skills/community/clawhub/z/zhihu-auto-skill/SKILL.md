---
name: zhihu-automation
description: >-
  知乎自动化 Skill（双通道）。发布文章（专栏）、发布想法、回答问题、提问、
  互动（点赞/评论/关注）、数据提取（热榜/搜索/用户/问题）。使用 Playwright 
  浏览器自动化 + HTTP API 双通道，Cookie 持久化登录。

  Trigger phrases:
  - "帮我发一篇知乎文章" / "写知乎文章"
  - "发布知乎想法" / "发一条想法"
  - "回答知乎问题" / "写回答"
  - "知乎提问" / "问一个问题"
  - "点赞" / "评论" / "关注"（知乎内容）
  - "查看知乎热榜" / "知乎热搜"
  - "搜索知乎" / "查一下知乎上的"
  - "知乎数据" / "提取知乎信息"
metadata:
  author: Hermes + WorkBuddy
  version: "2.0.0"
  requires:
    - node
    - playwright
    - python3
  env:
    - ZHIHU_COOKIE_KEY
    - ZHIHU_APP_KEY (optional)
    - ZHIHU_APP_SECRET (optional)
---

# 知乎自动化 Skill (Zhihu Automation v2.0)

双通道架构：HTTP 读（热榜/搜索/用户/问题）+ 浏览器写（发布/互动）。

---

## 快速开始

### 1. 安装依赖
```bash
# 依赖已安装，如首次使用：
cd zhihu-skill
npm install
npx playwright install chromium
```

### 2. 配置 Cookie 加密密钥
```bash
export ZHIHU_COOKIE_KEY="$(openssl rand -hex 32)"
```

### 3. 导出知乎 Cookie
```bash
# 会自动打开浏览器，手动登录后 Cookie 自动加密保存
node scripts/zhihu-export-cookie.js
```

### 4. 验证
```bash
# 检查 Cookie 是否有效
node tests/cookie-check.js
```

---

## 功能模块

### 1️⃣ 发布文章
在知乎专栏发布 Markdown 文章。

```
你: 帮我发一篇知乎文章，标题是"xxx"，内容是...
AI: 正在生成内容 → 打开编辑器 → 发布 → 返回链接
```

**CLI:**
```bash
# 直接指定内容
node scripts/zhihu-publish.js article --title "标题" --content "正文"

# 从文件读取内容
node scripts/zhihu-publish.js article --title "标题" --content-file "文章.md"

# 保存为草稿（不发布）
node scripts/zhihu-publish.js article --title "标题" --content "正文" --draft
```

### 2️⃣ 发布想法
类似 Twitter 的短内容发布。

```
你: 发一条知乎想法，内容是xxx
```

**CLI:**
```bash
node scripts/zhihu-publish.js thought --content "想法内容"

# 带图片
node scripts/zhihu-publish.js thought --content "想法内容" --image "图片路径"
```

### 3️⃣ 回答问题
搜索问题并撰写回答。

```
你: 帮我在知乎搜索关于xxx的问题并回答
AI: 搜索问题 → 列出选项 → 用户选择 → 撰写 → 提交
```

**CLI:**
```bash
node scripts/zhihu-answer.js --question-id 123456789 --content "回答内容"
```

### 4️⃣ 提问
在知乎上提出新问题。

```
你: 帮我在知乎提问：xxx
AI: 打开提问页 → 填写标题 → 补充详情 → 提交
```

**CLI:**
```bash
node scripts/zhihu-ask.js --title "问题标题" --detail "补充说明"
```

### 5️⃣ 互动
点赞、评论、关注。

```
你: 给这篇知乎文章点赞 / 评论 / 关注这个用户
```

**CLI:**
```bash
# 点赞
node scripts/zhihu-interact.js like --url "https://www.zhihu.com/question/xxx/answer/xxx"

# 取消点赞
node scripts/zhihu-interact.js unlike --url "..."

# 评论
node scripts/zhihu-interact.js comment --url "..." --content "评论内容"

# 关注用户
node scripts/zhihu-interact.js follow --user "用户ID"
```

### 6️⃣ 数据提取
从知乎提取结构化数据。

```
你: 今天知乎热榜是什么？
AI: 返回热榜 Top 20
```

**CLI:**
```bash
# 热榜
node scripts/zhihu-extract.js --type hot-list [--limit 20]

# 搜索
node scripts/zhihu-extract.js --type search --query "关键词" [--limit 10]

# 文章详情
node scripts/zhihu-extract.js --type article --id "文章ID"

# 用户信息
node scripts/zhihu-extract.js --type user --id "用户ID"

# 问题详情
node scripts/zhihu-extract.js --type question --id "问题ID"

# 回答列表
node scripts/zhihu-extract.js --type answers --id "问题ID" [--limit 10]
```

---

## 架构

```
                   AI Agent（用户自然语言触发）
                           │
                  ┌────────▼────────┐
                  │  Skill 调度层    │
                  │  SKILL.md → 路由  │
                  └────────┬────────┘
                           │
                  ┌────────▼────────┐
                  │  双通道决策      │
                  │  读操作→HTTP    │
                  │  写操作→浏览器  │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
    ┌─────────▼─────┐ ┌───▼────┐ ┌─────▼─────────┐
    │ HTTP 通道     │ │ 浏览器  │ │ Python        │
    │ zhihu-http.js │ │ 通道   │ │ OpenAPI       │
    │ zhihu-extract │ │ 自动化  │ │ zhihu_bot.py  │
    │ zhihu-signature│ │ publish│ │ zhihu-bridge  │
    └───────────────┘ │ interact│ └───────────────┘
                      │ answer  │
                      │ ask     │
                      └─────────┘
```

## 安全

- Cookie 使用 **AES-256-GCM** 加密存储（权限 0600）
- 环境变量 `ZHIHU_COOKIE_KEY` 管理加密密钥
- 支持密钥轮换（`rotateCookieKey`）

### Cookie 加密格式
```
~/.hermes/credentials/zhihu-cookies.enc
├── [12 bytes: 随机 IV]
├── [16 bytes: GCM 认证标签]
└── [AES-256-GCM 加密的 Cookie 数据]
```

## 环境变量

| 变量 | 必填 | 说明 |
|------|:----:|------|
| `ZHIHU_COOKIE_KEY` | ✅ | Cookie 加密密钥（`openssl rand -hex 32` 生成） |
| `ZHIHU_APP_KEY` | ❌ | 知乎 OpenAPI app_key（圈子互动） |
| `ZHIHU_APP_SECRET` | ❌ | 知乎 OpenAPI app_secret |
| `ZHIHU_PROXY` | ❌ | 代理地址（反爬场景） |
| `CAPTCHA_API_KEY` | ❌ | 打码平台 Key |

## 测试

```bash
# 选择器冒烟测试
node tests/smoke-test.js

# Cookie 到期检测
node tests/cookie-check.js

# 端到端集成测试（沙箱模式）
ZHIHU_TEST_MODE=sandbox node tests/e2e-test.js
```

## 注意事项

- ⚠️ **频率控制**：HTTP 200-500ms 间隔，浏览器 5-10s 间隔
- ⚠️ **Cookie 有效期**：约 30 天，到期需重新登录导出
- ⚠️ **知乎改版**：`config/selectors.json` 可能需更新
- ⚠️ **签名失效自动降级**：C3b 失败自动切换 Plan B（浏览器通道）
- ⚠️ **浏览器崩溃恢复**：withCrashRecovery 自动重建会话
