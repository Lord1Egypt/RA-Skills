# 🚀 Clawhub 发布指南

## 前置准备

### 1. 注册 Clawhub 账户

1. 访问 [Clawhub.com](https://clawhub.com)
2. 注册账号
3. 进入 `Settings` → `API Tokens`
4. 创建新 Token（权限：`publish:skills`）
5. 复制 Token（妥善保存）

### 2. 安装 Clawhub CLI

```bash
# 如果未安装
npm install -g @clawhub/cli

# 验证安装
clawhub --version
```

### 3. 登录 Clawhub

```bash
clawhub login
# 粘贴刚才复制的 API Token
```

---

## 发布流程

### 1. 安全检查（重要！）

在发布前，确保没有硬编码的敏感信息：

```bash
# 检查是否有硬编码的 uaKey
grep -r "uaKey" . --exclude-dir=node_modules --exclude="*.json" | grep -v "YOUR_UA_KEY"

# 检查是否有硬编码的 token/secret
grep -r "token\|secret\|password" . --exclude-dir=node_modules --exclude="*.json" | grep -v "YOUR_"

# 检查是否有 mcporter.json 或 .env
ls -la .env mcporter.json secrets.json 2>/dev/null || echo "No sensitive files found"
```

**如果发现问题，立即删除或替换为占位符！**

### 2. 构建 Skill

```bash
cd /root/.openclaw/workspace/skills/wecom-deep-op

# 构建
npm run build

# 预期输出：
# dist/index.cjs.js
# dist/index.esm.js
# dist/index.d.ts
```

### 3. dry-run 预览

```bash
# 预览发布包内容
clawhub publish . --dry-run --output json | jq '.files'
```

**检查重点**：
- ✅ `dist/` 目录存在
- ✅ `src/` 目录存在
- ✅ `SKILL.md`, `README.md`, `CHANGELOG.md`, `LICENSE`, `skill.yml` 存在
- ❌ `node_modules/` 不应出现在列表中
- ❌ `.env`, `mcporter.json`, `secrets.json` 不应出现在列表中

### 4. 创建 .clawhubignore（如果还没有）

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

### 5. 正式发布

```bash
# 发布 latest tag
clawhub publish . --tag latest

# 同时发布为 v1.0.0 版本
clawhub publish . --tag v1.0.0
```

**预期输出**：
```json
{
  "success": true,
  "skill": "wecom-deep-op",
  "version": "1.0.0",
  "downloads": 0,
  "url": "https://clawhub.com/skills/wecom-deep-op"
}
```

### 6. 验证发布

```bash
# 查看技能信息
clawhub info wecom-deep-op

# 列出所有版本
clawhub versions wecom-deep-op

# 搜索技能
clawhub search wecom
```

访问 `https://clawhub.com/skills/wecom-deep-op` 查看发布的页面。

---

## 发布检查清单

### 发布前

- [ ] 代码已构建（`npm run build`）
- [ ] 安全检查通过（无硬编码密钥）
- [ ] `.clawhubignore` 配置正确
- [ ] `skill.yml` 完整且无敏感信息
- [ ] `package.json` 的 `files` 字段正确
- [ ] `dependencies` 版本范围合理（`>=1.0.13`）
- [ ] README 中所有链接正确
- [ ] CHANGELOG.md 已更新

### 发布后

- [ ] 发布成功，返回 URL
- [ ] Clawhub 页面可访问
- [ ] 技能列表中可见
- [ ] 用户可通过 `clawhub install wecom-deep-op` 安装
- [ ] 安装测试通过

---

## 版本更新流程

每次版本更新：

```bash
# 1. 更新版本号
npm version patch  # 1.0.0 -> 1.0.1 (bug修复)
# 或
npm version minor  # 1.0.0 -> 1.1.0 (新功能)
# 或
npm version major  # 1.0.0 -> 2.0.0 (重大变更)

# 2. 更新 CHANGELOG.md

# 3. 提交
git add .
git commit -m "chore: bump version to 1.0.1"

# 4. 构建
npm run build

# 5. 推送
git push
git push origin v1.0.1

# 6. 创建 GitHub Release
# (在 GitHub 仓库页面创建新的 Release)

# 7. 发布到 Clawhub
clawhub publish . --tag v1.0.1 --tag latest
```

---

## 常见问题

### Q: 发布失败，提示 "skill already exists"

A: 如果同名技能已存在，Clawhub 可能会拒绝覆盖。需要：
1. 检查是否是不同版本（`--tag` 参数指定版本）
2. 或在 Clawhub 管理后台删除旧版本

### Q: 发布后用户无法安装

A: 检查：
1. 发布是否成功（查看 URL）
2. 技能是否在列表中可见（`clawhub search wecom`）
3. 是否有权限（`clawhub info wecom-deep-op`）

### Q: 安装后调用失败，提示 "Unknown MCP server"

A: 用户需要正确配置 `mcporter.json` 或环境变量。检查：
1. 用户是否安装了 `@wecom/wecom-openclaw-plugin`
2. 用户是否配置了对应的 MCP 服务器

---

## 发布后维护

### 监控

- 定期查看 `clawhub info wecom-deep-op` 了解下载量
- 查看仓库的 Issues 和 Pull Requests
- 关注用户反馈

### 更新频率

- 小版本更新：每月1-2次（bug修复、文档改进）
- 大版本更新：每季度1次（新功能）
- 紧急修复：随时发布 patch 版本

### 社区互动

- 回复 Clawhub 上的评论和问题
- 在 GitHub Issues 中回复用户
- 定期更新 README 和 CHANGELOG

---

## 一键发布脚本（可选）

创建 `scripts/publish-to-clawhub.mjs`：

```javascript
#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const skillDir = path.join(__dirname, '../..');

console.log('🚀 Publishing wecom-deep-op to Clawhub...\n');

// 1. 安全检查
console.log('🔒 Security check...');
try {
  execSync('grep -r "uaKey" . --exclude-dir=node_modules --exclude="*.json" || echo "OK"', {
    cwd: skillDir,
    stdio: 'inherit'
  });
} catch (e) {
  console.error('❌ Security check failed!');
  process.exit(1);
}

// 2. Build
console.log('\n🔨 Building...');
try {
  execSync('npm run build', { cwd: skillDir, stdio: 'inherit' });
} catch (e) {
  console.error('❌ Build failed!');
  process.exit(1);
}

// 3. Clawhub dry-run
console.log('\n👀 Clawhub dry-run...');
try {
  execSync('clawhub publish . --dry-run', { cwd: skillDir, stdio: 'inherit' });
} catch (e) {
  console.error('❌ Clawhub dry-run failed!');
  process.exit(1);
}

// 4. Confirm
console.log('\n✅ Ready to publish. Run:');
console.log('   clawhub publish . --tag latest');

module.exports = {};
```

使用：
```bash
node scripts/publish-to-clawhub.mjs
```

---

## 成功标志

发布成功后，你应该能够：

1. ✅ 访问 `https://clawhub.com/skills/wecom-deep-op`
2. ✅ 在 Clawhub 搜索中找到该技能
3. ✅ 用户可以通过 `clawhub install wecom-deep-op` 安装
4. ✅ 安装后调用 `wecom_mcp call wecom-deep-op.ping '{}'` 返回正常

**恭喜！你成功将企业微信集成能力分享给了 OpenClaw 社区！** 🎉

---

## 重要提醒

1. **绝对不要包含任何用户的敏感信息**
2. **所有配置必须由用户自己完成**
3. **定期更新依赖**（官方插件有新版本时及时更新）
4. **保持文档清晰易懂**
5. **响应社区反馈**

---

**发布指南版本**: 1.0.0
**最后更新**: 2026-03-21
