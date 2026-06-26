# ATOM-DELIVERY-011 - 飞书发送语音

> 版本：V1.1  
> 状态：✅ 已固化  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 飞书发送语音  
**分类：** 交付层（Delivery Layer）  
**编号：** ATOM-DELIVERY-011

**一句话描述：** 发送 TTS 语音消息到飞书（带文字稿）

---

## 🎯 输入输出

### 输入
- **类型：** MP3 文件路径 + 文字稿
- **文件路径：** `C:\Users\Xiabi\AppData\Local\Temp\tts-*/voice-*.mp3`
- **文字稿：** ≤1500 字符（避免自动摘要）
- **必填：** 是

### 输出
- **类型：** 飞书消息
- **包含：** 语音附件 + 文字稿
- **返回：** messageId

---

## ⚙️ 偏好设置

### 关键参数
- **必须用：** `filePath` 参数
- **禁止用：** `buffer` 参数（会失败）
- **原因：** message 工具要求文件附件用 filePath

### 文字稿格式
```markdown
## 📢 语音消息

[核心内容，1500 字符以内]
```

### 语音偏好
- **声音：** 阿福声音（TTS 默认）
- **长度：** ≤1500 字符（避免摘要）
- **格式：** MP3
- **存储：** Temp 目录（tts-*/voice-*.mp3）

### 自动播放
- **执行：** 发送后立即本地播放
- **方式：** Start-Process 最新 MP3
- **用户操作：** 0 步（全自动）

---

## 📝 操作步骤

```powershell
# 1. 确认 MP3 文件存在
$voicePath = "C:\Users\Xiabi\AppData\Local\Temp\tts-*/voice-*.mp3"
if (-not (Test-Path $voicePath)) {
    Write-Host "❌ MP3 文件不存在：$voicePath"
    return
}

# 2. 准备文字稿
$message = @"
## 📢 语音消息

$voiceScript
"@

# 3. 发送飞书（关键：用 filePath 参数！）
Invoke-MessageSend `
    -Action "send" `
    -FilePath $voicePath `
    -Message $message `
    -Target $targetUserId

# 4. 本地自动播放
Start-Process $voicePath

# 5. 确认
Write-Host "✅ 语音已发送并播放：$voicePath"
```

---

## 🔄 使用场景

### 场景 1：优先级提醒
```
触发：每小时 Cron 任务
  ↓
生成：TTS 语音（优先级提醒内容）
  ↓
调用：ATOM-DELIVERY-011
  ↓
输出：飞书语音消息 + 本地播放
```

### 场景 2：豆包会话点评
```
触发：豆包会话处理完成
  ↓
生成：TTS 语音（核心内容摘要）
  ↓
调用：ATOM-DELIVERY-011
  ↓
输出：飞书语音 + 文字稿 + 本地播放
```

---

## 🔗 关联动作

### 前置动作
- ATOM-VISUAL-008：生成 TTS 语音

### 后置动作
- ATOM-DELIVERY-013：本地播放语音

### 常组合使用
- ATOM-VISUAL-008 + ATOM-DELIVERY-011 + ATOM-DELIVERY-013
  （生成 TTS → 飞书发送 → 本地播放）

---

## ✅ 检查清单

执行前确认：
- [ ] MP3 文件存在
- [ ] 文字稿≤1500 字符
- [ ] **用 filePath 参数**（不用 buffer）
- [ ] 飞书 target 正确
- [ ] 本地播放成功

---

## ⚠️ 常见错误

### 错误 1：用 buffer 参数
```
❌ 错误：-Buffer $base64Data
✅ 正确：-FilePath "C:\...\voice-*.mp3"
```

### 错误 2：文字稿超长
```
❌ 错误：>1500 字符（会被自动摘要）
✅ 正确：≤1500 字符
```

### 错误 3：文件路径错误
```
❌ 错误：相对路径
✅ 正确：绝对路径（C:\Users\Xiabi\AppData\Local\Temp\...）
```

---

## 📚 参考文档

- 主数据清单：`原子级动作主数据清单.md`
- 使用 Skill：`skills/feishu-message-automation/SKILL.md`
- TTS 工具：`tts` tool

---

_模块化定义 | 可独立调用 | 2026-03-07_
