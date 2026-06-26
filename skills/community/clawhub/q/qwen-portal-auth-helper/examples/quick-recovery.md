# 快速恢复指南

> **当 qwen-portal 新闻任务失败时的5分钟修复流程**

## 🚨 问题症状

你的新闻收集任务开始失败，错误信息类似：
```
Qwen OAuth refresh token expired or invalid. 
Re-authenticate with `openclaw models auth login --provider qwen-portal`.
```

或者任务状态显示：
- 状态: `error`
- 连续错误: `5` (且不断增加)
- 最后执行: `10小时前`

## 🚀 5分钟修复流程

### **步骤1: 确认问题**
```bash
# 查看哪些任务失败了
openclaw cron list | grep -i "error\|qwen-portal"

# 示例输出:
# 71628635-03e3-414b-865b-e427af4e804f BlockBeats 新闻总结 ... error ... qwen-portal/coder...
# 9f557448-389b-4732-8da1-e0caafbc3a27 财经慢报 新闻总结 ... error ... qwen-portal/coder...
```

### **步骤2: 获取 OAuth 链接**
```bash
# 运行我们的自动化脚本
cd ~/.openclaw/skills/qwen-portal-auth-helper
./scripts/get-qwen-oauth-link.sh

# 你会看到:
# 🔗 OAuth 链接: https://chat.qwen.ai/authorize?user_code=M17WU0SC&client=qwen-code
# 📱 Device Code: M17WU0SC
```

### **步骤3: 完成浏览器授权**
1. **点击上面的链接** (在新的浏览器标签页中)
2. **登录** 你的 qwen 账户
3. **授权** 应用访问权限
4. **等待** 页面显示授权成功

**注意**: 整个过程中 CLI 窗口可以保持打开，它会自动检测授权完成。

### **步骤4: 验证修复**
```bash
# 测试一个任务
openclaw cron run 71628635-03e3-414b-865b-e427af4e804f

# 检查结果
openclaw cron runs --id 71628635-03e3-414b-865b-e427af4e804f | grep -i "status\|error\|token"

# 应该看到:
# "status": "ok"
# 有 token 使用量统计 (input_tokens, output_tokens)
```

### **步骤5: 重置任务状态 (如果需要)**
```bash
# 如果任务状态还是 error，重置它
./scripts/reset-task-state.py 71628635-03e3-414b-865b-e427af4e804f

# 对每个失败的任务执行
./scripts/reset-task-state.py 9f557448-389b-4732-8da1-e0caafbc3a27
```

## ✅ 成功验证

修复完成后，检查：
```bash
# 所有任务状态正常
openclaw cron list | grep qwen-portal
# 应该显示: status: ok, consecutiveErrors: 0

# Telegram 收到新闻消息
# 检查你的 Telegram，应该收到最新的新闻摘要
```

## 🔧 故障排除

### **问题1: 脚本找不到 tmux**
```bash
# 安装 tmux
brew install tmux  # macOS
# 或
sudo apt install tmux  # Ubuntu/Debian
```

### **问题2: OAuth 链接无效**
- 链接有效期为 **15-30分钟**，如果超时需要重新获取
- 确保在**同一个浏览器会话**中完成
- 如果仍然失败，qwen 账户可能有问题

### **问题3: 授权后任务还是失败**
```bash
# 1. 等待几分钟让凭证同步
sleep 60

# 2. 再次测试
openclaw cron run <task-id>

# 3. 检查详细错误
openclaw cron runs --id <task-id> | tail -20
```

### **问题4: 多个任务需要修复**
```bash
# 批量检查所有 qwen-portal 任务
./scripts/check-qwen-auth.sh

# 报告会显示所有需要关注的任务
# 按照报告建议逐个修复
```

## 📅 预防措施

### **设置每周自动检查**
```bash
# 添加到 crontab (每周一上午9点)
echo "0 9 * * 1 ~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh >> ~/.openclaw/logs/qwen-check.log 2>&1" | crontab -

# 验证添加成功
crontab -l | grep check-qwen-auth
```

### **预期维护频率**
- **qwen-portal OAuth**: 每 **1-2周** 过期一次
- **建议检查**: 每周一次 (周一上午)
- **修复时间**: 5-10分钟 (熟悉后)

## 🎯 最佳实践

### **记录你的任务ID**
创建 `~/.openclaw/my-qwen-tasks.txt`:
```
# 我的 qwen-portal 任务
71628635-03e3-414b-865b-e427af4e804f : BlockBeats 新闻总结
9f557448-389b-4732-8da1-e0caafbc3a27 : 财经慢报 新闻总结
```

### **创建一键修复脚本**
```bash
#!/bin/bash
# fix-all-qwen-tasks.sh
echo "修复所有 qwen-portal 任务..."
./scripts/get-qwen-oauth-link.sh
echo "请完成浏览器授权，然后按 Enter 继续..."
read
./scripts/reset-task-state.py 71628635-03e3-414b-865b-e427af4e804f
./scripts/reset-task-state.py 9f557448-389b-4732-8da1-e0caafbc3a27
echo "✅ 所有任务修复完成"
```

## 📞 获取帮助

如果按照这个指南还是无法修复：

1. **检查日志**: `cat /tmp/qwen-auth-check-*.log`
2. **查看报告**: `cat /tmp/qwen-auth-report-*.md`
3. **社区支持**: 在 OpenClaw Discord 或 GitHub 提问
4. **提供信息**: 错误信息、脚本输出、OpenClaw 版本

---

**记住**: qwen-portal 免费但有维护成本。  
**解决方案**: 每周检查 + 这个技能 = 无忧使用。

*基于 2026-03-09 实战经验 - 解决过同样问题*