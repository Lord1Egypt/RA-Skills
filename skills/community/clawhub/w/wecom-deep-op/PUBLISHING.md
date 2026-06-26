# 发布 wecom-deep-op 到 GitHub 与 Clawhub 完整指南

## 📦 1. 准备发布

### 1.1 代码清单检查

确保以下文件完整且内容正确：

- [x] `src/index.ts` - 源代码
- [x] `package.json` - 包含 `"files": ["dist", "src", "SKILL.md", "README.md", "CHANGELOG.md", "LICENSE", "skill.yml"]`
- [x] `tsconfig.json` - TypeScript 配置
- [x] `rollup.config.js` - 构建配置
- [x] `skill.yml` - Clawhub 元数据（**注意：不包含任何真实 uaKey**）
- [x] `README.md` - 完整使用文档
- [x] `CHANGELOG.md` - 版本历史
- [x] `LICENSE` - MIT License
- [x] `.gitignore` - 排除 node_modules, dist, env 等
- [x] `SKILL.md` - OpenClaw 技能描述（已在根目录）

### 1.2 敏感信息扫描（重要！）

**必须确保以下内容不会出现在发布版本中：**

```bash
# 检查是否有硬编码的 uaKey、token、密码等
grep -r "uaKey" . --exclude-dir=node_modules --exclude="*.json" | grep -v "YOUR_UA_KEY"
grep -r "WECOM_" . --exclude-dir=node_modules | grep -v "BASE_URL"
grep -r "password\|token\|secret" . --exclude-dir=node_modules

# 如果有，立即删除或替换为占位符
```

**检查 `skill.yml`：**
- ✅ 只能包含占位符说明，无真实值
- ✅ 只声明依赖，不包含配置

**检查 `README.md`：**
- ✅ 示例中的 `uaKey` 必须是 `YOUR_UA_KEY` 或 `YOUR_COMBINED_KEY`
- ✅ 不能包含我自己的任何实际配置

---

## 🐙 2. 创建 GitHub 仓库

### 2.1 在 GitHub.com 创建仓库

1. 登录 GitHub，点击右上角 `+` → `New repository`
2. 仓库名：`wecom-deep-op`
3. Description: `Enterprise WeChat all-in-one OpenClaw skill`
4. **不要**初始化 README、.gitignore 或 LICENSE（本地已有）
5. 点击 `Create repository`

### 2.2 本地初始化 Git 并推送

```bash
cd /root/.openclaw/workspace/skills/wecom-deep-op

# 初始化 git（如果还未初始化）
git init
git branch -M main

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/wecom-deep-op.git

# 检查文件状态
git status

# 提交所有文件
git add .
git commit -m "feat: initial release - wecom-deep-op v1.0.0

- unified wrapper for all WeCom MCP services
- supports doc, schedule, meeting, todo, contact
- TypeScript implementation with full type definitions
- MIT licensed"

# 推送
git push -u origin main
```

---

## 🔖 3. 创建 Git Tag 并发布 Release

### 3.1 创建版本 Tag

```bash
# 创建 v1.0.0 tag
git tag -a v1.0.0 -m "wecom-deep-op v1.0.0 - First stable release"

# 推送 tag 到 GitHub
git push origin v1.0.0
```

### 3.2 创建 GitHub Release

1. 访问 GitHub 仓库页面 → `Releases` → `Draft a new release`
2. Tag: 选择 `v1.0.0`
3. Release title: `v1.0.0 - Enterprise WeChat All-in-One Skill`
4. Description:

```markdown
## 🎉 wecom-deep-op v1.0.0 正式发布

### ✨ 新功能
- 统一封装企业微信文档、日程、会议、待办、通讯录
- 基于官方插件 `@wecom/wecom-openclaw-plugin` v1.0.13
- 完整 TypeScript 类型定义
- 生产环境就绪

### 📦 安装
```bash
clawhub install wecom-deep-op
```

### 📖 文档
- [Complete README](https://github.com/YOUR_USERNAME/wecom-deep-op/blob/main/README.md)
- [Skill Metadata](https://github.com/YOUR_USERNAME/wecom-deep-op/blob/main/skill.yml)

### 🔐 安全说明
⚠️ **本 Skill 不会也不应包含任何企业微信 uaKey 或 token**。
用户需要自行完成 BOT 授权和配置，详见 README 安全章节。

### 🐛 已知问题
无

### 🙏 致谢
基于腾讯企业微信官方 OpenClaw 插件构建。

---

**Full Changelog**: https://github.com/YOUR_USERNAME/wecom-deep-op/compare/...v1.0.0
```

5. 点击 `Publish release`

---

## 🚀 4. 发布到 Clawhub

### 4.1 准备 Clawhub 账户

