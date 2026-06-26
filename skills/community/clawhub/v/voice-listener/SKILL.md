# Voice Listener Skill

百度语音识别 + 智能唤醒技能

## 功能

- 🎤 百度语音识别（高准确度）
- ✨ 智能唤醒模式："小龙虾"激活，"停止"暂停
- 🔄 持续监听：激活后所有语音自动输入
- 📋 无需每次都说唤醒词

## 快速开始

### 方式1：通过OpenClaw技能系统调用（推荐）

在对话中直接说或输入：
```
启动语音监听
```

OpenClaw会自动调用此技能并启动语音识别程序。

### 方式2：启动脚本

双击运行：
```
voice_input_baidu_smart.bat
```

### 方式3：命令行

在技能目录下运行：
```bash
python start_voice_listener.py
```

## 使用方法

### 激活模式

1. 双击 `voice_input_baidu_smart.bat` 启动程序
2. 程序进入待机模式
3. 说：**"小龙虾"**
4. 程序进入激活模式
5. 所有语音都会自动识别并输入

### 持续输入

激活后，你说的话会自动输入到光标位置：

```
说: "你好" → 自动输入
说: "帮我打开淘宝" → 自动输入
说: "今天天气怎么样？" → 自动输入
```

### 暂停输入

说：**"停止"**

程序回到待机模式，不会再输入你的语音。

## 配置文件

### 百度 API 配置

编辑 `baidu_config.json`：

```json
{
  "APP_ID": "你的APP_ID",
  "API_KEY": "你的API_KEY",
  "SECRET_KEY": "你的SECRET_KEY"
}
```

### 修改唤醒词

编辑 `voice_input_baidu_smart.py`：

```python
# 唤醒词
WAKE_WORD = "小龙虾"  # 改成你喜欢的词

# 停止词
STOP_WORD = "停止"  # 改成你喜欢的词
```

## 工作流程

```
[待机模式]
   ↓
   说: "小龙虾" → [激活模式]
   ↓
   持续语音输入...
   ↓
   说: "停止" → [待机模式]
```

## 文件说明

### 核心文件

- `voice_input_baidu_smart.py` - 智能唤醒模式（推荐）
- `voice_input_baidu_smart.bat` - 启动脚本
- `baidu_config.json` - 百度API配置

### 其他版本

- `voice_input_baidu.py` - 简单持续监听（无唤醒词）
- `voice_input_baidu_wakeup.py` - 单次唤醒版本
- `BAIDU_README.md` - 百度API使用指南
- `SMART_WAKEUP_README.md` - 智能唤醒详细指南

### 配置文件

- `baidu_config.json` - 百度API密钥配置

## 技术参数

### 音频配置

- 采样率：16000 Hz（百度要求）
- 声道：1（单声道）
- 格式：WAV
- 静音阈值：0.02（可调）
- 静音时长：1.5 秒（说话结束后停止录音）
- 最短语音：0.5 秒（防止误触发）

### API 配置

- 识别引擎：百度语音识别 API
- Token API：https://aip.baidubce.com/oauth/2.0/token
- 识别 API：https://vop.baidu.com/server_api
- 免费额度：50,000 次/天
- 语言：普通话（支持简单英文）

## 优势

| 特性 | 说明 |
|------|------|
| ✅ 高准确度 | 百度语音识别准确度高 |
| ✅ 智能唤醒 | 唤醒后持续工作 |
| ✅ 易控制 | 明确的激活/停止 |
| ✅ 免费额度高 | 每天50,000次 |
| ✅ 配置简单 | 只需三个API密钥 |

## 常见问题

### 问题1：Token获取失败

**错误：** 无法获取百度Access Token

**解决：**
1. 检查 `baidu_config.json` 中的密钥是否正确
2. 检查网络连接
3. 重新登录百度控制台，检查API密钥状态

### 问题2：唤醒词检测不到

**解决：**
1. 清楚地说"小龙虾"
2. 在安静环境下使用
3. 靠近麦克风

### 问题3：停止词检测不到

**解决：**
1. 清楚地说"停止"
2. 或者按 `Ctrl+C` 停止程序

## API 密钥申请

### 获取步骤

1. 访问：https://ai.baidu.com/
2. 注册/登录账号
3. 进入控制台：https://console.bce.baidu.com/ai/
4. 创建应用
5. 选择"语音识别"
6. 获取 APP ID, API Key, Secret Key
7. 填入 `baidu_config.json`

### 文档

- 百度AI开放平台：https://ai.baidu.com/
- 语音识别文档：https://ai.baidu.com/ai-doc/SPEECH/Vk38lxily
- 控制台地址：https://console.bce.baidu.com/ai/

## 输出

识别结果：
- 自动输入到光标位置
- 同时在控制台显示识别文本
- 失败时复制到剪贴板，手动粘贴

## 技术栈

- 音频处理：`sounddevice`
- 键盘控制：`keyboard`
- 剪贴板：`pyperclip`
- 语音识别：百度 REST API
- HTTP 请求：`requests`