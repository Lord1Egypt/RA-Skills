# 快速安装指南

## 3 分钟快速开始

### 1️⃣ 复制 Skill

```bash
# Windows PowerShell
Copy-Item -Recurse "D:\openclaw_self_skill\usage-monitor" "$env:USERPROFILE\.openclaw\workspace\skills\"
```

### 2️⃣ 配置参数

```bash
cd skills/usage-monitor
copy config.example.json config.json
notepad config.json
```

**必须填写的配置：**

```json
{
  "panelUrl": "从这里粘贴你的用量面板 URL",
  "alertThreshold": 80
}
```

### 3️⃣ 获取你的 URL

1. 打开浏览器，访问你的用量/配额面板页面（如：OpenClaw Token 数量面板）
2. **复制浏览器地址栏的完整 URL**
3. 粘贴到 `config.json` 的 `panelUrl` 字段

### 4️⃣ 测试运行

```bash
node check.js
```

看到 `✅ 配置加载成功！` 即表示配置正确。

### 5️⃣ 启用自动监控

编辑工作区的 `HEARTBEAT.md`，添加：

```markdown
- [ ] 检查服务用量
```

## 配置示例

### 示例 1：基础配置（80% 告警）

```json
{
  "panelUrl": "https://platform.example.com/token/quota",
  "alertThreshold": 80
}
```

### 示例 2：保守配置（50% 告警）

```json
{
  "panelUrl": "https://platform.example.com/token/quota",
  "alertThreshold": 50,
  "serviceName": "OpenClaw Token",
  "remainingDays": 30
}
```

### 示例 3：宽松配置（90% 告警）

```json
{
  "panelUrl": "https://console.cloud.com/usage/dashboard",
  "alertThreshold": 90,
  "checkIntervalHours": 6
}
```

## 常见问题

### Q: URL 从哪里复制？

**A:** 从浏览器地址栏复制！打开你的用量/配额面板页面，地址栏显示的就是你的专属 URL。

### Q: 阈值设置多少合适？

**A:** 
- 保守型：50-70%（提前预警）
- 标准型：80%（推荐）
- 宽松型：90-95%（接近用完再提醒）

### Q: 如何修改配置？

**A:** 直接编辑 `config.json`，保存后下次运行自动生效。

### Q: 可以监控多个用量页面吗？

**A:** 当前版本支持单个 URL。如需监控多个，可复制多份配置并分别运行。

## 下一步

配置完成后，参考 `README.md` 了解详细使用方法。

---

**需要帮助？** 查看 `README.md` 或 `SKILL.md`
