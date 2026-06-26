# 🚀 发布 windows-tts 到 ClawHub - 完整指南

## 📦 已准备的发布文件

你的 skill 现在包含以下 ClawHub 发布所需的文件：

```
/home/cmos/skills/windows-tts/
├── 📄 SKILL.md                    ✅ 主文档（含 ClawHub frontmatter）
├── 📄 package.json                ✅ NPM 包元数据
├── 📄 tsconfig.json               ✅ TypeScript 配置
├── 📄 openclaw.plugin.json        ✅ OpenClaw 插件清单
├── 📄 _meta.json                  ✅ ClawHub 元数据
├── 📁 .clawhub/
│   └── origin.json                ✅ 注册表配置
├── 📄 CHANGELOG.md                ✅ 版本历史
├── 📄 README.md                   ✅ 使用示例
├── 📄 INSTALL.md                  ✅ 安装指南
├── 📄 PUBLISH.md                  ✅ 发布文档
├── 📄 IMPLEMENTATION_SUMMARY.md   ✅ 实现总结
├── 📁 dist/                       ✅ 编译输出
│   ├── index.js
│   ├── client.js
│   ├── tools.js
│   ├── types.js
│   ├── config.js
│   └── guards.js
├── 📁 src/
│   ├── index.ts
│   ├── client.ts
│   ├── tools.ts
│   ├── types.ts
│   ├── config.ts
│   └── guards.ts
└── 📁 node_modules/               ✅ 依赖
```

## ✅ 发布前检查清单

### 文件完整性
- [x] `SKILL.md` - 包含完整的 frontmatter 和徽章
- [x] `package.json` - 包含版本、描述、脚本
- [x] `dist/` - 已编译的 JavaScript 文件
- [x] `_meta.json` - ClawHub 元数据
- [x] `.clawhub/origin.json` - 注册表配置
- [x] `CHANGELOG.md` - 版本变更记录
- [x] `openclaw.plugin.json` - OpenClaw 插件配置

### 代码质量
- [x] TypeScript 编译成功
- [x] 类型定义完整（.d.ts 文件）
- [x] 无运行时错误
- [x] 功能测试通过

### 文档完整性
- [x] 使用示例清晰
- [x] 配置说明完整
- [x] 故障排查指南
- [x] 安装指南详细

## 🎯 发布步骤

### 第 1 步：登录 ClawHub

```bash
# 方式 A：浏览器登录（推荐）
clawhub login

# 方式 B：使用 API Token
clawhub login --token YOUR_API_TOKEN --label "windows-tts-publish"
```

**获取 Token 方法**：
1. 访问 https://clawhub.ai
2. 登录你的账号
3. 进入 Settings → API Tokens
4. 创建新 Token，复制保存

### 第 2 步：验证登录状态

```bash
clawhub whoami
```

预期输出：
```
✓ Authenticated as: your-handle
  User ID: kn74589cx1nbhnc3x0f3nwre39814699
```

### 第 3 步：查看技能文件

```bash
cd /home/cmos/skills/windows-tts
ls -la
```

确认包含：
- `SKILL.md`（必需）
- `package.json`（必需）
- `dist/` 目录（必需）
- `index.ts` 或其他入口文件

### 第 4 步：发布技能

```bash
# 方式 A：使用默认配置（推荐）
cd /home/cmos/skills
clawhub publish windows-tts

# 方式 B：指定所有参数
clawhub publish /home/cmos/skills/windows-tts \
  --slug windows-tts \
  --name "Windows TTS Notification" \
  --version 1.0.0 \
  --tags "latest,tts,notification,windows,azure,broadcast,reminder" \
  --changelog "Initial release: Cross-device TTS broadcast for family reminders"
```

### 第 5 步：验证发布

```bash
# 搜索你的技能
clawhub search windows-tts

# 查看技能详情
clawhub inspect windows-tts
```

### 第 6 步：测试安装

