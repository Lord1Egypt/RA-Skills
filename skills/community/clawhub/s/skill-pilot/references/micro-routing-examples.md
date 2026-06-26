# 微路由示例 (Micro Routing Examples)

使用这些示例保持发现 vs 复用行为的稳定性。

---

## 示例 1: 用户要求安装新技能，但已安装技能已足够

### 已安装技能
- `github`: GitHub issues, PRs, releases, runs
- `clawhub`: 发布和管理技能

### 用户请求
"给我装一个处理 GitHub issue 的技能"

### 期望路由
- 优先复用
- 推荐 `github` 而非跳转到发现

### 良好回答
"你现在已经有能覆盖这个任务的 `github` skill，先不用装新的。只有现有流程明显不够时，再去找更专门的 skill。"

### 不良回答
"好的，我来帮你找 GitHub issue 相关的技能..." (直接跳到发现)

---

## 示例 2: 无强匹配的已安装技能

### 已安装技能
- `github`
- `weather`

### 用户请求
"帮我控制浏览器点一下这个按钮"

### 期望路由
- 不假装浏览器技能存在
- 路由到发现

### 良好回答
"我现在没看到已安装的强匹配浏览器控制 skill。先走 `find-skills` 找候选；如果来源陌生，先用 `skill-vetter` 过一遍。"

### 不良回答
"我用 `github` 帮你..." (错误匹配)
"浏览器控制很简单，我自己来做..." (不推荐技能)

---

## 示例 3: 未知的第三方候选

### 已安装技能
- `find-skills`
- `skill-vetter`

### 用户请求
"有没有帮我备份 OpenClaw 的技能？"

### 期望路由
- 先发现
- 审查陌生候选再推荐安装

### 良好回答
"先用 `find-skills` 看有没有备份类 skill；如果候选来自陌生第三方，先过 `skill-vetter`，再决定装不装。"

---

## 示例 4: 多个技能可能适用

### 已安装技能
- `multi-search-engine` (17 引擎搜索)
- `exa-web-search-free` (AI 优化搜索)
- `tavily-search` (AI 深度搜索)

### 用户请求
"搜索一下 2026 AI Agent 技术趋势"

### 期望路由
- 根据场景选择最优
- 中文内容 → `multi-search-engine`
- 技术深度 → `exa-web-search-free`

### 良好回答
"这是中文技术搜索，用 `multi-search-engine` 最合适 (百度 + 谷歌 + 微信)。如果需要更深的技术分析，备选 `exa-web-search-free`。"

---

## 示例 5: 反爬网站抓取

### 已安装技能
- `web_fetch` (基础抓取)
- `scrapling-fetch` (反爬绕过)
- `browser` (交互式)

### 用户请求
"帮我抓取这篇微信文章的内容"

### 期望路由
- 识别反爬需求
- 优先 `scrapling-fetch`

### 良好回答
"微信文章有反爬，用 `scrapling-fetch`。如果失败，备选 `browser` 交互式抓取。"

### 不良回答
"用 `web_fetch`..." (可能失败)
"我来帮你抓取..." (不推荐技能)

---

## 示例 6: 技能选择不是有意义的决策

### 已安装技能
- `weather` (天气预报)

### 用户请求
"北京今天天气怎么样？"

### 期望路由
- 静默执行
- 不输出技能选择过程

### 良好回答
"北京今天晴，最高 25°C，最低 15°C。" (直接回答)

### 不良回答
"我使用 `weather` skill 来查询..." (暴露技能选择)

---

## 示例 7: 中文内容搜索

### 已安装技能
- `multi-search-engine` (支持百度/微信/搜狗)
- `exa-web-search-free` (国际搜索)

### 用户请求
"搜索一下 国产 AI Agent 框架有哪些"

### 期望路由
- 识别中文内容
- 优先国内引擎

### 良好回答
"这是中文内容搜索，用 `multi-search-engine` (百度 + 微信 + 搜狗)。"

---

## 示例 8: 技术代码搜索

### 已安装技能
- `multi-search-engine`
- `exa-web-search-free` (代码搜索优化)

### 用户请求
"找一下 Python asyncio 的 best practices"

### 期望路由
- 识别技术内容
- 优先 `exa-web-search-free`

### 良好回答
"这是技术搜索，用 `exa-web-search-free` (对代码/文档优化)。备选 `multi-search-engine` (GitHub 搜索)。"

---

## 决策原则总结

| 场景 | 决策 |
|------|------|
| 已安装技能足够 | ✅ 推荐复用 |
| 无强匹配 | ⚠️ 路由到发现 |
| 第三方候选 | 🔍 先审查后推荐 |
| 多技能适用 | 📊 根据场景选择 |
| 反爬/特殊需求 | 🎯 推荐专用技能 |
| 简单明确任务 | 🤫 静默执行 |

---

*参考：skillhub skill-router micro-routing-examples.md*  
*最后更新：2026-03-17*
