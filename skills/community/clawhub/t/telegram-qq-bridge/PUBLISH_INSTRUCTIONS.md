# 发布到 ClawHub 指南

## 发布包已就绪 ✅

**发布包位置**: `/home/raolin/.openclaw/skills/telegram-qq-bridge.tar.gz`  
**文件大小**: 40KB  
**版本**: 1.0.0

---

## 手动发布步骤

### 步骤 1: 访问 ClawHub
打开浏览器访问：**https://clawhub.ai/skills/new**

### 步骤 2: 填写技能信息

#### 基本信息
- **技能名称**: `telegram-qq-bridge`
- **版本号**: `1.0.0`
- **描述**: Telegram 群组消息自动转发到 QQ，事件驱动，Node.js 实现
- **分类**: Communication
- **标签**: `telegram`, `qq`, `forward`, `bridge`, `automation`, `nodejs`

#### 作者信息
- **作者**: OpenClaw Community
- **主页**: (可选) https://github.com/openclaw
- **许可证**: MIT

#### 系统要求
- **OpenClaw**: >= 2026.5.2
- **Node.js**: >= 14.0.0

### 步骤 3: 上传文件

点击"选择文件"或拖拽上传：
```
/home/raolin/.openclaw/skills/telegram-qq-bridge.tar.gz
```

### 步骤 4: 填写详细说明

在"详细说明"或"README"栏位填写：

```markdown
# Telegram → QQ 自动转发技能

自动将 Telegram 群组消息转发到 QQ，支持事件驱动、无轮询、Node.js 实现。

## 功能特性
- ✅ 自动监听 Telegram 群组消息
- ✅ 自动转发到 QQ
- ✅ 事件驱动，无轮询
- ✅ Node.js 实现
- ✅ OpenClaw 插件集成
- ✅ 支持配置文件和环境变量

## 快速开始

### 1. 安装
```bash
openclaw skill install telegram-qq-bridge
```

### 2. 配置
```bash
cd ~/.openclaw/skills/telegram-qq-bridge/
cp config.example.json config.json
vim config.json  # 修改 QQ_TARGET 和 QQ_ACCOUNT
```

### 3. 启动
```bash
# 随 OpenClaw 自动启动
openclaw restart

# 或手动启动
cd ~/.openclaw/plugins/telegram-qq-bridge/
node index.js
```

### 4. 测试
```bash
# 在 Telegram 群组发送
@ollama_openclaw_at_dzt_bot 测试

# 检查 QQ 是否收到
# 应收到：[Telegram] 测试
```

## 配置说明

### 配置文件
```json
{
  "qqTarget": "qqbot:c2c:YOUR_OPENID",
  "qqAccount": "your_qq_account",
  "pollInterval": 2000
}
```

### 环境变量
```bash
export QQ_TARGET="qqbot:c2c:YOUR_OPENID"
export QQ_ACCOUNT="your_qq_account"
export POLL_INTERVAL="2000"
```

## 架构

```
Telegram → OpenClaw Channel → telegram-qq-bridge → QQ Bot → 用户 QQ
```

## 故障排查

### 消息未转发
- 确保 Telegram 消息包含 `@ollama_openclaw_at_dzt_bot`
- 检查插件是否运行：`ps aux | grep telegram-qq-bridge`
- 查看日志：`tail -f ~/.openclaw/plugins/telegram-qq-bridge/telegram-qq-bridge.log`

### QQ 未收到
- 确认 `qqTarget` 格式正确：`qqbot:c2c:OPENID`
- 确认 `qqAccount` 正确
- 手动测试发送

## 相关文档
- [完整文档](README.md)
- [快速参考](QUICKSTART.md)
- [发布指南](PUBLISH.md)
- [审核报告](AUDIT_REPORT.md)

## 许可证
MIT License
```

### 步骤 5: 提交审核

1. 确认所有信息填写正确
2. 点击"提交审核"或"发布"按钮
3. 等待审核通过（通常 1-3 个工作日）

---

## 发布后验证

### 1. 检查发布状态
访问技能页面查看是否显示"已发布"

### 2. 测试安装
```bash
# 清除本地版本
rm -rf ~/.openclaw/skills/telegram-qq-bridge/

# 从 ClawHub 重新安装
openclaw skill install telegram-qq-bridge

# 验证安装
ls -la ~/.openclaw/skills/telegram-qq-bridge/
```

### 3. 功能测试
按照 README.md 中的测试步骤验证功能

---

## 常见问题

### Q: 上传失败怎么办？
A: 检查网络连接，确认文件大小不超过限制（通常 100MB）

### Q: 审核被拒绝怎么办？
A: 查看拒绝原因，修改后重新提交

### Q: 如何更新已发布的技能？
A: 在 ClawHub 技能页面点击"更新版本"，上传新版本压缩包

### Q: 如何删除已发布的技能？
A: 在技能页面点击"删除"或联系管理员

---

## 联系支持

如有问题，请：
- 查看文档：https://docs.openclaw.ai
- 提交 Issue: https://github.com/openclaw/telegram-qq-bridge/issues
- 社区讨论：https://discord.gg/clawhub

---

**创建时间**: 2026-05-17  
**版本**: 1.0.0  
**状态**: 准备发布 ✅
