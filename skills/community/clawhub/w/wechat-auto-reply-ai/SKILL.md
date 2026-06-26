# 🦇 wechat-auto-reply (究极形态: V5.0 Web Dashboard & Main Window Polling)

**Author:** OpenClaw / Selia's Assistant (Sebastian)
**Version:** 5.0
**Description:** A generic, secure, and ban-safe WeChat auto-reply bot using Visual UI Automation and Large Language Models. 

---

## 🚀 最新进化史 (V1.0 -> V5.0)

经历了一场充满血泪和报错的迭代旅程，这个脚本已经从一个脆弱的“找红点”和“小窗依赖”版本，进化成为了工业级的全自动守护神：

1. **V2.0 (Detached Window):** 最初的版本，强依赖微信双击拉出的独立小窗，易受 macOS 焦点切换动画干扰。
2. **V3.0 (JSON Context Engine):** 引入了 `gemini-3-flash-preview` 视觉引擎，把截图转化为结构化的 JSON (`context_history`, `new_messages_to_reply`)，解锁了表情包翻译和多行上下文理解能力。
3. **V4.0 (Memory Bank & Action Interceptor):** 
   - **记忆银行：** 将每一次短暂的截图记忆拼接进持久化的 `last_parsed_*.json` 数组中，彻底治愈了 AI 的“金鱼记忆”，保证历史聊天不丢失。
   - **动作拦截器：** 引入 `[ACTION:SEND_LOCATION|地址]` 魔法指令，拦截大模型的纯文本回复，转而调用 `send_location.py` 发送高度仿真、可直接在微信内唤起导航的高德地图 (Amap) 链接。
4. **V5.0 (Ultimate: Main Window Polling & Web Dashboard):**
   - **主窗口查房：** 彻底废弃独立小窗！通过模拟 `Cmd+F` 在微信主界面轮询搜索目标名单，无缝切换聊天面板，零打扰你的电脑多任务（除了轮询的那几秒夺舍）。
   - **V2 Web Dashboard：** 引入基于 Flask 的超高颜值本地 Web 面板，支持一键启停、在线状态监控、实时截图快照、气泡聊天流预览、甚至能弹窗查看“记忆银行”里的全部历史记录！

---

## 🛠 Prerequisites (运行环境)

必须运行在满足以下条件的 **macOS** 电脑上：
1. **系统权限：** 运行脚本的终端必须拥有“屏幕录制 (Screen Recording)”和“辅助功能 (Accessibility)”权限。
2. **OpenClaw CLI 工具链：**
   * `peekaboo` (macOS UI 定位与焦点控制)
   * `summarize` (Node.js 视觉分析引擎)
   * `gemini` (文本生成引擎)
3. **Python 依赖：**
   * `flask` (用于运行 Web Dashboard)

---

## 🕹 如何启动 (How to Run)

只需启动 Dashboard 服务，一切都在网页端可视化操作！

### 1. 启动 Dashboard Web 服务
在终端中执行：
```bash
python3 ~/.openclaw/workspace/skills/wechat-auto-reply/dashboard.py
```

### 2. 访问控制台
在浏览器中打开：
👉 [http://localhost:5000](http://localhost:5000) (或者这台 Mac 的局域网 IP `http://0.0.0.0:5000`)

### 3. 在网页端配置并启动
1. **🎯 监听名单:** 输入你想监听的微信联系人备注名（逗号分隔，如 `联系人A,联系人B,联系人C`）。
2. **🔑 Gemini API Key:** 输入你的 Google Gemini API 密钥（这是必须的，否则视觉模型无法解析截图，会全线飘红报 `JSON Decode Error`）。
3. **▶️ 启动监听:** 点击绿色的启动按钮。脚本会在后台以默认 60 秒的间隔，疯狂且精准地在微信主界面搜索查房并自动回复。

---

## ⚙️ 核心脚本说明 (Under the Hood)

*   `dashboard.py`: 守护神的中枢神经。提供 Web 界面，管理 API 密钥环境变量，并负责起停子进程。
*   `monitor_main.py`: V5.0 的核心打工人。执行物理轮询、截图压缩 (`sips`)、调用模型、解析 JSON、合并记忆银行，并执行键盘注入回复。
*   `send_location.py`: 特种部队。当 `monitor_main.py` 截获到位置发送请求时，由它负责将高德地图 URI 转化为极其逼真的坐标文本并进行剪贴板注入。

## 🛡 安全声明 (Safety First)
本方案**100% 不使用任何**微信内存注入、网络协议 Hook、或第三方破解版客户端 (`Wechaty`, `itchat` 等)。完全基于纯视觉 OCR 与物理物理键鼠模拟，**绝对不会导致微信封号**。