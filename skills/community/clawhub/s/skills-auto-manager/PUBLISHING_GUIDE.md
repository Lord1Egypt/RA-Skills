# Skills Auto Manager - 发布指南

## 📦 发布步骤

### Step 1: 登录 ClawHub

```bash
# 浏览器登录（推荐）
clawhub login

# 或者使用 token
clawhub login --token <your-token>
```

登录后，验证登录状态：
```bash
clawhub whoami
```

### Step 2: 准备发布文件

确保以下文件存在且格式正确：

```
skills-auto-manager/
├── SKILL.md              # 必需 - 主 skill 文件
├── README.md             # 推荐 - 用户文档
├── config.json           # 可选 - 配置文件
├── implementation.md     # 可选 - 实现指南
└── manifest.json         # 自动生成 - 发布元数据
```

### Step 3: 发布到 ClawHub

```bash
cd ~/.openclaw/workspace/skills/skills-auto-manager

# 基本发布
clawhub publish ./ \
  --slug skills-auto-manager \
  --name "Skills Auto Manager" \
  --version 1.0.0 \
  --changelog "Initial release: Auto check, smart filtering, safe install"
```

### Step 4: 验证发布

```bash
# 搜索新发布的 skill
clawhub search skills-auto-manager

# 查看 skill 详情
clawhub inspect skills-auto-manager
```

---

## 📝 发布元数据

### 基本信息

- **Slug**: `skills-auto-manager`
- **Name**: `Skills Auto Manager`
- **Version**: `1.0.0`
- **Category**: `automation`
- **Author**: `OpenClaw Community`
- **License**: `MIT`

### 关键词

```
skills, automation, clawhub, quantitative-trading,
stock-analysis, data-analysis, auto-install,
smart-recommendation
```

---

## 🔄 更新版本

### 次要更新（1.0.1）

```bash
# 更新 SKILL.md 中的版本号
# 添加 changelog

# 发布更新
clawhub publish ./ \
  --slug skills-auto-manager \
  --version 1.0.1 \
  --changelog "Bug fix: Improved error handling"
```

### 主要更新（2.0.0）

```bash
# 更新所有文件
# 更新版本号到 2.0.0
# 添加新的 changelog

# 发布主要更新
clawhub publish ./ \
  --slug skills-auto-manager \
  --version 2.0.0 \
  --changelog "Major update: Added ML-based skill recommendations"
```

---

## ⚠️ 常见问题

### Q1: 登录失败

**问题**: `Error: Not logged in`

**解决方案**:
```bash
# 清除旧的 token
clawhub logout

# 重新登录
clawhub login
```

### Q2: Skill 已存在

**问题**: `Error: Skill already exists`

**解决方案**:
- 如果是你的 skill，使用 `clawhub update` 更新
- 如果不是你的 skill，换个 slug

### Q3: 文件验证失败

**问题**: `Error: Invalid SKILL.md`

**解决方案**:
- 确认 SKILL.md 格式正确
- 确保包含必需的 metadata 部分

### Q4: API 限流

**问题**: `Rate limit exceeded`

**解决方案**:
- 等待重置时间（通常60秒）
- 减少请求频率

---

## 📊 发布检查清单

发布前确认：

- [ ] SKILL.md 格式正确，包含 metadata
- [ ] README.md 文档完整
- [ ] config.json 配置合理
- [ ] implementation.md 实现指南清晰
- [ ] 已登录 ClawHub (`clawhub whoami`)
- [ ] slug 唯一（可用 `clawhub search` 确认）
- [ ] version 号正确（遵循语义化版本）
- [ ] changelog 清晰描述变更

---

## 🚀 发布后

### 测试安装

```bash
# 在另一个环境测试安装
clawhub install skills-auto-manager

# 验证安装
openclaw skills list
```

### 社区推广

- 在 OpenClaw Discord 分享
- 在 GitHub 提交 issue/PR
- 更新文档和示例

### 收集反馈

- 监控用户反馈
- 记录 bug 和 feature requests
- 规划下一版本

---

## 📞 支持

- ClawHub 文档: https://clawhub.ai/docs
- OpenClaw Discord: https://discord.com/invite/clawd
- GitHub Issues: https://github.com/openclaw/clawhub-cli/issues

---

**发布指南 v1.0.0**
**最后更新: 2026-04-21**
