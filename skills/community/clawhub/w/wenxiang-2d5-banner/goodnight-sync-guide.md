# 晚安同步配置指南

**配置时间**: 2026-03-05 23:00  
** Cron Job ID**: `9d1b9ac7-19f3-458d-bb91-aa89b52b700e`

---

## 🌙 功能说明

每天 23:00 自动触发晚安同步流程：

1. **提醒晚安** - 系统发送晚安提醒
2. **自动同步** - 运行同步脚本备份记忆到 OneDrive
3. **生成报告** - 创建同步报告文件

---

## 📋 配置详情

### Cron 任务
- **名称**: 晚安记忆同步
- **时间**: 每天 23:00 (Asia/Shanghai)
- **Cron 表达式**: `0 23 * * *`
- **会话**: main session
- **状态**: ✅ 已启用

### 同步脚本
- **文件**: `sync-goodnight.ps1`
- **位置**: `C:\Users\Xiabi\.openclaw\workspace\`
- **功能**: 同步 memory/ 文件夹到 OneDrive

### OneDrive 目标
- **路径**: `E:\OneDrive\OpenClaw-Workspace`
- **同步内容**: 
  - memory/*.md (所有每日记忆)
  - MEMORY.md (长期记忆)
  - USER.md (用户信息)
  - TOOLS.md (工具配置)

---

## 🎯 使用方式

### 自动模式（推荐）
每天 23:00 自动运行，无需手动操作。

### 手动模式
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\Xiabi\.openclaw\workspace\sync-goodnight.ps1
```

---

## 📊 同步报告

每次同步会生成报告文件：
```
E:\OneDrive\OpenClaw-Workspace\last-sync-YYYY-MM-DD.txt
```

报告内容：
- 同步时间
- 同步文件列表
- 文件数量统计
- 同步状态

---

## 🔧 修改时间

如果想修改同步时间（比如 22:30）：

1. **查看当前任务**
```bash
openclaw cron list
```

2. **更新 Cron 表达式**
```bash
openclaw cron update --id <job-id> --schedule "30 22 * * *"
```

3. **验证**
```bash
openclaw cron list
```

---

## ⚠️ 注意事项

### 1. OneDrive 状态
- 确保 OneDrive 客户端正常运行
- 检查任务栏云朵图标是否有错误
- 同步完成后文件应有小绿勾 ✅

### 2. 网络要求
- 需要联网才能同步到 OneDrive
- 离线时会缓存，联网后自动同步
- 可能产生冲突副本（需手动合并）

### 3. 时间选择
- 默认 23:00，根据你的作息时间调整
- 建议在你通常说"晚安"的时间
- 避免太早（可能还有工作）或太晚（已经睡了）

---

## 💡 高级用法

### 添加个性化晚安消息

编辑 cron job 的 payload text：
```json
{
  "payload": {
    "kind": "systemEvent",
    "text": "🌙 Thomas 先生，晚安！今天辛苦了！\n\n正在同步记忆到 OneDrive...\n\n💤 早点休息，明天继续加油！\n\n运行：powershell -ExecutionPolicy Bypass -File sync-goodnight.ps1"
  }
}
```

### 同步后发送邮件（可选）

在脚本末尾添加邮件发送逻辑（需要配置 SMTP）。

### 同步前检查

在脚本开头添加检查逻辑：
```powershell
# 检查 OneDrive 是否运行
$onedrive = Get-Process OneDrive -ErrorAction SilentlyContinue
if (-not $onedrive) {
    Write-Host "OneDrive 未运行，正在启动..."
    Start-Process "$env:LOCALAPPDATA\Microsoft\OneDrive\OneDrive.exe"
    Start-Sleep -Seconds 3
}
```

---

## 📝 验证同步

### 方法 1：检查报告文件
```powershell
Get-ChildItem "E:\OneDrive\OpenClaw-Workspace\last-sync-*.txt" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1 | 
    Get-Content
```

### 方法 2：查看 OneDrive 文件夹
1. 打开文件资源管理器
2. 导航到：`E:\OneDrive\OpenClaw-Workspace`
3. 检查文件是否有小绿勾 ✅

### 方法 3：查看 Cron 历史
```bash
openclaw cron runs --id <job-id>
```

---

## 🎉 配置完成！

现在每天 23:00，系统会自动：
1. ✅ 提醒你该说晚安了
2. ✅ 自动同步记忆到 OneDrive
3. ✅ 生成同步报告

**Thomas 先生，今晚就可以体验了！** 🌙

---

**最后更新**: 2026-03-05  
**版本**: 1.0
