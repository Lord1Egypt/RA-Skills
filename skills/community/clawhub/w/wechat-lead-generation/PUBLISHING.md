# Publishing Guide

本文档说明如何将 `wechat-lead-generation` 技能发布到 GitHub 和 ClawHub。

## 📦 Release 准备

### 1. 本地检查

```bash
cd ~/.openclaw/workspace/.agents/skills/wechat-lead-generation

# 验证所有文件存在
ls -la SKILL.md README.md LICENSE Requirements.md CHANGELOG.md CONTRIBUTING.md .gitignore bin/ engine.py

# 本地测试运行
bin/run --source groups --days_back 1 --keywords "AI" --auto_reply false

# 检查输出
ls -la output/wechat-lead-generation/
```

### 2. 更新版本号

编辑 `SKILL.md` 的 frontmatter：
```yaml
version: 0.1.0  # → 0.2.0 或其他
```

同时更新 `CHANGELOG.md`（为新版本添加条目）。

### 3. 提交到 Git

```bash
cd ~/.openclaw/workspace/.agents/skills/wechat-lead-generation

git init
git add .
git commit -m "chore: prepare v0.1.0 release"
```

## 🚀 GitHub 发布

### 创建远程仓库

1. 登录 GitHub
2. 点击 New repository
3. 仓库名：`wechat-lead-generation-skill`
4. 选择 Public（开源）或 Private
5. **不要** 初始化 README、.gitignore、LICENSE（已有本地）
6. 创建仓库

### 关联并推送

```bash
# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/wechat-lead-generation-skill.git
git branch -M main
git push -u origin main
```

### 创建 Release

```bash
# 打 tag
git tag -a v0.1.0 -m "WeChat Lead Generation Skill v0.1.0"
git push origin v0.1.0
```

然后在 GitHub 页面上：
- 进入 Releases → Draft a new release
- Choose a tag: `v0.1.0`
- Title: `WeChat Lead Generation Skill v0.1.0`
- Description: 复制 CHANGELOG.md 中 `[0.1.0]` 内容
- Publish release

✅ GitHub 发布完成！用户可以通过：
```bash
git clone https://github.com/YOUR_USERNAME/wechat-lead-generation-skill.git \
  ~/.openclaw/workspace/.agents/skills/wechat-lead-generation
```

---

## 🏛️ ClawHub 上架

### 提交 PR

1. Fork https://github.com/openclaw/skills
2. 将本技能复制到 `skills/wechat-lead-generation/` 目录
3. 提交 PR 并填写：
   - 技能名称：`wechat-lead-generation`
   - 核心功能：微信线索抓取与分析
   - 依赖：`agentmemory`、`wechat-md-publish`（可选）
   - 测试情况：✅ 通过（模拟数据）
   - 合规说明：默认半自动模式，提醒风险
4. 等待审核（通常 1-3 天）

审核要点：
- ✅ 结构符合 OpenClaw Skill Standard
- ✅ 文档完整（README + SKILL.md）
- ✅ 许可证清晰（MIT）
- ✅ 风险提示充分
- ✅ 依赖声明明确

---

## 📢 宣传建议

- 在 OpenClaw Discord 社区宣布发布
- 提交到 awesome-openclaw 列表
- 撰写使用案例（如：销售自动化）
- 添加 GitHub Topics: `openclaw`, `wechat`, `lead-generation`, `marketing-automation`

---

**祝发布顺利！** 🎉

如有问题，请在仓库 Issues 中提问。
