# Content 1: Twitter/X Thread

---

**Tweet 1 (hook)**
I built a free macOS voice-to-text app in one night that works better than Siri dictation.

280KB. Zero dependencies. Pure Swift.

It speaks Chinese AND English, and the name is a bilingual pun.

Here's the story 🧵

---

**Tweet 2**
The problem: every good voice input tool on Mac is either:

• Siri dictation (decent but clunky, no global hotkey)
• Whisper (great accuracy, but you're running Python, ffmpeg, and a 1.5GB model locally)
• Typeless ($12/mo for what should be a system feature)

I wanted none of that.

---

**Tweet 3**
So I built ClawBB (虾BB).

It sits in your menu bar. Hold Globe key → speak → release → text appears wherever your cursor is.

That's it. No app switching. No UI to interact with. It just works.

Works in ANY app: Notion, Xcode, Terminal, browsers, everything.

---

**Tweet 4**
The name 虾BB is a bilingual pun.

虾 = shrimp (our company mascot, ClawHire 龙虾招聘)
BB = baby? No.

In Cantonese slang, "BB" means "talking" — so 虾BB = a shrimp that talks.

But phonetically in Mandarin, 瞎BB means "talking nonsense."

The name is both the product and the warning label.

---

**Tweet 5**
Technical stack:

• Pure Swift, zero dependencies
• Dual-engine: Gemini Live API (streaming, low latency) + Gemini REST (final, accurate)
• Flash-Lite for real-time translation to your target language
• CGEvent tap for global hotkey capture
• AXUIElement for text injection — no clipboard pollution

280KB total binary.

---

**Tweet 6**
The dual-engine architecture is the key insight.

While you're still speaking → streaming Gemini Live shows a live preview HUD.
When you release the key → REST Gemini fires, returns final accurate text, injects it.

You get BOTH speed feedback AND accuracy. Most tools pick one.

---

**Tweet 7**
vs Typeless ($12/mo):
✅ ClawBB is free, forever
✅ Same global hotkey UX
✅ Bilingual CN/EN in one session
❌ Typeless has a polished settings UI (ours is JSON config for now)

vs local Whisper:
✅ No 1.5GB model download
✅ No Python environment
❌ Whisper works offline (ClawBB needs internet + Gemini API key)

---

**Tweet 8**
The hardest bug: Accessibility permissions on macOS.

CGEvent tap silently fails if you don't have Accessibility access. No error. No crash. Just... nothing.

Spent 45 minutes wondering why Globe key wasn't registering before realizing the permission prompt never appeared.

Now we check and prompt properly on launch.

---

**Tweet 9**
Built entirely with Claude Code in one night.

No prior Swift Audio experience. I described what I wanted, it scaffolded the architecture, I debugged the edge cases with it.

This is what AI-assisted dev actually looks like in 2025: you still need to understand the system, but the surface area you can cover in a night is insane.

---

**Tweet 10 (CTA)**
ClawBB is free and open source.

→ github.com/dyz2102/clawbb

You need a Gemini API key (free tier works). Install takes ~2 minutes.

If you do voice notes, dictat code comments, or just hate typing — try it.

RT if you know a Mac user who'd find this useful.

---

---

# Content 2: 知乎 Article

---

**一个晚上，用AI做了一个比Siri好用的免费语音输入工具**

*ClawBB（虾BB）开发全记录：双引擎架构、踩坑日记、以及为什么叫"瞎BB"*

---

## 一、先说结论

我在一个晚上，用Claude Code从零写了一个macOS语音输入工具，叫做ClawBB（虾BB）。

它的核心特性：

- **全局热键**：按住Globe键说话，松开自动注入文字，任何应用都支持
- **双语混输**：中英文混说，自动识别，不需要切换输入法
- **双引擎架构**：说话时Gemini Live实时预览，松键后REST接口输出最终准确结果
- **极致轻量**：280KB，纯Swift，零依赖，不需要Python环境，不需要下载1.5GB的本地模型
- **完全免费开源**：github.com/dyz2102/clawbb

这篇文章是完整的开发记录，包括技术方案、踩坑经历、竞品分析，以及这个名字为什么叫"虾BB"。

---

## 二、为什么现有工具都不够好用

在开始写代码之前，我用过市面上几乎所有的Mac语音输入方案，逐一说说问题在哪。

**macOS自带听写（Siri Dictation）**

系统自带，不需要安装任何东西，按两次fn键激活。准确率其实还不错，中英文都支持。

但问题是体验割裂：它没有全局热键的"按住说话、松手注入"逻辑。你需要先点击输入框，激活听写，说完，等它处理。如果你在写代码、在Notion里做笔记、在Terminal里输命令，频繁切换焦点非常烦。

更关键的是：它没有实时反馈。你说了很长一段话，屏幕上什么都没有，你不知道它有没有在听。

**本地Whisper**

OpenAI的Whisper模型在准确率上是目前最好的方案之一，尤其是large-v3模型，中英文效果都很强。

但门槛很高：你需要Python环境、ffmpeg、以及至少1.5GB的模型文件。对于非技术用户来说，光是配置环境就要花半天。而且本地推理对CPU/GPU有一定压力，老机器上延迟明显。

**Whisper-based的GUI工具**

比如WhisperMic、MacWhisper等，把Whisper包装成GUI，降低了使用门槛。但本质问题没变：还是本地推理，还是大模型文件，而且部分工具要收费。

**Typeless**

这是目前我见过的体验最好的商业产品。全局热键、菜单栏驻留、实时HUD预览，该有的都有。准确率也很好，背后用的是云端语音API。

但它要$12/月。对于一个"我只是想偶尔语音输入"的需求来说，$12/月真的很难说服自己。

**讯飞输入法**

中文识别准确率很高，在国内有大量用户基础。但macOS版本的体验相比iOS版本差很多，更新也不积极。而且它是完整的输入法，要替换掉系统输入法，很多人不愿意这么做。

**我要的是什么？**

想了想，我的需求其实很简单：

1. 按住一个键说话，松开自动填到光标位置
2. 中英文混说，不需要手动切模式
3. 有实时反馈，知道它在听
4. 轻量，不要装一堆依赖
5. 免费

这四个需求，没有一个现有工具能同时满足。那就自己做。

---

## 三、技术方案设计

花了大概20分钟想清楚架构，核心问题是：**语音识别用什么，文字注入怎么做。**

### 3.1 语音识别：Gemini双引擎

最初想用OpenAI Whisper API（不是本地模型，是云端API），便宜、准确率高。但Whisper API有一个问题：它是非流式的，你必须把整段音频发上去，才能拿到结果。对于"实时预览"的需求来说，这行不通。

Google的Gemini有两个适合的接口：

**Gemini Live API**：流式双向音频，延迟极低，说话时就能实时返回识别结果。这是做实时HUD预览的关键。

**Gemini REST API（音频转文字）**：把录完的音频发上去，返回准确的最终结果。准确率比Live API更高（Live API为了低延迟会做一些取舍）。

两个接口各有优势，所以我做了双引擎架构：

```
用户按住Globe键 → 开始录音
        ↓
Gemini Live API（流式）→ 实时更新HUD预览文字
        ↓
用户松开Globe键 → 停止录音
        ↓
Gemini REST API → 返回最终准确文字
        ↓
AXUIElement注入 → 文字出现在光标位置
```

这样你说话的时候有实时反馈（Live API），松手后注入的是最准确的版本（REST API）。

另外加了Flash-Lite做翻译：如果你设置了目标语言（比如只要中文输出），Gemini在返回识别结果时会顺便翻译。这对于开会时说英语、但要输中文的场景很有用。

### 3.2 文字注入：AXUIElement而不是剪贴板

很多语音输入工具用的是剪贴板注入：把识别结果复制到剪贴板，然后模拟Cmd+V粘贴。

这个方案的问题：
- 会破坏用户当前剪贴板的内容
- 在某些应用里Cmd+V的行为不是"粘贴纯文本"
- 在Terminal里粘贴会触发确认提示（如果内容有换行）

我用的是macOS Accessibility框架里的`AXUIElement`：直接向当前聚焦的文本输入框写入文字，不经过剪贴板。

```swift
func injectText(_ text: String) {
    guard let element = AXUIElementCreateSystemWide()
        .focusedElement else { return }
    
    // 获取当前值，在光标位置插入新文字
    var currentValue: AnyObject?
    AXUIElementCopyAttributeValue(element, kAXValueAttribute as CFString, &currentValue)
    
    let insertionPoint = getInsertionPoint(element)
    let newValue = insert(text, into: currentValue as? String ?? "", at: insertionPoint)
    
    AXUIElementSetAttributeValue(element, kAXValueAttribute as CFString, newValue as CFTypeRef)
}
```

这个方案的效果是：文字像是从键盘输入的，不影响剪贴板，在任何文本输入框都能用。

### 3.3 全局热键：CGEvent Tap

Globe键（地球键）在macOS上的键码是kVK_Function（63），需要用CGEvent Tap来全局捕获，不受当前聚焦应用影响。

---

## 四、用Claude Code开发的过程

我没有写过Swift音频处理的代码。整个项目从零开始，用的是Claude Code。

整体流程大概是：

**第一步（约30分钟）**：描述需求，让Claude Code搭骨架。

我告诉它：macOS菜单栏应用，监听Globe键，按住录音，松手注入。它生成了项目结构、`AppDelegate`、基础的`AVAudioEngine`录音逻辑、以及菜单栏的`NSStatusItem`。

**第二步（约1小时）**：接入Gemini API。

Live API的WebSocket协议文档比较新，Claude Code对最新版本不太熟，这部分我需要参考Google的官方文档，然后让它根据文档实现。REST接口更简单，直接描述需求它就写对了。

**第三步（约2小时）**：调试踩坑。

这是花时间最多的部分，下面单独说。

**第四步（约30分钟）**：UI和配置。

HUD预览窗口（一个半透明浮窗，显示实时识别文字）、菜单栏图标状态切换、JSON配置文件支持（API key、目标语言、热键等）。

Claude Code在这些部分非常高效，样板代码写得又快又标准。

---

## 五、踩坑记录

这部分是整个开发过程中最有意思的，也是最容易让人放弃的。

### 坑1：Accessibility权限的静默失败

CGEvent Tap需要系统的Accessibility权限。如果没有这个权限，`CGEvent.tapCreate`不会报错，不会崩溃，只是返回`nil`，然后什么都不发生。

我花了将近一个小时在调试"Globe键为什么没有反应"，检查了键码、检查了回调注册逻辑，全都是对的。最后才发现是权限问题——权限弹窗根本没有出现，因为应用没有在正确的时机请求权限。

正确的做法是在`applicationDidFinishLaunching`里主动检查并请求：

```swift
func checkAccessibilityPermission() -> Bool {
    let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true]
    return AXIsProcessTrustedWithOptions(options as CFDictionary)
}
```

如果返回`false`，就引导用户去系统设置 → 隐私与安全性 → 辅助功能手动开启。

而且还有一个坑：添加权限后，需要重启应用才生效。这一点一定要在UI里说清楚，否则用户会以为应用有bug。

### 坑2：CGEvent Tap超时

macOS对CGEvent Tap有超时限制：如果你的回调处理时间超过一定阈值，系统会认为这个tap无响应，自动禁用它。

问题是我最初在回调里做了一些同步操作（检查当前应用、判断是否在文本框里），导致偶发性的tap被禁用。

解决方案是把所有非关键逻辑移到异步队列：

```swift
func eventTapCallback(event: CGEvent) -> CGEvent? {
    // 只在回调里做最轻量的判断
    let keyCode = event.getIntegerValueField(.keyboardEventKeycode)
    guard keyCode == kGlobeKeyCode else { return event }
    
    // 其余逻辑异步处理
    DispatchQueue.main.async {
        self.handleGlobeKeyEvent(event.type)
    }
    
    return nil // 吃掉这个事件，不传给其他应用
}
```

### 坑3：Flash-Lite翻译的语言代码bug

Gemini Flash-Lite支持在识别的同时做翻译，在prompt里指定目标语言即可。但我发现一个问题：用`zh-CN`指定中文时，有时返回的是繁体字；用`Chinese`指定时，有时返回英文。

最终发现需要在prompt里更明确地描述：

```
Transcribe the audio. Output in Simplified Chinese (简体中文) only. 
If the audio is in English, translate to Simplified Chinese.
Do not output any explanation, only the transcribed/translated text.
```

光靠语言代码不够可靠，需要在prompt里明确说"简体中文"。

### 坑4：HUD窗口的焦点抢占

最初的HUD实现用的是普通`NSWindow`，结果每次弹出预览窗口，都会抢走当前应用的输入焦点。用户一边说话，输入框焦点已经跑掉了，松手后文字没地方注入。

解决方案：把HUD窗口设置为`NSPanel`，并设置`becomesKeyOnlyIfNeeded = false`、`hidesOnDeactivate = false`，同时把window level设置为`floating`。这样HUD只是悬浮显示，不抢焦点。

```swift
let panel = NSPanel(
    contentRect: .zero,
    styleMask: [.nonactivatingPanel, .borderless],
    backing: .buffered,
    defer: false
)
panel.level = .floating
panel.isFloatingPanel = true
panel.becomesKeyOnlyIfNeeded = false
```

---

## 六、竞品横向对比

| 维度 | ClawBB | Typeless | 本地Whisper | 讯飞输入法 |
|------|--------|----------|-------------|------------|
| 价格 | 免费 | $12/月 | 免费 | 免费（有付费版） |
| 安装体积 | 280KB | ~50MB | 1.5GB+ | ~200MB |
| 实时预览 | 有 | 有 | 无（部分工具有） | 有 |
| 中英混输 | 支持 | 支持 | 支持 | 中文为主 |
| 离线使用 | 不支持 | 不支持 | 支持 | 部分支持 |
| 全局热键 | 支持 | 支持 | 依赖工具 | 支持 |
| 开源 | 是 | 否 | 是（模型） | 否 |
| 剪贴板污染 | 无 | 无 | 有些有 | 无 |

Typeless在产品体验上确实打磨得更好，设置界面、多语言配置都比我的JSON配置文件友好很多。如果你不介意$12/月，Typeless是更完善的商业产品。

ClawBB的优势是：**免费、轻量、开源、可自部署、可二次开发**。技术背景的用户会更喜欢这种方式。

---

## 七、虾BB这个名字的由来

我们公司做的是招聘产品，叫龙虾招聘（ClawHire），虾是我们的吉祥物。

给这个工具起名的时候想：一个会说话的虾，广东话里"BB"有"讲嘢"（说话）的意思，所以虾BB = 一只会说话的虾，很直觉。

但发现粤语梗对北方用户不够友好，想了想，普通话谐音：虾BB，念快一点，就是"瞎BB"——瞎说、乱讲。

一个工具，两个解释：官方解释是"会说话的虾"，非官方解释是"用来瞎BB的工具"。

对语音输入来说，"瞎BB"反而是最准确的描述：你就是在瞎说，让它帮你整理成文字。名字本身就是一种免责声明。

---

## 八、开源发布

项目地址：**github.com/dyz2102/clawbb**

使用前提：
- macOS 13.0+
- 一个Gemini API Key（去 aistudio.google.com 免费申请，免费额度对个人使用完全够）

配置方式很简单，在`~/.clawbb/config.json`里写：

```json
{
  "gemini_api_key": "YOUR_KEY_HERE",
  "target_language": "zh-CN",
  "hotkey": "globe"
}
```

启动后在菜单栏会看到一个虾的图标，按住Globe键说话，松手文字自动填到光标位置。

---

## 九、后记

整个项目从0到能用，花了大概一个晚上（6-7小时）。其中调试踩坑占了一半时间，真正写新功能的时间并不多。

用AI写代码的感受：**你不需要知道所有API的用法，但你必须知道系统在做什么**。Accessibility权限的问题、CGEvent Tap的超时机制、NSPanel和NSWindow的区别——这些都需要有一定的macOS开发背景才能快速定位。AI负责写代码，你负责理解系统。

这个分工在效率上确实有质的飞跃。一个没有Swift音频经验的人，一个晚上做出一个能用的工具，放在三年前是不可能的事。

如果你有macOS，有Gemini API Key，愿意花10分钟配置——试试看。如果有问题或者建议，欢迎在GitHub开Issue。

---

*本文作者是龙虾招聘（ClawHire）的创始人，ClawBB是内部工具开源，不代表公司产品路线。*
