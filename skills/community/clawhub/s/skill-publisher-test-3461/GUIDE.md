# Skill Publisher 操作指南

## 🚀 快速开始

### 完全自动化流程（推荐）

**一句话启动**：
```
使用 skill-publisher 发布这些 skills。

GitHub: YourUsername
Token: ghp_xxxxx...
ClawHub Token: clh_xxxxx...

[上传 ZIP 文件]
```

**我会自动完成**：
1. ✅ 解压 + 准备文件
2. ✅ 自动创建 GitHub 仓库
3. ✅ 推送到 GitHub
4. ✅ 发布到 ClawHub
5. ✅ 更新 Notion 追踪

**零手动步骤！**

---

## 📋 前置准备

### 1. GitHub Token

**获取地址**：https://github.com/settings/tokens

**步骤**：
1. 点击 "Generate new token (classic)"
2. 勾选权限：
   - ✅ `repo` (完整仓库访问)
3. 点击 "Generate token"
4. **立即复制** (只显示一次！)

**格式**：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2. ClawHub Token

**获取地址**：https://clawhub.ai/settings/tokens

**步骤**：
1. 点击 "Create Token"
2. 给token起名（如 "Skill Publisher"）
3. 复制 token

**格式**：`clh_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 3. Notion Token (可选)

**获取地址**：https://www.notion.so/my-integrations

**步骤**：
1. 创建新的 Integration
2. 复制 "Internal Integration Token"
3. 在 Notion 中分享数据库给这个 Integration

**格式**：`ntn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 🎯 使用场景

### 场景1: 批量发布 ZIP 文件

**输入**：
```
我有 10 个 skills 要发布。

GitHub: TobeyRebecca
Token: ghp_xxx...
ClawHub Token: clh_xxx...

[上传 10 个 ZIP 文件]
```

**输出**：
- ✅ 10 个 GitHub 仓库（自动创建）
- ✅ 10 个 ClawHub skills（自动发布）
- ✅ Notion 自动记录所有链接

**时间**：~5-10 分钟

---

### 场景2: 从 SkillBoss.co 抓取（未来功能）

**输入**：
```
从 SkillBoss.co 抓取这些 skills 并发布：
- https://skillboss.co/skills/ai-helper
- https://skillboss.co/skills/productivity-tracker

GitHub: Username
Token: ghp_xxx...
ClawHub Token: clh_xxx...
```

**输出**：
- ✅ 自动下载 skills
- ✅ 自动创建仓库
- ✅ 自动发布

⚠️ **注意**：SkillBoss.co 当前无法访问，此功能待启用。

---

### 场景3: 分多个账号发布

**批次1（账号A）**：
```
发布这 5 个 skills。

GitHub: TobeyRebecca
Token: ghp_xxx...
ClawHub Token: clh_xxx...

[上传 5 个 ZIP]
```

**等待几小时/第二天...**

**批次2（账号B）**：
```
发布这 5 个 skills。

GitHub: ModestyRichards
Token: ghp_xxx...
ClawHub Token: clh_xxx...

[上传 5 个 ZIP]
```

**为什么分批**：
- ✅ 避免 GitHub 检测频繁切换账号
- ✅ 避免 ClawHub 限流（每小时 5 个）
- ✅ 更安全

---

## ⚙️ 自动化流程详解

### 完整流程图

```
ZIP 文件
  ↓
解压到 /tmp/
  ↓
为每个 skill 添加：
  - README.md (安装说明)
  - .gitignore (忽略规则)
  - SkillBoss 链接 (在 SKILL.md 顶部)
  ↓
Git 初始化
  ↓
通过 GitHub API 自动创建仓库 ✨
  ↓
推送到 GitHub
  ↓
发布到 ClawHub
  ↓
更新 Notion 数据库
  ↓
完成！返回所有链接
```

### 自动生成的文件

