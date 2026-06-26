# 🐙 GitHub 仓库创建指南

## 快速步骤

### 1. 创建仓库

1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `wecom-deep-op`
   - **Description**: `Enterprise WeChat all-in-one OpenClaw skill - unified wrapper for doc, schedule, meeting, todo, contact`
   - **Public** ✅ (推荐，便于社区使用)
   - **不要**初始化 README, .gitignore, LICENSE (本地已有)
3. 点击 `Create repository`

### 2. 本地初始化并推送

```bash
cd /root/.openclaw/workspace/skills/wecom-deep-op

# 初始化 git
git init
git branch -M main

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/wecom-deep-op.git

# 查看文件
git status

# 提交
git add .
git commit -m "feat: initial release - wecom-deep-op v1.0.0

- unified wrapper for all WeCom MCP services
- supports doc, schedule, meeting, todo, contact
- TypeScript implementation with full type definitions
- MIT licensed"

# 推送
git push -u origin main
```

### 3. 创建 Git Tag

```bash
# 创建 v1.0.0 tag
git tag -a v1.0.0 -m "wecom-deep-op v1.0.0 - First stable release"

# 推送 tag
git push origin v1.0.0
```

### 4. 创建 GitHub Release

1. 访问仓库页面 → `Releases` → `Draft a new release`
2. **Tag**: 选择 `v1.0.0`
3. **Title**: `v1.0.0 - Enterprise WeChat All-in-One Skill`
4. **Description**:

```markdown
## 🎉 wecom-deep-op v1.0.0 正式发布

### ✨ 新功能
- 统一封装企业微信文档、日程、会议、待办、通讯录
- 基于官方插件 `@wecom/wecom-openclaw-plugin` v1.0.13
- 完整 TypeScript 类型定义
- 生产环境就绪

### 📦 安装
\`\`\`bash
clawhub install wecom-deep-op
\`\`\`

### 📖 文档
- [Complete README](https://github.com/YOUR_USERNAME/wecom-deep-op/blob/main/README.md)
- [Publishing Guide](https://github.com/YOUR_USERNAME/wecom-deep-op/blob/main/PUBLISHING.md)

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

## 发布检查清单

- [ ] 仓库已创建并推送
- [ ] v1.0.0 tag 已创建并推送
- [ ] GitHub Release 已发布
- [ ] Release 描述包含完整信息
- [ ] 所有示例中的 `YOUR_USERNAME` 已替换为实际用户名
- [ ] README 中链接正确

---

## 后续更新流程

每次版本更新：

1. 修改代码，更新 `CHANGELOG.md` 和 `package.json`
2. 提交：`git commit -m "feat: new feature"`
3. 构建：`npm run build`
4. 打 tag：`git tag -a v1.1.0 -m "v1.1.0"`
5. 推送：`git push && git push origin v1.1.0`
6. 创建新的 GitHub Release
7. 发布到 Clawhub：`clawhub publish . --tag v1.1.0`

---

## 仓库结构

```
wecom-deep-op/
├── src/                    # 源代码
├── dist/                   # 构建输出（自动生成）
├── examples/               # 使用示例
├── test/                   # 测试文件
├── SKILL.md                # 技能说明（OpenClaw 专用）
├── README.md               # 详细使用文档（对外）
├── CHANGELOG.md            # 版本历史
├── LICENSE                 # MIT License
├── skill.yml               # Clawhub 元数据
├── PUBLISHING.md           # 发布指南
├── package.json
├── tsconfig.json
└── rollup.config.js
```

---

## 注意事项

1. **不要提交敏感信息**：`.env`, `mcporter.json`, `secrets.json` 已在 `.gitignore` 中
2. **版本号管理**：遵循语义化版本（SemVer）
3. **README 链接**：发布前替换 `YOUR_USERNAME` 为实际 GitHub 用户名
4. **安全声明**：在 README 中明确说明配置必须由用户自己完成
