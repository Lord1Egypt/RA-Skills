# ATOM-DELIVERY-013 - 本地播放语音

> 版本：**V2.0**  
> 状态：✅ 已固化  
> 最后更新：**2026-03-07 15:18**

---

## 📋 动作定义

**名称：** 本地播放语音  
**分类：** 交付层（Delivery Layer）  
**编号：** ATOM-DELIVERY-013

**一句话描述：** 本地播放最新生成的 TTS 语音文件

---

## 🎯 输入输出

### 输入
- **类型：** 无（自动查找最新）
- **查找路径：** `C:\Users\Xiabi\.openclaw\workspace\tts\voice-*.mp3`
- **规则：** 按 LastWriteTime 降序取第一个
- **命名：** `voice-时间戳.mp3`（时间戳精确到毫秒）

### 输出
- **类型：** 系统播放（无返回值）
- **效果：** 系统默认播放器播放 MP3

---

## ⚙️ 偏好设置

### 查找规则
- **路径模式：** `workspace/tts/voice-*.mp3`
- **完整路径：** `C:\Users\Xiabi\.openclaw\workspace\tts\voice-*.mp3`
- **排序：** LastWriteTime 降序
- **选择：** 第一个（最新）

### 播放方式
- **命令：** Start-Process
- **播放器：** 系统默认（Windows Media Player/其他）
- **模式：** 后台播放（不阻塞）

### 自动执行
- **触发：** 飞书发送语音后自动执行
- **用户操作：** 0 步（全自动）
- **延迟：** 无（立即播放）

### 锁屏检测 🆕（2026-03-07 14:10）
- **检测方式：** 检测 LockApp 进程
- **锁屏时：** ❌ 跳过播放（不浪费）
- **活跃时：** ✅ 自动播放
- **日志：** 记录到 `Temp\voice-playback-log.txt`
- **用户偏好：** 锁屏时不播放，活跃时 0 步自动播放

---

## 📝 操作步骤

```powershell
# 1. 查找最新 MP3 文件（workspace/tts 文件夹）
$ttsFolder = "C:\Users\Xiabi\.openclaw\workspace\tts"
$latestVoice = Get-ChildItem -Path $ttsFolder -Filter "voice-*.mp3" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1

# 2. 检查文件存在
if (-not $latestVoice) {
    Write-Host "⚠️  未找到语音文件" -ForegroundColor Yellow
    return
}

Write-Host "📁 找到最新语音：$($latestVoice.Name)" -ForegroundColor Cyan
Write-Host "  路径：$($latestVoice.FullName)" -ForegroundColor Gray
Write-Host "  大小：$($latestVoice.Length) 字节" -ForegroundColor Gray

# 3. 检测锁屏状态 🆕
$lockProcess = Get-Process "LockApp" -ErrorAction SilentlyContinue
if ($lockProcess) {
    Write-Host "🔒 屏幕已锁定，跳过播放" -ForegroundColor Yellow
    # 记录日志
    Add-Content -Path "$env:TEMP\voice-playback-log.txt" -Value "$(Get-Date) - 跳过播放（屏幕锁定）"
    return
}

Write-Host "✅ 屏幕活跃，准备播放..." -ForegroundColor Green

# 4. 播放
Write-Host "▶️  播放语音：$($latestVoice.Name)" -ForegroundColor Cyan
Start-Process $latestVoice.FullName
Write-Host "✅ 语音正在播放..." -ForegroundColor Green

# 记录日志
Add-Content -Path "$env:TEMP\voice-playback-log.txt" -Value "$(Get-Date) - 播放成功：$($latestVoice.Name)"
```

---

## 🔄 使用场景

### 场景 1：优先级提醒后
```
触发：优先级提醒飞书发送完成
  ↓
调用：ATOM-DELIVERY-013
  ↓
输出：本地播放提醒语音
```

### 场景 2：豆包会话点评后
```
触发：豆包点评飞书发送完成
  ↓
调用：ATOM-DELIVERY-013
  ↓
输出：本地播放点评语音
```

---

## 🔗 关联动作

### 前置动作
- ATOM-DELIVERY-011：飞书发送语音

### 后置动作
- 无（终端动作）

### 常组合使用
- ATOM-VISUAL-008 + ATOM-DELIVERY-011 + ATOM-DELIVERY-013
  （生成 TTS → 飞书发送 → 本地播放）

---

## ✅ 检查清单

执行前确认：
- [ ] Temp 目录有 MP3 文件
- [ ] 文件路径正确
- [ ] Start-Process 可用
- [ ] 系统音量未静音
- [ ] 🆕 屏幕未锁定（或接受跳过播放）
- [ ] 🆕 LockApp 进程检测正常

---

## ⚠️ 常见问题

### 问题 1：找不到文件
```
原因：Temp 目录被清理
解决：重新生成 TTS
```

### 问题 2：播放失败
```
原因：文件损坏或路径错误
解决：检查文件是否存在，重新生成
```

### 问题 3：无声
```
原因：系统静音或音量过低
解决：检查系统音量设置
```

### 问题 4：锁屏时不播放 🆕
```
原因：检测到 LockApp 进程（屏幕锁定）
解决：这是预期行为，解锁后手动播放或重新运行脚本
日志：查看 Temp\voice-playback-log.txt 确认跳过原因
```

---

## 📚 参考文档

- 主数据清单：`原子级动作主数据清单.md`
- 使用 Skill：`skills/feishu-message-automation/SKILL.md`
- 播放脚本：`play-latest-voice.ps1`

---

_模块化定义 | 可独立调用 | 2026-03-07_