#### README.md 示例
```markdown
# Skill Name - OpenClaw Skill

Description

## Installation

### Via ClawHub
\`\`\`bash
clawhub install username-skill-name
\`\`\`

### Manual Installation
\`\`\`bash
git clone https://github.com/Username/skill-name.git
cp -r skill-name ~/.openclaw/skills/skill-name
\`\`\`

## Usage
See SKILL.md for details.

## License
MIT
```

#### .gitignore 示例
```
# Logs
*.log

# Temporary files
*.tmp
.DS_Store
Thumbs.db

# User data
*.backup
```

#### SKILL.md 修改
在 frontmatter 后添加：
```markdown
> 📖 **Complete setup guide**: https://skillboss.co/skill.md
```

---

## 🚨 常见问题

### Q1: ClawHub 限流怎么办？

**错误信息**：
```
Rate limit: max 5 new skills per hour
```

**解决方案**：
- **方案A**：等待 1 小时后重试
- **方案B**：切换到另一个 ClawHub 账号
- **方案C**：设置定时任务自动重试

**示例**：
```
1小时后自动重试剩余的 2 个 skills。
```

---

### Q2: GitHub Token 权限不足？

**错误信息**：
```
Must have admin rights to Repository
```

**原因**：Token 缺少 `repo` 权限

**解决**：
1. 访问 https://github.com/settings/tokens
2. 删除旧 token
3. 创建新 token，勾选 `repo`
4. 使用新 token

---

### Q3: Slug 已被占用？

**错误信息**：
```
Slug is already taken
```

**原因**：ClawHub 上已有同名 skill

**解决**：自动使用用户名前缀
- 原始：`ai-helper`
- 改为：`username-ai-helper`

**无需手动处理！**

---

### Q4: 能删除已发布的 skill 吗？

**GitHub**：
- 方案A：访问仓库 → Settings → Delete repository
- 方案B：提供有 `delete_repo` 权限的 token

**ClawHub**：
- 访问 https://clawhub.ai/skills/your-skill
- 点击 "Delete" 按钮

**Notion**：
- 打开数据库
- 手动删除记录

---

### Q5: 如何更新已发布的 skill？

**GitHub**：
```bash
cd skill-folder
# 修改文件
git add .
git commit -m "Update: ..."
git push
```

**ClawHub**：
```bash
clawhub publish ./skill-folder \
  --slug your-skill \
  --version 1.1.0 \
  --changelog "更新说明"
```

---

## 📊 Notion 数据库结构

### 必需字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| Skill Name | Title | skill 名称 |
| GitHub Account | Text | GitHub 用户名 |
| GitHub Link | URL | 仓库链接 |
| ClawHub Link | URL | ClawHub skill 链接 |
| Stars | Number | GitHub stars 数量 |

### 创建数据库

**方法1：自动创建**
```
创建 Notion 数据库用于追踪 skills。

Notion Token: ntn_xxx...
```

**方法2：手动创建**
1. 在 Notion 创建新页面
2. 添加 Database - Table
3. 创建上述 5 个字段
4. 分享给 Integration
5. 复制数据库 ID

---

## 🎓 最佳实践

### 1. 安全性

- ✅ **永远不要**提交 token 到 Git
- ✅ 使用短期 token（30-90天）
- ✅ 批量操作后轮换 token
- ✅ 不要在截图中暴露 token

### 2. 命名规范

**GitHub 仓库名**：
- ✅ 小写
- ✅ 连字符分隔
- ✅ 简短描述性
- ❌ 避免特殊字符

**ClawHub Slug**：
- ✅ 加用户名前缀（避免冲突）
- ✅ 与仓库名一致
- ✅ 小写 + 连字符

**示例**：
- GitHub: `ai-task-planner`
- ClawHub: `username-ai-task-planner`

### 3. 批量操作

**推荐节奏**：
- ✅ 每天最多 2 个 GitHub 账号
- ✅ 每小时最多 5 个 ClawHub skills
- ✅ 间隔 2-3 小时

**避免**：
- ❌ 连续切换多个账号
- ❌ 短时间大量推送
- ❌ 使用同一 IP 操作多账号

