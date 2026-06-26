# GitHub 发布流程

---

## 1️⃣ 创建 GitHub 仓库

```bash
# 登录 GitHub（如果未登录）
gh auth login

# 创建公开仓库
gh repo create obsidian-brain-pro --public --description "拒绝 AI 爹味！这款 Obsidian 插件只记你的原话，不装逼。"

# 或创建私有仓库（测试阶段）
gh repo create obsidian-brain-pro --private --description "WhatsApp → Obsidian 智能记忆增强"
```

---

## 2️⃣ 初始化 Git 并推送

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/obsidian-brain-pro

# 初始化 Git
git init

# 添加所有文件
git add -A

# 首次提交
git commit -m "🎉 v1.1.0 初始发布

核心功能：
- 闪电入库（保持原味）
- 多语言纠偏白名单
- 隐私脱敏红线
- Ollama 语义检索

调教者：电力系统专家 & 2026 北影考研党实战调教"

# 关联远程仓库
git remote add origin https://github.com/openclaw/obsidian-brain-pro.git

# 推送到 GitHub
git push -u origin main
```

---

## 3️⃣ 创建 Release

```bash
# 创建 v1.1.0 Release
gh release create v1.1.0 \
  --title "v1.1.0 - 多语言纠偏 + 隐私脱敏加固版" \
  --notes "## ✨ 新增功能

### 🎤 多语言纠偏白名单
- Open Crow → OpenClaw
- 导课 → Docker
- 码云 → Git

### 🔒 隐私脱敏红线
- API Key → [API_KEY_PROTECTED]
- 密码 → [PASSWORD_PROTECTED]

## 📦 安装方式

\`\`\`bash
openclaw skill install obsidian-brain-pro
\`\`\`

## 🎯 核心一句话

> 用户说的每一句话都是证据，你只能整理格式，不能篡改证据。" \
  obsidian-brain-pro-v1.1.0.tar.gz
```

---

## 4️⃣ 添加 Topics（标签）

```bash
# 添加 Topics（帮助用户发现）
gh repo edit --add-topic obsidian
gh repo edit --add-topic openclaw
gh repo edit --add-topic whatsapp
gh repo edit --add-topic ollama
gh repo edit --add-topic semantic-search
gh repo edit --add-topic privacy-first
gh repo edit --add-topic voice-to-text
```

---

## 5️⃣ 启用 GitHub Pages（可选）

```bash
# 启用 GitHub Pages（展示 SKILL.md）
gh api repos/openclaw/obsidian-brain-pro/pages -X POST -f source '{"branch":"main","path":"/"}'
```

---

## 📋 发布后检查清单

| 检查项 | 状态 |
|--------|------|
| GitHub 仓库创建 | ⏳ 待执行 |
| 首次推送成功 | ⏳ 待执行 |
| Release 创建 | ⏳ 待执行 |
| Topics 添加 | ⏳ 待执行 |
| ClawHub 提交 | ⏳ 待执行 |

---

## 🔗 GitHub 链接

https://github.com/openclaw/obsidian-brain-pro

---

## 📝 注意事项

1. **README.md 人设文案**：已添加"电力系统专家 & 2026 北影考研党实战调教"
2. **SKILL.md 封面**：使用"正确 vs 错误对照图"作为防幻觉示例
3. **prompts/organizer.txt**：v2.1 加固版（多语言纠偏 + 隐私脱敏）
4. **scripts/sync.sh**：Git 只增不减推送脚本

---

*准备时间：2026-03-28 22:16*
*作者：小弟 🤓*