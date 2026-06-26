# 语音控制增强 Skill - 酷狗 K8 耳机深度集成

> 版本：V1.0  
> 创建时间：2026-03-08 09:05  
> 状态：🟡 待配置  
> 触发词："语音控制"、"语音命令"、"酷狗 K8"

---

## 📋 Skill 定义

**名称：** 语音控制增强 Skill  
**编号：** SKILL-VOICE-CTRL-001  
**触发：** 用户说"语音控制"、"语音命令"、"用语音执行 XX"

**一句话描述：** 酷狗 K8 耳机语音输入 → 语音命令识别 → 执行复杂任务

**核心价值：**
- 解放双手，语音执行复杂任务
- 深度集成酷狗 K8 耳机硬件按键
- 支持自定义语音命令词库

---

## 🎯 目标

**解决什么问题：**
- ✅ 语音输入替代键盘输入
- ✅ 语音命令触发复杂工作流
- ✅ 硬件按键快捷操作
- ✅ 离线语音识别（本地处理）

**核心价值：**
- 效率提升 3-5 倍（语音 vs 打字）
- 单手操作，解放另一只手
- 开车/走路/忙碌时也能用

---

## 🔄 工作流程

```
酷狗 K8 耳机语音输入
  ↓
🆕 语音命令识别（本地关键词匹配）
  ↓
🆕 命令分类（查询/执行/创建/删除）
  ↓
🆕 调用对应 Skill/原子动作
  ↓
🆕 语音 + 文字双重反馈
  ↓
✅ 任务完成
```

---

## 📝 详细步骤

### 步骤 1：酷狗 K8 耳机配置

**硬件准备：**
- 酷狗 K8 蓝牙耳机（已配对）
- 酷狗音乐 App（最新版）
- 语音输入权限已开启

**快捷指令配置：**
```powershell
# 创建快捷指令配置文件
$config = @{
    "device" = "Kugou K8"
    "voiceInput" = $true
    "offlineRecognition" = $true
    "wakeWord" = "嗨阿福"
    "commands" = @(
        @{ "name" = "优先级"; "action" = "priority-reminder" },
        @{ "name" = "生成周报"; "action" = "weekly-report" },
        @{ "name" = "打开 Chrome"; "action" = "open-chrome" },
        @{ "name" = "发送飞书"; "action" = "send-feishu" },
        @{ "name" = "保存会话"; "action" = "save-session" }
    )
}

$config | ConvertTo-Json | Set-Content "voice-commands.json" -Encoding UTF8
```

### 步骤 2：语音命令词库

**预置命令（20 个）：**

| 分类 | 语音命令 | 触发行动 |
|------|---------|---------|
| **查询类** | "当前优先级" | 显示优先级提醒 |
| | "今天天气" | 查询天气预报 |
| | "我的工作" | 显示 worklog.txt |
| | "项目进度" | 显示项目卡片 |
| **执行类** | "生成周报" | 调用周报 Skill |
| | "保存会话" | 调用豆包归档 Skill |
| | "发送飞书" | 调用飞书消息 Skill |
| | "打开 Chrome" | Start-Process Chrome |
| | "播放语音" | 播放最新 TTS |
| **创建类** | "新建待办" | 创建任务卡片 |
| | "记录想法" | 写入 memory/日期.md |
| | "添加会议" | 创建日历事件 |
| **删除类** | "删除提醒" | 删除 Cron 任务 |
| | "清空缓存" | 清理 Temp 文件夹 |

**自定义命令：**
```powershell
# 用户可自定义命令
$customCommands = @{
    "帮我弄那个" = "打开上次编辑的文档"
    "老样子" = "执行昨天的操作"
    "你懂的" = "根据上下文推断"
}
```

### 步骤 3：语音识别引擎

**方案选择：**

**方案 A：Windows 内置语音识别**
```powershell
# 使用 Windows.Speech 命名空间
Add-Type -AssemblyName System.Speech

$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
$grammar = New-Object System.Speech.Recognition.DictationGrammar

$recognizer.LoadGrammar($grammar)
$recognizer.SetInputToDefaultAudioDevice()

$result = $recognizer.Recognize()
Write-Host "识别结果：$($result.Result.Text)"
```

**方案 B：阿里云语音识别（推荐）**
```powershell
# 阿里云智能语音交互
$apiKey = "sk-xxx"
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

# 上传音频文件
$audioPath = "temp-voice-input.wav"
$response = Invoke-RestMethod `
    -Uri "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr" `
    -Method POST `
    -Headers $headers `
    -InFile $audioPath

Write-Host "识别结果：$($response.text)"
```

**方案 C：Whisper 本地识别（离线）**
```powershell
# 使用 Whisper.cpp
$whisperPath = "C:\Tools\whisper.cpp\main.exe"
$audioPath = "temp-voice-input.wav"

& $whisperPath -m "ggml-base.bin" -f $audioPath -l zh
```

### 步骤 4：命令执行引擎

```powershell
function Invoke-VoiceCommand {
    param(
        [string]$CommandText
    )
    
    # 1. 关键词匹配
    $command = $null
    foreach ($c in $global:VoiceCommands) {
        if ($CommandText -like "*$($c.name)*") {
            $command = $c
            break
        }
    }
    
    if (!$command) {
        Write-Host "❌ 未识别命令：$CommandText" -ForegroundColor Red
        return
    }
    
    # 2. 执行对应动作
    Write-Host "▶️  执行命令：$($command.action)" -ForegroundColor Cyan
    
    switch ($command.action) {
        "priority-reminder" {
            # 调用优先级提醒
            & ".\generate-priority-reminder.ps1"
        }
        "weekly-report" {
            # 调用周报生成
            & ".\generate-workreport.ps1"
        }
        "open-chrome" {
            Start-Process "chrome.exe"
        }
        "send-feishu" {
            # 调用飞书消息
            # ...
        }
        default {
            Write-Host "⚠️  未知动作：$($command.action)" -ForegroundColor Yellow
        }
    }
    
    # 3. 语音反馈
    $feedback = "✅ 命令执行完成：$($command.action)"
    & ".\tts-feedback.ps1" -Text $feedback
}
```

