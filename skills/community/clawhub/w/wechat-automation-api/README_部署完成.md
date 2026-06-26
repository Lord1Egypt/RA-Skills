# ✅ 微信自动化 - 部署完成！

## 部署状态

| 项目 | 状态 |
|------|------|
| 项目克隆 | ✅ 完成 |
| Python 环境 | ✅ uv + Python 3.12.12 |
| 依赖安装 | ✅ 31 个包已安装 |
| 配置文件 | ✅ 已生成（含随机 token） |
| 启动脚本 | ✅ 已创建 |

---

## 🔑 重要信息

**Token:** `B3S6GiMbIPW1nX4VrK8JTkuEhoFcON9t`

**API 地址:** `http://127.0.0.1:8808/`

**项目位置:** `C:\Users\admin\.openclaw\workspace\wechat-automation-api`

---

## 🚀 启动服务

### 方法 1：双击启动（推荐）
双击 `启动服务.bat`

### 方法 2：命令行启动
```powershell
cd C:\Users\admin\.openclaw\workspace\wechat-automation-api
.venv\Scripts\python.exe scripts\app.py
```

---

## 📝 使用示例

### 发送文本消息（PowerShell）
```powershell
$body = @{
    token = "B3S6GiMbIPW1nX4VrK8JTkuEhoFcON9t"
    action = "sendtext"
    to = @("文件传输助手")
    content = "你好，这是自动发送的消息"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8808/" -Method Post -Body $body -ContentType "application/json"
```

### 发送图片消息
```powershell
$body = @{
    token = "B3S6GiMbIPW1nX4VrK8JTkuEhoFcON9t"
    action = "sendpic"
    to = @("文件传输助手")
    content = "https://example.com/image.jpg"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8808/" -Method Post -Body $body -ContentType "application/json"
```

### 批量发送（多个联系人）
```powershell
$body = @{
    token = "B3S6GiMbIPW1nX4VrK8JTkuEhoFcON9t"
    action = "sendtext"
    to = @("联系人 1", "联系人 2", "联系人 3")
    content = "这是群发消息"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8808/" -Method Post -Body $body -ContentType "application/json"
```

---

## ⚠️ 注意事项

1. **必须登录微信 Windows 客户端**
2. **微信窗口不能最小化到托盘**（可以最小化到任务栏）
3. **联系人名字必须和微信里显示的完全一致**（区分大小写）
4. **每条消息间隔 1 秒**（避免发送过快）

---

## 🔍 测试连接

启动服务后，访问：
- 服务状态：`http://127.0.0.1:8808/status`
- 健康检查：`http://127.0.0.1:8808/health`

---

## 📋 应用场景（适合你的工作）

### 主播招募 - 自动通知候选人
```powershell
# 给候选人发面试通知
$body = @{
    token = "B3S6GiMbIPW1nX4VrK8JTkuEhoFcON9t"
    action = "sendtext"
    to = @("张三", "李四", "王五")
    content = "您好，我是快手主播招募的运营。看到您对主播职位感兴趣，我们这边是高返点 + 不用做任务的挂靠模式，有兴趣详聊吗？"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8808/" -Method Post -Body $body -ContentType "application/json"
```

---

**部署时间：** 2026-03-12 13:07
**部署人：** 来财 💰
