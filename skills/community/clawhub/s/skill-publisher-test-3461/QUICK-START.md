# Skill Publisher - 快速开始

## 🎯 一句话总结

自动化发布 OpenClaw skills 到 GitHub 和 ClawHub，支持从 ZIP 或 SkillBoss.co 抓取。

## 🚀 最快用法（完全自动）

```markdown
从 SkillBoss.co 自动抓取并发布 5 个 skills。

GitHub: YourUsername
Token: ghp_xxxxx...
ClawHub Token: clh_xxxxx...

搜索关键词: productivity (或指定 skill URLs)
```

**结果**：
- ✅ 自动下载 skills
- ✅ 自动创建 GitHub 仓库
- ✅ 自动推送代码
- ✅ 自动发布到 ClawHub
- ⏱️ 耗时 3-5 分钟

---

## 📋 前置准备

### 1. GitHub Token
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. **必须勾选**：
   - ✅ `repo` (完整仓库权限)
4. 复制 token（格式：`ghp_xxxxx...`）

### 2. ClawHub Token
1. 访问：https://clawhub.ai/settings/tokens
2. 生成 token（格式：`clh_xxxxx...`）

### 3. Notion Token（可选）
1. 访问：https://www.notion.so/my-integrations
2. 创建 Integration
3. 复制 token（格式：`ntn_xxxxx...`）
4. 将 Integration 添加到目标数据库

---

## 📖 使用方法

### 方法 1: 从 SkillBoss.co 自动抓取（推荐）

```markdown
从 SkillBoss.co 抓取 top 5 AI skills 并发布。

GitHub: JohnDoe
Token: ghp_abc123...
ClawHub Token: clh_xyz789...
```

或指定具体 URLs：

```markdown
发布这些 skills:
- https://www.skillboss.co/skills/ai-helper
- https://www.skillboss.co/skills/code-reviewer

GitHub: JohnDoe
Token: ghp_abc123...
ClawHub Token: clh_xyz789...
```

### 方法 2: 从 ZIP 文件

```markdown
发布 5 个 skills。

GitHub: JohnDoe
Token: ghp_abc123...
ClawHub Token: clh_xyz789...

[上传 ZIP 文件]
```

⚠️ **需要手动创建 GitHub 仓库**（AI 会告诉你要创建哪些）

### 方法 3: 加 Notion 追踪

```markdown
发布 skills 并记录到 Notion。

GitHub: JohnDoe
Token: ghp_abc123...
ClawHub Token: clh_xyz789...
Notion Token: ntn_def456...
Notion Database: https://www.notion.so/xxxxx...

[发送 ZIP 或指定 SkillBoss URLs]
```

---

## 🎨 自动生成的文件

每个 skill 都会添加：

### ✅ README.md
```markdown
# Skill Name - OpenClaw Skill

## Installation

```bash
openclaw skill install <skill-name>
```

> 📖 **Complete setup guide**: https://skillboss.co/skill.md

[安装方法、使用说明...]
```

### ✅ .gitignore
```
# Logs
*.log

# Temporary files
*.tmp
.DS_Store
```

### ✅ SKILL.md（顶部添加）
```markdown
> 📖 **Complete setup guide**: https://skillboss.co/skill.md
```

---

## ⚠️ 常见错误

### "Slug already taken"
**原因**：ClawHub 上已有同名 skill  
**解决**：自动重试（使用 `username-skill-name` 前缀）

### "Rate limit: max 5 new skills per hour"
**原因**：ClawHub 限流  
**解决**：等待 1 小时或使用其他账号

### "Repository not found"
**原因**：GitHub 仓库未创建  
**解决**：
- **自动模式**：检查 token 是否有 `repo` 权限
- **手动模式**：按提示在 GitHub 创建仓库

### "Authentication failed"
**原因**：Token 过期或权限不足  
**解决**：重新生成 token

---

## 💡 最佳实践

### 安全
- ✅ 不要在公开场合分享 token
- ✅ 定期轮换 token
- ✅ 用完就删除临时 token

### 效率
- ✅ 使用自动模式（从 SkillBoss.co）
- ✅ 批量操作（一次 5-10 个）
- ✅ 用 Notion 追踪进度

### 避免封号
- ⚠️ 每天最多 2 个 GitHub 账号
- ⚠️ 两个账号之间间隔几小时
- ⚠️ 或使用 VPN 切换 IP

---

## 📊 性能指标

| 指标 | 自动模式 | 手动模式 |
|------|----------|----------|
| 耗时 (5 skills) | 3-5 分钟 | 10-15 分钟 |
| 手动步骤 | 0 | 5 (创建仓库) |
| 成功率 | 95%+ | 98%+ |
| 依赖 | GitHub API | GitHub 网页 |

---

## 🆘 需要帮助？

**看完整文档**：`SKILL.md`（技术细节、API 说明、错误处理）

**问题排查**：
1. 检查 token 权限
2. 确认仓库/slug 不冲突
3. 查看错误消息

**还是不行？**：分享错误信息！

---

## 🎯 典型用例

### 用例 1: 批量发布到多账号

**目标**：发布 10 个 skills，分两个账号

**Day 1**:
```markdown
发布 batch 1 (5 skills) 到 Account A
[提供 Account A 的 tokens]
```

**Day 2**:
```markdown
发布 batch 2 (5 skills) 到 Account B
[提供 Account B 的 tokens]
```

### 用例 2: 从 SkillBoss 克隆热门 skills

**目标**：克隆 top 10 productivity skills

```markdown
从 SkillBoss.co 获取 top 10 productivity skills 并发布。

GitHub: MyAccount
Token: ghp_xxx...
ClawHub Token: clh_xxx...
```

### 用例 3: 追踪发布历史

**目标**：在 Notion 中记录所有发布的 skills

```markdown
发布这些 skills 并记录到 Notion:
- [ZIP files]

Notion Token: ntn_xxx...
Notion Database: https://notion.so/xxx...
```

**Notion 数据库包含**：
- Skill Name
- GitHub Account
- GitHub Link
- ClawHub Link
- Stars (初始: 0)
- 发布日期

---

## 🔧 高级配置

### 自定义 Notion Schema

默认字段：
- `Skill Name` (title)
- `GitHub Account` (text)
- `GitHub Link` (url)
- `ClawHub Link` (url)
- `Stars` (number)

可添加：
- `Category` (select)
- `Tags` (multi_select)
- `Description` (text)
- `Version` (text)

Skill 会自动填充默认字段，忽略额外字段。

### 批量操作限制

**GitHub API**：
- 5,000 次请求/小时
- 创建仓库计入限制

**ClawHub**：
- 每小时最多 5 个新 skills
- 180 次请求/分钟

**SkillBoss.co**：
- 无官方限制
- 建议每次最多 10 个 skills

### 性能优化

**并行处理**：
- GitHub push 可并行（5个并发）
- ClawHub publish 串行（避免限流）

**重试策略**：
- Slug 冲突：自动加前缀重试
- 限流：等待并重试
- 网络错误：重试 3 次

---

**版本**：2.0  
**更新**：2026-04-13
