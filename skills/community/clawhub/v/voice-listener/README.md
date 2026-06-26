# 🎤 语音监听助手

> 百度语音识别 + 智能唤醒模式 - 持续语音监听助手

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)
[![Version](https://img.shields.io/badge/version-1.0.0-green)]()
[![License](https://img.shields.io/badge/license-MIT-orange)]()

---

## ✨ 特性

- 🎤 **百度语音识别** - 高准确度的中文语音识别
- ✨ **智能唤醒模式** - 说"小龙虾"激活，"停止"暂停
- 🔄 **持续监听** - 激活后所有语音自动输入
- 📋 **无需重复唤醒** - 激活后持续工作，不用每次都说唤醒词
- 🚀 **简单易用** - 开箱即用，配置简单
- 🆓 **免费使用** - 百度 API 每天 50,000 次免费额度

---

## 📦 安装

### 通过 ClawHub 安装（推荐）

在 OpenClaw 中运行：

```
openclaw skill install voice-listener
```

---

### 手动安装

1. 下载技能文件
2. 解压到 `C:\Users\你的用户名\.agents\skills\voice-listener\`
3. 配置百度 API 密钥（见下方配置说明）
4. 运行 `voice_input_baidu_smart.bat`

---

## ⚙️ 配置

### 百度 API 密钥

1. 访问 [百度 AI 开放平台](https://ai.baidu.com/)
2. 注册/登录账号
3. 进入控制台：https://console.bce.baidu.com/ai/
4. 创建应用，选择"语音识别"
5. 获取：
   - **APP ID**
   - **API Key**
   - **Secret Key**

6. 编辑 `baidu_config.json`：

```json
{
  "APP_ID": "你的APP_ID",
  "API_KEY": "你的API_KEY",
  "SECRET_KEY": "你的SECRET_KEY"
}
```

---

## 🚀 使用方法

### 快速开始

1. 启动程序：双击 `voice_input_baidu_smart.bat`
2. 等待初始化完成
3. 说：**"小龙虾"** 激活
4. 开始说话，文字自动输入
5. 说：**"停止"** 暂停

---

### 工作流程

```
[待机模式]
   ↓
   说: "小龙虾" → [激活模式]
   ↓
   持续语音输入...
   ↓
   说: "停止" → [待机模式]
```

---

### 示例

**激活：**
```
你: "小龙虾"
系统: ✨ 进入激活模式！
```

**输入：**
```
你: "你好"
系统: ✅ 已输入: 你好

你: "帮我打开淘宝"
系统: ✅ 已输入: 帮我打开淘宝
```

**停止：**
```
你: "停止"
系统: 🛑 停止激活模式！
```

---

## 📖 功能说明

### 待机模式（默认）

- **状态**：程序启动后的默认状态
- **行为**：只识别包含"小龙虾"的语音
- **其他语音**：忽略，不会输入

### 激活模式

- **状态**：检测到"小龙虾"后进入
- **行为**：所有语音都会自动输入
- **停止方式**：说"停止"回到待机

---

## 🔧 自定义配置

### 修改唤醒词

编辑 `voice_input_baidu_smart.py` 第31行：

```python
WAKE_WORD = "小龙虾"  # 改成你喜欢的词
```

例如：
```python
WAKE_WORD = "小助手"
WAKE_WORD = "开始"
WAKE_WORD = "指令"
```

---

### 修改停止词

编辑 `voice_input_baidu_smart.py` 第32行：

```python
STOP_WORD = "停止"  # 改成你喜欢的词
```

例如：
```python
STOP_WORD = "结束"
STOP_WORD = "关闭"
STOP_WORD = "待机"
```

---

### 调整灵敏度

编辑 `voice_input_baidu_smart.py` 第22-24行：

```python
# 静音阈值（降低提高灵敏度）
SILENCE_THRESHOLD = 0.02

# 静音时长（增加延长录音时间）
SILENCE_DURATION = 1.5

# 最短语音（增加防止误触发）
MIN_SPEECH_DURATION = 0.5
```

---

## 📊 技术参数

| 参数 | 值 | 说明 |
|------|------|------|
| 采样率 | 16000 Hz | 百度要求 |
| 声道 | 1 | 单声道 |
| 格式 | WAV | 音频格式 |
| 静音阈值 | 0.02 | 可调 |
| 静音时长 | 1.5s | 可调 |
| 最短语音 | 0.5s | 可调 |

---

## 💡 使用技巧

### 提高识别准确度

1. **清楚地说唤醒词**
   - "小 龙 虾" - 每个字都清楚
   - 不要吞音

2. **环境安静**
   - 减少背景噪音
   - 靠近麦克风

3. **语速适中**
   - 不要太快
   - 清楚地发音

---

### 避免误触发

1. **提高静音阈值** - 环境吵闹时
2. **增加最短语音时长** - 防止短促噪音误触发
3. **清楚地说唤醒词** - 确保识别准确

---

## 🐛 常见问题

### 问题1：Token获取失败

**错误**：无法获取百度Access Token

**解决**：
1. 检查 `baidu_config.json` 中的密钥是否正确
2. 检查网络连接
3. 重新登录百度控制台，检查API密钥状态

---

### 问题2：唤醒词检测不到

**错误**：未检测到唤醒词 '小龙虾'

**解决**：
1. 清楚地说"小龙虾"
2. 在安静环境下使用
3. 靠近麦克风

---

### 问题3：停止词检测不到

**错误**：停止不了激活模式

**解决**：
1. 清楚地说"停止"
2. 或者按 `Ctrl+C` 停止程序

---

### 问题4：自动输入失败

**错误**：自动输入失败

**解决**：
1. 文字已复制到剪贴板，手动按 `Ctrl+V` 粘贴
2. 以管理员身份运行程序

---

## 📚 相关资源

- **百度AI开放平台**：https://ai.baidu.com/
- **语音识别文档**：https://ai.baidu.com/ai-doc/SPEECH/Vk38lxily
- **控制台地址**：https://console.bce.baidu.com/ai/
- **ClawHub**：https://clawhub.com/

---

## 📦 技术栈

- **音频处理**：`sounddevice`
- **键盘控制**：`keyboard`
- **剪贴板**：`pyperclip`
- **语音识别**：百度 REST API
- **HTTP 请求**：`requests`

---

## 📝 许可证

MIT License

Copyright (c) 2026 OpenClaw

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🤝 贡献

欢迎贡献！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📮 联系方式

- **作者**：OpenClaw
- **网站**：https://openclaw.ai
- **ClawHub**：https://clawhub.com/

---

## ⭐ Star History

如果这个技能对你有帮助，请给个 Star ⭐

---

**享受语音输入的便利吧！** 🎤✨