1. 访问 [Clawhub.com](https://clawhub.com) 并注册/登录
2. 进入 `Settings` → `API Tokens`
3. 创建新 Token（权限：`publish:skills`）
4. 复制 Token（妥善保存）

### 4.2 本地登录 Clawhub CLI

```bash
# 如果未安装 Clawhub CLI，先安装
npm install -g @clawhub/cli

# 登录
clawhub login
# 粘贴刚才复制的 API Token
```

### 4.3 dry-run 预览（检查发布内容）

```bash
cd /root/.openclaw/workspace/skills/wecom-deep-op

# 预览发布包内容
clawhub publish . --dry-run --output json | jq '.'

# 检查重点：
# - files 列表应只包含必要的文件（排除 node_modules, .git 等）
# - skill.yml 已正确读取
# - 无敏感信息泄露
```

如果 `dry-run` 显示有不应发布文件（如 `.env`、`mcporter.json`），检查 `.clawhubignore`。

### 4.4 创建 .clawhubignore（如果还没有）

```bash
cat > .clawhubignore << 'EOF'
node_modules/
dist/.cache?
.git/
.env
.env.*
*.local
mcporter.json
secrets.json
credentials.json
npm-debug.log
coverage/
test/
.vscode/
.idea/
*.swp
*.swo
.DS_Store
EOF
```

### 4.5 正式发布

```bash
# 发布 latest tag
clawhub publish . --tag latest

# 同时发布为 v1.0.0 版本
clawhub publish . --tag v1.0.0
```

**预期输出：**
```json
{
  "success": true,
  "skill": "wecom-deep-op",
  "version": "1.0.0",
  "downloads": 0,
  "url": "https://clawhub.com/skills/wecom-deep-op"
}
```

### 4.6 验证发布

```bash
# 查看技能信息
clawhub info wecom-deep-op

# 列出所有版本
clawhub versions wecom-deep-op
```

访问 `https://clawhub.com/skills/wecom-deep-op` 查看发布的页面。

---

## 🧪 5. 测试安装

在新环境或新用户会话中测试：

```bash
# 列出可用技能
clawhub list

# 搜索
clawhub search wecom

# 安装（从Clawhub）
clawhub install wecom-deep-op

# 或使用 openclaw 命令
openclaw skill add wecom-deep-op
```

验证安装后，运行：
```bash
wecom_mcp call wecom-deep-op.ping "{}"
```

---

## 📝 6. 后续维护

### 6.1 版本更新工作流

1. 修改代码，更新 `CHANGELOG.md` 和 `package.json` 版本
2. 提交：`git commit -m "feat: new feature"`
3. 构建：`npm run build`
4. 打 tag：`git tag -a v1.1.0 -m "v1.1.0"`
5. 推送：`git push && git push origin v1.1.0`
6. GitHub Release：创建新的 Release 页面
7. Clawhub：`clawhub publish . --tag v1.1.0`

### 6.2 用户反馈

- 在 GitHub Repo 的 `Issues` 中收集 bug 报告和功能请求
- 在 Clawhub 技能页面回复用户评论
- 定期查看 `clawhub install` 的下载统计

---

## 🚨 7. 安全复查清单（发布前必读）

- [ ] **代码中无任何真实 `uaKey`, `token`, `secret`**
- [ ] **所有示例中的密钥都是占位符**（如 `YOUR_UA_KEY`）
- [ ] **`.env`、`mcporter.json` 在 `.gitignore` 和 `.clawhubignore` 中**
- [ ] **`package.json` 的 `dependencies` 中无敏感信息**
- [ ] **`skill.yml` 只声明依赖，不包含配置**
- [ ] **LICENSE 文件正确（MIT）**
- [ ] **README 中强调安全配置和最小权限原则**
- [ ] **更新 `skill.yml` 的 `dependencies` 版本范围为 `>=1.0.13`（官方插件）**
- [ ] **测试安装流程是否顺畅，文档是否清晰**

---

## 🎯 8. 一键发布脚本（可选）

创建 `scripts/publish.mjs` 简化流程：

```javascript
#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');

console.log('🚀 Starting publish process for wecom-deep-op...');

// 1. 安全检查
console.log('🔒 Running security check...');
execSync('grep -r "uaKey" . --exclude-dir=node_modules --exclude="*.json" || echo "No hardcoded keys found"', { stdio: 'inherit' });

// 2. Build
console.log('🔨 Building...');
execSync('npm run build', { stdio: 'inherit' });

// 3. Git tag
const version = require('./package.json').version;
console.log(`🏷️  Tagging v${version}...`);
execSync(`git tag -a v${version} -m "v${version}"`, { stdio: 'inherit' });

// 4. Push
console.log('📤 Pushing to GitHub...');
execSync('git push && git push origin --tags', { stdio: 'inherit' });

// 5. Clawhub dry-run
console.log('👀 Clawhub dry-run...');
execSync('clawhub publish . --dry-run', { stdio: 'inherit' });

// 6. Confirm
console.log('✅ Ready to publish. Run:');
console.log(`   clawhub publish . --tag ${version} --tag latest`);

module.exports = {};
```

使用：
```bash
node scripts/publish.mjs
```

---

## 🎊 发布完成！

完成后：
- ✅ GitHub 仓库公开可用
- ✅ Clawhub 技能页面可访问
- ✅ 用户可通过 `clawhub install wecom-deep-op` 安装
- ✅ 所有文档已就位

**恭喜！你为 OpenClaw 社区贡献了一个强大的企业微信集成 Skill！** 🚀

---

**注意**：本指南基于你当前的环境（root 权限，本地开发）编写。实际发布时请根据 GitHub 和 Clawhub 的最新UI调整操作步骤。