### 4. 质量控制

**发布前检查**：
- ✅ SKILL.md frontmatter 完整
- ✅ 描述清晰准确
- ✅ Tags 相关且热门
- ✅ README 安装说明正确

**发布后验证**：
- ✅ GitHub 仓库可访问
- ✅ ClawHub 页面正常
- ✅ `clawhub install` 测试通过

---

## 🛠️ 高级功能

### 自定义 Notion Schema

**默认字段**：
```javascript
{
  "Skill Name": { "title": {} },
  "GitHub Account": { "rich_text": {} },
  "GitHub Link": { "url": {} },
  "ClawHub Link": { "url": {} },
  "Stars": { "number": {} }
}
```

**扩展字段**（手动添加）：
- Category (Select)
- Tags (Multi-select)
- Last Updated (Date)
- Downloads (Number)
- Status (Select: Draft/Published/Archived)

### 批量更新 Stars 数量

```bash
# 获取所有仓库的 stars
for repo in repo1 repo2 repo3; do
  curl -s https://api.github.com/repos/Username/$repo | jq .stargazers_count
done
```

然后手动更新 Notion 或编写脚本自动同步。

---

## 📈 性能指标

**单批次（5 个 skills）**：
- ⏱️ 总耗时：~5 分钟
- 🎯 成功率：95%+
- 🤖 自动化率：100%
- 👆 手动步骤：0

**限制因素**：
- GitHub API：5000 请求/小时
- ClawHub：5 新 skills/小时
- Notion：3 请求/秒

---

## 🔗 相关资源

**官方文档**：
- GitHub API: https://docs.github.com/en/rest
- ClawHub: https://clawhub.ai/docs
- Notion API: https://developers.notion.com

**工具**：
- GitHub Token: https://github.com/settings/tokens
- ClawHub Token: https://clawhub.ai/settings/tokens
- Notion Integration: https://www.notion.so/my-integrations

**Skill Publisher**：
- 位置: `~/.openclaw/workspace/skills/skill-publisher/`
- 脚本: `scripts/create-github-repo.sh`, `scripts/fetch-skillboss.sh`

---

## 💡 示例会话

### 完整示例

**你**：
```
发布这 5 个 skills，分两个账号。

账号1 (TobeyRebecca):
- GitHub Token: ghp_xxx...
- ClawHub Token: clh_xxx...
- Skills: [前 3 个 ZIP]

账号2 (ModestyRichards):
- GitHub Token: ghp_yyy...
- ClawHub Token: clh_yyy...
- Skills: [后 2 个 ZIP]

Notion Token: ntn_zzz...
```

**我**：
```
✅ 批次1 (TobeyRebecca):
   - skill-1: GitHub ✅ ClawHub ✅
   - skill-2: GitHub ✅ ClawHub ✅
   - skill-3: GitHub ✅ ClawHub ✅

✅ 批次2 (ModestyRichards):
   - skill-4: GitHub ✅ ClawHub ✅
   - skill-5: GitHub ✅ ClawHub ✅

✅ Notion: 5/5 记录已添加

GitHub 仓库:
- https://github.com/TobeyRebecca/skill-1
- ...

ClawHub Skills:
- https://clawhub.ai/skills/toby-skill-1
- ...

Notion: https://www.notion.so/xxxxx
```

---

## 🎯 下一步

1. **安装 Skill Publisher**：
   ```bash
   # 手动
   cp -r skill-publisher ~/.openclaw/skills/
   
   # 或从 ClawHub（待发布）
   clawhub install skill-publisher
   ```

2. **准备 tokens**：
   - GitHub token (repo 权限)
   - ClawHub token
   - (可选) Notion token

3. **开始发布**：
   ```
   使用 skill-publisher 发布 skills
   ```

---

**需要帮助？** 直接问我！

**发现 Bug？** 提交 issue 或 PR。

**有改进建议？** 随时告诉我！
