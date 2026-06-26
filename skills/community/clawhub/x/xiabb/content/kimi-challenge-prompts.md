# 30分钟 Kimi Code 挑战 — Prompt 模板

> 目标：用 Kimi Code 从零做一个能用的终端版语音转文字工具
> 拍摄时按顺序复制粘贴这些 prompt，每一步都会产生可展示的进度

---

## Prompt 1：基础框架（预计5分钟）

```
用纯 Swift 写一个 macOS 命令行语音转文字工具，单文件 main.swift。

功能：
1. 运行后提示 "按 Enter 开始录音"
2. 按 Enter 开始录音（AVAudioEngine，16kHz mono PCM）
3. 再按 Enter 停止录音
4. 把录音保存为 WAV（加 WAV header）
5. 调用 Google Gemini REST API 转录
6. 输出转录文字到终端

Gemini API 调用方式：
- POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent
- Header: x-goog-api-key: (从环境变量 GEMINI_API_KEY 读取)
- Body: {"contents":[{"parts":[{"text":"Transcribe this audio exactly as spoken, with proper punctuation. Chinese must be Simplified. Preserve original language per word. Output ONLY the transcribed text."},{"inline_data":{"mime_type":"audio/wav","data":"<base64>"}}]}],"generationConfig":{"temperature":0.0,"maxOutputTokens":4096}}

编译方式：swiftc main.swift -o voicetest -framework AVFoundation -framework CoreAudio
```

**拍摄点**: Kimi 开始输出代码，这里可以 4x 加速

---

## Prompt 2：修 Bug（预计3-5分钟）

编译大概率报错，直接贴错误：

```
编译报错了，帮我修：

<粘贴 swiftc 报错信息>
```

重复直到编译通过。

**拍摄点**: 来回修 bug 的过程展示 Vibe Coding 的真实感，不需要加速太多

---

## Prompt 3：第一次测试（预计2分钟）

编译通过后运行测试：

```bash
export GEMINI_API_KEY="你的key"
./voicetest
```

按 Enter 录音，说一句："这是用 Kimi Code 做出来的语音转文字工具"

**拍摄点**: 第一次成功出结果，这是高潮时刻，正常速度播放

---

## Prompt 4：加 Globe 键支持（预计8分钟）

```
现在改成用 Globe 键（fn 键）控制录音：

1. 用 CGEventTap 监听 flagsChanged 事件
2. 检测 fn flag (0x800000)
3. fn 按下 → 开始录音，终端显示 "🔴 录音中..."
4. fn 松开 → 停止录音，发送到 Gemini，显示结果
5. 需要 Accessibility 权限，用 AXIsProcessTrustedWithOptions 提示用户
6. 加一个 5 秒 watchdog timer，如果 event tap 被系统 disable 了就重新启用

编译命令加上：-framework ApplicationServices -framework CoreGraphics

注意 event tap callback 必须极快返回，所有逻辑放到 DispatchQueue.global() 异步执行。
```

**拍摄点**: 这是最关键的一步，Globe 键是虾BB 的核心。这里可以 2x 加速

---

## Prompt 5：修 Globe 键相关 Bug（预计5分钟）

可能遇到的问题：
- Event tap 创建失败 → 需要 Accessibility 权限
- fn 键检测不到 → flag 值不对
- 录音在 callback 线程崩溃 → 要 dispatch 到主线程

```
<粘贴报错或问题描述>
```

**拍摄点**: 如果 Accessibility 权限弹窗出来，这是很好的画面

---

## Prompt 6：加自动粘贴（预计3分钟）

```
转录完成后，自动把文字粘贴到光标位置：

1. 用 NSPasteboard 把文字写入剪贴板
2. 用 CGEvent 模拟 Cmd+V 按键
3. 粘贴完成后终端显示 "✅ 已粘贴: <文字>"

代码：
func copyAndPaste(_ text: String) {
    let pb = NSPasteboard.general
    pb.clearContents()
    pb.setString(text, forType: .string)
    // Simulate Cmd+V
    let src = CGEventSource(stateID: .hidSystemState)
    let keyDown = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: true) // V key
    let keyUp = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: false)
    keyDown?.flags = .maskCommand
    keyUp?.flags = .maskCommand
    keyDown?.post(tap: .cghidEventTap)
    keyUp?.post(tap: .cghidEventTap)
}
```

**拍摄点**: 测试粘贴——打开一个文本编辑器，按 Globe 说话，松开后文字出现在编辑器里。这是最有视觉冲击力的时刻。

---

## Prompt 7（可选加分项）：加实时预览

如果时间还够（<25分钟），可以加：

```
加一个简单的实时预览功能：录音时终端每秒显示 "🔴 录音中... Xs"，显示已录音时长。
```

---

## 最终测试脚本

录完最终版本后，说这几句话测试，展示中英混搭能力：

1. "帮我查一下 OpenClaw 最新的 skills 列表"
2. "用 Claude Code 写一个 API endpoint，要支持 async 和 error handling"
3. "这个 bug 在 production 环境才能复现，需要加 logging"
4. "帮我写一封邮件给 investor，说 Q1 report 已经发了"

---

## 计时里程碑（贴在屏幕旁边参考）

| 时间 | 里程碑 | 状态 |
|------|--------|------|
| 0:00 | 开始，打开 Kimi Code | 🟢 |
| 5:00 | Prompt 1 代码生成完 | 🟢 |
| 10:00 | 编译通过 | 🟢 |
| 12:00 | 第一次录音+转录成功 | 🟡 关键时刻 |
| 20:00 | Globe 键工作 | 🟡 关键时刻 |
| 25:00 | 自动粘贴工作 | 🟡 关键时刻 |
| 30:00 | 最终测试完成 | 🔴 计时结束 |

## 备用方案

如果30分钟内搞不定 Globe 键（CGEventTap 权限问题是最大风险）：
- 退回到 Enter 键方案，也是一个完整可用的工具
- 口播说 "Globe 键需要 Accessibility 权限配置，完整版虾BB 已经处理好了"
- 展示正式版虾BB 作为对比

## 事前 Checklist

- [ ] Kimi Code 安装好并能正常运行
- [ ] `GEMINI_API_KEY` 环境变量设好
- [ ] Xcode Command Line Tools 安装好（`xcode-select --install`）
- [ ] 麦克风权限已授予 Terminal
- [ ] Accessibility 权限已授予 Terminal
- [ ] OBS 录屏 + 人脸画面设好
- [ ] 计时器 app 准备好
- [ ] 跑通一遍完整流程，记录实际耗时
- [ ] 如果 >35分钟，简化 prompt 或预写部分代码
