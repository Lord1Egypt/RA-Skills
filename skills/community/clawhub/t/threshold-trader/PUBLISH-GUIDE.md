# 📦 发布指南

## ✅ 已完成

1. ✅ 创建了完整的技能文件结构
2. ✅ 创建了发布脚本 `publish.sh`
3. ✅ 登录了 ClawHub 账户 (@sky-bin_bvox)

## ⚠️ 当前问题

ClawHub 发布时遇到 GitHub API 速率限制：
```
Error: GitHub account lookup failed (remaining: 179/180, reset in XXs)
```

## 🔧 解决方案

### 方案 1：稍后重试（推荐）

等待 5-10 分钟后，直接运行：

```bash
cd /Users/sky/Documents/Simmer-Skill/threshold-trader
npx clawhub@latest publish . --slug threshold-trader --version 1.0.0
```

### 方案 2：使用发布脚本

```bash
cd /Users/sky/Documents/Simmer-Skill/threshold-trader
./publish.sh
```

### 方案 3：检查 ClawHub 服务状态

如果问题持续，可能是 ClawHub 服务端问题：
- 查看 https://clawhub.ai 是否有服务通知
- 访问 ClawHub Discord/Telegram 了解是否有已知问题

### 方案 4：手动排查

```bash
# 检查登录状态
npx clawhub@latest whoami

# 尝试简单的 bump 发布
npx clawhub@latest publish . --slug threshold-trader --bump patch

# 查看已发布的技能
npx clawhub@latest list
```

## 📋 发布检查清单

当成功发布后，验证以下内容：

- [ ] 技能出现在 ClawHub: `npx clawhub@latest search threshold`
- [ ] 可以安装: `npx clawhub@latest install threshold-trader`
- [ ] 文件完整：SKILL.md, clawhub.json, threshold_trader.py
- [ ] 6 小时后出现在 Simmer 注册表: https://simmer.markets/skills

## 🔍 故障排除

### GitHub API 限制

如果确实是 GitHub API 问题：
- **原因**：ClawHub 在发布时需要验证 GitHub 账户
- **解决**：等待 15-60 分钟后重试
- **避免**：不要多次快速重试（会加重限制）

### "Not logged in" 错误

```bash
npx clawhub@latest login
```

### "Skill already exists" 错误

如果技能已存在，使用版本递增：

```bash
npx clawhub@latest publish . --slug threshold-trader --bump patch
```

## 📱 联系支持

如果问题持续超过 1 小时：

- ClawHub: https://clawhub.ai
- Simmer: simmer@agentmail.to
- Telegram: https://t.me/+m7sN0OLM_780M2Fl

## 🎯 发布成功后

1. **验证安装**：
   ```bash
   npx clawhub@latest install threshold-trader
   ```

2. **测试运行**：
   ```bash
   export SIMMER_API_KEY="your-key"
   python threshold_trader.py
   ```

3. **等待 Simmer 同步**：
   - 6 小时内自动出现在 https://simmer.markets/skills
   - 无需人工审批

4. **分享你的技能**：
   ```
   安装命令: npx clawhub@latest install threshold-trader
   文档: https://clawhub.ai/skills/threshold-trader
   ```

---

## 📌 快速参考

```bash
# 发布新版本
npx clawhub@latest publish . --slug threshold-trader --version 1.0.0

# 自动递增版本
npx clawhub@latest publish . --slug threshold-trader --bump patch

# 检查状态
npx clawhub@latest whoami

# 搜索技能
npx clawhub@latest search threshold

# 安装测试
npx clawhub@latest install threshold-trader
```

---

**当 GitHub API 问题解决后，直接运行上述任何发布命令即可！** 🚀
