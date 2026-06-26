# ATOM-VISUAL-008 - 生成 TTS 语音

> 版本：**V2.0**  
> 状态：✅ 已固化  
> 最后更新：**2026-03-07 15:18**

---

## 📋 动作定义

**名称：** 生成 TTS 语音  
**分类：** 呈现层（Visual Layer）  
**编号：** ATOM-VISUAL-008

**一句话描述：** 将文字稿转换成 MP3 语音文件

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 文字稿（≤1500 字符）

### 输出
- **类型：** 文件
- **路径：** `workspace/tts/voice-时间戳.mp3`
- **示例：** `C:\Users\Xiabi\.openclaw\workspace\tts\voice-1772864000000.mp3`

---

## ⚙️ 偏好设置

### 语音偏好
- **声音：** 阿福声音（TTS 默认）
- **长度：** ≤1500 字符（避免自动摘要）
- **格式：** MP3
- **存储：** **workspace/tts 文件夹**（统一归档）
- **命名：** `voice-时间戳.mp3`（时间戳精确到毫秒）

### 文字稿要求
- **编码：** UTF-8
- **语言：** 中文
- **风格：** 口语化、自然流畅
- **禁止：** 特殊符号、过长句子

---

## 📝 操作步骤

```powershell
# 1. 准备文字稿
$text = "你好，这是优先级提醒..."

# 2. 确保 TTS 文件夹存在
$ttsFolder = "C:\Users\Xiabi\.openclaw\workspace\tts"
if (!(Test-Path $ttsFolder)) {
    New-Item -ItemType Directory -Path $ttsFolder -Force | Out-Null
}

# 3. 生成文件名（时间戳）
$timestamp = [DateTimeOffset]::Now.ToUnixTimeMilliseconds()
$voiceFile = Join-Path $ttsFolder "voice-$timestamp.mp3"

# 4. 调用 TTS 工具
Invoke-TTS `
    -Text $text `
    -OutputPath $voiceFile

# 5. 确认生成
if (Test-Path $voiceFile) {
    Write-Host "✅ TTS 语音已生成：$voiceFile" -ForegroundColor Green
    Write-Host "  大小：$((Get-Item $voiceFile).Length) 字节" -ForegroundColor Gray
} else {
    Write-Host "❌ TTS 语音生成失败" -ForegroundColor Red
}
```

---

## 🔄 使用场景

### 场景 1：优先级提醒
```
触发：每小时 Cron 任务
  ↓
生成：优先级提醒文字稿
  ↓
调用：ATOM-VISUAL-008
  ↓
输出：MP3 语音文件
```

### 场景 2：豆包会话点评
```
触发：豆包会话处理完成
  ↓
生成：核心内容摘要
  ↓
调用：ATOM-VISUAL-008
  ↓
输出：点评语音
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-DELIVERY-011：飞书发送语音
- ATOM-DELIVERY-013：本地播放语音

### 常组合使用
- ATOM-VISUAL-008 + ATOM-DELIVERY-011 + ATOM-DELIVERY-013
  （生成 TTS → 飞书发送 → 本地播放）

---

## ✅ 检查清单

执行前确认：
- [ ] 文字稿≤1500 字符
- [ ] 文字稿口语化
- [ ] Temp 目录可写
- [ ] TTS 工具可用

---

## ⚠️ 常见错误

### 错误 1：文字稿超长
```
❌ 错误：>1500 字符（会被自动摘要）
✅ 正确：≤1500 字符，分段生成
```

### 错误 2：Temp 目录不可写
```
❌ 错误：权限不足
✅ 正确：检查目录权限
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
