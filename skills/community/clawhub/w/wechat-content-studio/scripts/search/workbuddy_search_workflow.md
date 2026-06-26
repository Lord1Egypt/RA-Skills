# WorkBuddy WebSearch 集成方案

## 核心思路

由于 `web_search` 是 Agent 专用工具，Node.js 脚本无法直接调用，我们采用以下工作流：

```
Agent 调用 web_search → 解析结果 → 调用 wechat-content-studio links 命令 → 后续流程
```

## 使用方法

### 方案 A：使用 keyword-search 技能（推荐）

```bash
# 1. 使用 keyword-search 搜索文章 URL
keyword-search 搜索 "RAG 幻觉治理" --limit 10

# 2. 使用 wechat-content-studio 处理搜索到的 URL
node {baseDir}/scripts/main.js links "URL1,URL2,URL3" --merge

# 3. 后续流程（改写、封面、发布）
node {baseDir}/scripts/main.js rewrite ./wechat-content-studio/文章标题/article.md
node {baseDir}/scripts/main.js generate-cover --title "文章标题"
```

### 方案 B：Agent 直接使用 web_search 工具

Agent 在执行 `wechat-content-studio` 的搜索任务时：

1. **不调用** `node scripts/main.js search` 命令
2. **直接使用** `web_search` 工具搜索：
   ```
   query: "RAG 幻觉治理" site:mp.weixin.qq.com OR site:zhihu.com OR site:juejin.cn
   ```
3. **提取** 搜索结果中的 URL 列表
4. **调用** `wechat-content-studio links` 命令处理这些 URL

## 搜索查询模板

### 微信公众号（全网）
```
"关键词" site:mp.weixin.qq.com
```

### 微信公众号（指定账号）
```
"公众号名" "关键词" site:mp.weixin.qq.com
```

### 多来源组合
```
"关键词" site:mp.weixin.qq.com OR site:zhihu.com OR site:juejin.cn OR site:blog.csdn.net
```

### 带时间范围
```
"关键词" site:mp.weixin.qq.com after:2026-05-01
```

## 搜索引擎对比

| 特性 | Brave Search | WorkBuddy WebSearch |
|------|-------------|---------------------|
| 配置要求 | 需代理 (HTTPS_PROXY) | 开箱即用 |
| 支持站点 | 所有（site: 语法） | 所有（site: 语法） |
| 限流风险 | 有（429 错误） | 无 |
| 中文结果 | 一般 | 更优 |
| 推荐使用 | ❌ 不推荐 | ✅ 推荐 |

## 迁移指南

### 原命令（Brave Search）
```bash
node scripts/main.js search "RAG" --merge --sources high_quality_channels
```

### 新工作流（WorkBuddy WebSearch）
```bash
# 方法 1：使用 keyword-search 技能
keyword-search 搜索 "RAG" --limit 20
node scripts/main.js links "URL1,URL2,URL3" --merge

# 方法 2：Agent 直接使用 web_search 工具
# （见上方"方案 B"）
```

## 代码适配建议

如需在 `wechat-content-studio` 代码中集成 WorkBuddy 搜索，建议：

1. **保留现有 Brave Search 代码**（向后兼容）
2. **添加搜索策略选择参数**：
   ```bash
   node scripts/main.js search "RAG" --engine workbuddy
   ```
3. **当 `--engine workbuddy` 时**：
   - 不调用 `multi_source_search.js`
   - 输出查询字符串，提示 Agent 使用 `web_search` 工具
   - Agent 解析结果后继续后续流程

## 环境变量配置

无需额外配置！WorkBuddy WebSearch 开箱即用。

如需禁用 Brave Search 的代理配置，可设置：
```bash
export DISABLE_BRAVE_SEARCH=true
```

## 示例工作流

```bash
# 完整流程示例
# 1. Agent 使用 web_search 搜索
web_search("RAG 幻觉治理 site:mp.weixin.qq.com OR site:zhihu.com")

# 2. 提取 URL 列表
urls = ["https://...", "https://...", ...]

# 3. 调用 wechat-content-studio 处理
node scripts/main.js links "url1,url2,url3" --merge --rewrite --generate-cover --publish
```

## 注意事项

1. **不要修改现有 Brave Search 代码** —— 保留作为备选方案
2. **推荐用户优先使用 keyword-search 技能** —— 已优化用于 WorkBuddy WebSearch
3. **wechat-content-studio 专注于内容处理** —— 搜索、合并、改写、发布

---

**更新日期**: 2026-05-24  
**版本**: 1.0.0