```bash
# 在测试环境安装
clawhub install windows-tts

# 验证安装
clawhub list
```

## 🔧 常见问题处理

### ❌ 错误：Slug 已被占用

```bash
# 使用不同的 slug
clawhub publish windows-tts \
  --slug windows-tts-broadcast \
  --name "Windows TTS Broadcast"
```

### ❌ 错误：缺少必需文件

确保以下文件存在：
```bash
ls SKILL.md package.json dist/
```

如果缺少 `dist/`，重新编译：
```bash
npm run build
```

### ❌ 错误：认证失败

```bash
# 重新登录
clawhub logout
clawhub login
```

### ❌ 错误：版本已存在

如果发布过相同版本：
```bash
# 1. 更新版本号（在 package.json 和 _meta.json 中）
# 2. 更新 CHANGELOG.md
# 3. 重新发布
clawhub publish windows-tts --version 1.0.1
```

## 📊 发布后的工作

### 1. 分享你的技能

**在社区宣传**：
- OpenClaw Discord/Telegram
- GitHub Discussions
- 社交媒体（Twitter/X, LinkedIn）
- 技术博客

**分享模板**：
```
🎉 新技能发布！

Windows TTS Notification - 跨设备语音播报系统

✅ 家庭提醒（作业、吃药、吃饭）
✅ 支持 Azure TTS 所有音色
✅ 局域网广播，零延迟
✅ 简单易用，配置灵活

立即安装：clawhub install windows-tts

#OpenClaw #AI #TTS #HomeAutomation
```

### 2. 监控使用情况

```bash
# 查看安装统计（如果 ClawHub 支持）
clawhub stats windows-tts

# 查看用户反馈
# 关注 ClawHub 上的评论和评分
```

### 3. 收集反馈

- 回复用户问题
- 记录功能建议
- 修复报告的 bug
- 规划下一版本

## 📝 版本更新流程

### 发布新版本

```bash
# 1. 更新版本号
# package.json: "version": "1.0.1"
# _meta.json: "version": "1.0.1"

# 2. 更新 CHANGELOG.md
cat >> CHANGELOG.md << 'EOF'

## [1.0.1] - 2026-03-16

### Fixed
- 修复了网络超时问题
- 改进了错误提示

### Changed
- 默认音量调整为 0.8
EOF

# 3. 重新编译
npm run build

# 4. 发布
clawhub publish windows-tts \
  --version 1.0.1 \
  --changelog "Fixed network timeout, improved error messages"
```

## 🏆 发布清单

### 必需项
- ✅ `SKILL.md` - 完整的前端元数据
- ✅ `package.json` - 版本、描述、脚本
- ✅ `dist/` - 编译后的代码
- ✅ 入口文件（`index.ts` 或 `index.js`）
- ✅ ClawHub 账户

### 推荐项
- ✅ `CHANGELOG.md` - 版本历史
- ✅ `README.md` - 使用示例
- ✅ `INSTALL.md` - 安装指南
- ✅ `.clawhub/origin.json` - 注册表配置
- ✅ 徽章和 Shields.io 标识

### 可选项
- 📄 `PUBLISH.md` - 发布文档
- 📄 `IMPLEMENTATION_SUMMARY.md` - 实现总结
- 📄 `CONTRIBUTING.md` - 贡献指南
- 📄 `LICENSE` - 许可证
- 📄 `.github/` - GitHub 相关文件

## 🎊 恭喜发布！

发布成功后，你的技能将会：
- ✅ 在 ClawHub 注册表可见
- ✅ 全球用户可以搜索和安装
- ✅ 自动版本管理
- ✅ 统计和反馈追踪

**技能页面**：`https://clawhub.ai/skills/windows-tts`

**安装命令**：`clawhub install windows-tts`

---

## 📞 需要帮助？

- ClawHub 文档：https://clawhub.ai/docs
- 社区支持：OpenClaw Discord
- 问题反馈：GitHub Issues

**祝你发布成功！** 🚀