### 步骤 5：双重反馈

**文字反馈：**
```markdown
## 🎤 语音命令执行完成

**识别内容：** "生成周报"
**执行动作：** weekly-report
**耗时：** 3.2 秒
**结果：** ✅ 成功

**生成文件：** workreport.txt
**下一步：** 请审阅内容，手动完善措辞
```

**语音反馈：**
```
TTS 生成："✅ 周报已生成，请审阅内容。"
自动播放：Start-Process voice-feedback.mp3
```

---

## 🎯 输入输出

### 输入
- **类型：** 语音（音频流）
- **来源：** 酷狗 K8 耳机麦克风
- **格式：** WAV/MP3
- **时长：** ≤60 秒

### 输出
- **类型：** 文字 + 语音双重反馈
- **内容：** 执行结果 + 下一步建议
- **附加：** 生成的文件/消息

---

## ⚙️ 偏好设置

### 语音识别
- **引擎：** 阿里云智能语音交互（在线）
- **备用：** Whisper.cpp（离线）
- **语言：** 中文普通话
- **方言：** 支持上海话（可选）

### 命令词库
- **预置：** 20 个常用命令
- **自定义：** 用户可随时添加
- **模糊匹配：** 支持同义词

### 反馈方式
- **文字：** Markdown 格式
- **语音：** TTS 自动生成
- **同时发送：** 是

---

## 🔄 使用示例

### 示例 1：语音生成周报

```
用户（语音）："生成周报"
  ↓
识别：阿里云 ASR → "生成周报"
  ↓
匹配：命令词库 → weekly-report
  ↓
执行：调用周报 Skill
  ↓
反馈：
  - 文字：周报已生成，请审阅
  - 语音：TTS 播放"周报已生成"
```

### 示例 2：语音查询优先级

```
用户（语音）："当前优先级"
  ↓
识别：阿里云 ASR → "当前优先级"
  ↓
匹配：命令词库 → priority-reminder
  ↓
执行：读取 worklog.txt，生成优先级
  ↓
反馈：
  - 文字：优先级列表
  - 语音：TTS 播放"最优先任务是..."
```

### 示例 3：语音保存会话

```
用户（语音）："保存刚才的豆包会话"
  ↓
识别：阿里云 ASR → "保存刚才的豆包会话"
  ↓
匹配：命令词库 → save-session
  ↓
执行：调用豆包归档 Skill
  ↓
反馈：
  - 文字：会话已保存到 doubao-sessions/
  - 语音：TTS 播放"会话已保存"
```

---

## 🔗 关联动作

### 前置动作
- 酷狗 K8 耳机配对
- 语音输入权限开启
- 阿里云 API Key 配置

### 后置动作
- 调用对应 Skill（周报/飞书/豆包等）
- TTS 反馈生成
- 本地播放反馈语音

### 复用原子动作
- ATOM-VISUAL-008：生成 TTS 语音
- ATOM-DELIVERY-013：本地播放语音
- ATOM-DELIVERY-010：飞书发送文字
- 🆕 ATOM-VOICE-001：语音命令识别（待创建）
- 🆕 ATOM-VOICE-002：关键词匹配（待创建）

---

## ✅ 检查清单

**配置阶段：**
- [ ] 酷狗 K8 耳机已配对
- [ ] 语音输入权限已开启
- [ ] 阿里云 API Key 已配置
- [ ] 命令词库已创建
- [ ] 快捷指令配置文件已生成

**使用阶段：**
- [ ] 语音清晰，无环境噪音
- [ ] 网络连接正常（在线识别）
- [ ] 命令在词库中
- [ ] 对应 Skill 可用

**执行后：**
- [ ] 命令识别正确
- [ ] 动作执行成功
- [ ] 文字反馈已发送
- [ ] 语音反馈已播放

---

## ⚠️ 常见错误

### 错误 1：识别不准确

```
❌ 错误：环境噪音大，识别错误
✅ 正确：安静环境，靠近麦克风
```

### 错误 2：命令未匹配

```
❌ 错误：说了不在词库中的命令
✅ 正确：使用预置命令或自定义添加
```

### 错误 3：API Key 无效

```
❌ 错误：阿里云 API Key 过期
✅ 正确：检查配置，更新 Key
```

### 错误 4：耳机未连接

```
❌ 错误：酷狗 K8 未配对
✅ 正确：蓝牙设置中重新配对
```

---

## 💡 核心原则

> **语音输入 → 命令识别 → 自动执行 → 双重反馈！**

**关键点：**
1. ✅ 酷狗 K8 硬件集成（耳机按键）
2. ✅ 本地 + 云端双引擎（离线/在线）
3. ✅ 命令词库可扩展
4. ✅ 文字 + 语音双重反馈

**触发词：**
- "语音控制"
- "语音命令"
- "用语音 XX"
- "嗨阿福"（唤醒词）

---

## 📚 参考文档

- 酷狗 K8 说明书：https://www.kugou.com/k8
- 阿里云语音识别：https://help.aliyun.com/product/30487.html
- Whisper.cpp: https://github.com/ggerganov/whisper.cpp
- Windows 语音识别：https://docs.microsoft.com/speech

---

_语音控制增强 | 酷狗 K8 集成 | 解放双手 | 2026-03-08_
_版本：V1.0 - 初始版本，待配置_
