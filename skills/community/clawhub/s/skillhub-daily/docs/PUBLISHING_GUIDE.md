# 🚀 发布指南 / Publishing Guide

> 本文档说明如何将 skillhub-daily v6.2.0 发布到 ClawHub 和 GitHub。

## 📦 已准备好的文件

### 桌面 zip 包（ClawHub 上传用）

```
C:\Users\Administrator\Desktop\skillhub-daily-v6.2.0.zip
```

### GitHub 仓库（待 push）

```
d:\TRAE SOLO CN\project\skillhub-daily-github\
```

完整结构：
```
skillhub-daily-github/
├── .claude-plugin/
│   └── plugin.json            # Claude Code 插件元数据
├── .github/
│   └── workflows/             # （空，预留 CI/CD）
├── .gitignore
├── CHANGELOG.md               # 完整更新日志
├── LICENSE                    # MIT
├── README.md                  # 中英 README
├── RELEASE_NOTES_v6.2.0.md   # Release Notes 详细版
├── SKILL.md                   # 技能主文件
├── data/
│   └── .gitkeep
├── docs/
│   └── CONTRIBUTING.md
├── references/
│   ├── setup-wizard.md
│   ├── platform-adapters.md
│   ├── prompt-templates.md
│   ├── briefing-template.md
│   ├── config.md
│   └── source-contract.md
└── scripts/
    ├── skillhub_daily.py
    └── push_to_ima.py
```

---

## 🎯 ClawHub 发布

### 步骤 1：上传 zip 包

1. 打开 ClawHub 平台
2. 进入"我的技能"或"上传技能"
3. 上传 `C:\Users\Administrator\Desktop\skillhub-daily-v6.2.0.zip`
4. 填写技能元数据：
   - **名称**：skillhub-daily
   - **版本**：6.2.0
   - **分类**：AI 工具 / 效率提升
   - **标签**：skillhub, daily, recommendation, ai, agent
   - **描述**：使用 SKILL.md 中的 description
5. 提交审核

### 步骤 2：填写发布说明

使用 [RELEASE_NOTES_v6.2.0.md](RELEASE_NOTES_v6.2.0.md) 的中文版（核心要点）作为发布说明：

```
🎉 v6.2.0 跨平台融合版发布

✨ 核心新功能：
- 双模式支持：常规 Skills / Cron 定时任务
- 5 大平台适配：qclaw/WorkBuddy/OpenClaw/Hermes/纯脚本
- 推送职责解耦：外部编排负责推送
- 完整中英 README

🔧 改进：
- 描述精简、版本号统一
- 添加 allowed-tools 元数据
- 隐私保护（占位符化所有真实 ID/路径）

🐛 修复：
- argparse 格式化崩溃 bug
- 版本号不一致
- 飞书文档验证步骤

📚 详细说明：见 Release Notes
```

---

## 🎯 GitHub 发布

### 步骤 1：创建 GitHub 仓库

1. 登录 GitHub
2. 创建新仓库：
   - **Repository name**: `skillhub-daily`
   - **Description**: "Daily SkillHub skill discovery - scan Top100 + 7 categories, match user pain points, push to IMA/Lark/Obsidian"
   - **Visibility**: Public
   - **Initialize**: 不勾选（手动 push）

### 步骤 2：初始化本地 Git 并 push

```bash
cd d:\TRAE SOLO CN\project\skillhub-daily-github

git init
git add .
git commit -m "feat: v6.2.0 - cross-platform universal edition

- Add dual mode support (interactive / cron)
- Add 5 platform adapters (qclaw/WorkBuddy/OpenClaw/Hermes/script)
- Add .claude-plugin/plugin.json
- Add bilingual README
- Add CHANGELOG.md
- Add RELEASE_NOTES_v6.2.0.md

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"

git branch -M main
git remote add origin https://github.com/<your-username>/skillhub-daily.git
git push -u origin main
```

### 步骤 3：创建 v6.2.0 Release（GitHub）

#### 方式 A：通过 GitHub 网页

1. 进入 GitHub 仓库页面
2. 点击右侧 **"Create a new release"**
3. 填写：
   - **Choose a tag**: `v6.2.0`
   - **Release title**: `v6.2.0 - 跨平台融合版 / Cross-Platform Universal Edition`
   - **Description**: 复制 [RELEASE_NOTES_v6.2.0.md](RELEASE_NOTES_v6.2.0.md) 内容（去掉最上方"详见"链接）
4. **Attach binaries**：上传 `C:\Users\Administrator\Desktop\skillhub-daily-v6.2.0.zip`
5. 勾选 **"Set as the latest release"**
6. 点击 **"Publish release"**

#### 方式 B：通过 GitHub CLI

```bash
gh release create v6.2.0 \
  --title "v6.2.0 - 跨平台融合版" \
  --notes-file RELEASE_NOTES_v6.2.0.md \
  C:\Users\Administrator\Desktop\skillhub-daily-v6.2.0.zip#skillhub-daily-v6.2.0.zip
```

### 步骤 4：验证发布

检查清单：

- [ ] GitHub 仓库已创建并 push
- [ ] v6.2.0 Release 已发布
- [ ] zip 包已上传到 Release
- [ ] ClawHub 平台已上传
- [ ] Release Notes 显示正确
- [ ] Star History 正常显示

---

## 🔗 双平台互相引流

发布完成后，建议：

1. **ClawHub 描述中添加 GitHub 链接**：
   ```
   GitHub: https://github.com/<your-username>/skillhub-daily
   ```

2. **GitHub README 中添加 ClawHub 链接**：
   ```
   ClawHub: https://clawhub.com/skills/skillhub-daily
   ```

3. **Release Notes 中互相引用**（已包含在 RELEASE_NOTES_v6.2.0.md）

---

## 📊 发布后监控

- 监控 ClawHub 下载量
- 监控 GitHub Stars / Issues / PRs
- 收集用户反馈，准备 v6.3.0

---

## 🆘 常见问题

### Q1: 推送失败？

检查 `git remote -v` 是否正确配置。常见错误是 HTTPS vs SSH 协议。

### Q2: zip 包体积过大？

当前 ~150 KB，正常范围。如果超过 1 MB，请检查是否误将 `data/` 目录打包。

### Q3: GitHub Release 创建失败？

可能是 GitHub 账号未验证邮箱，或 token 权限不足。

### Q4: ClawHub 审核不通过？

常见原因：
- 描述不够详细
- 缺少使用示例
- 触发词不清晰

请对照 [references/setup-wizard.md](references/setup-wizard.md) 检查。

---

**祝发布顺利！** 🎉
