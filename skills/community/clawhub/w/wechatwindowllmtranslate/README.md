# wechat-window-llm-translate

[![Version](https://img.shields.io/npm/v/wechat-window-llm-translate)](https://clawhub.com/package/wechat-window-llm-translate)
[![Platform](https://img.shields.io/badge/platform-win32-blue)](https://clawhub.com/package/wechat-window-llm-translate)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

微信聊天窗口自动监控、翻译和智能回复工具，集成 Qwen 大语言模型和百度翻译 API。

## 🚀 功能特性

- **🔍 自动监控**: 实时检测微信聊天窗口的最新消息
- **🌐 智能翻译**: 自动翻译英文内容为中文
- **🤖 LLM 回复**: 调用 Qwen 模型生成智能回答
- **⚡ 自动发送**: 一键复制并发送回复内容
- **🎯 可配置**: 支持自定义 API 参数和运行间隔

## 📦 安装

```bash
# 安装依赖
clawhub install wechat-window-llm-translate

# 或手动安装
cd skills/wechat-window-llm-translate
uv pip install requests pyautogui pyperclip pywin32
```

## ⚙️ 配置

### 环境变量配置

| 变量名 | 必填 | 说明 | 示例 |
|--------|------|------|------|
| `QWEN_BASE_URL` | ✅ | Qwen 模型 API 基础地址 | `https://api.example.com/v1` |
| `QWEN_API_KEY` | ✅ | Qwen 模型 API 密钥 | `sk-xxx` |
| `QWEN_URL_PATH` | ✅ | Qwen API 接口路径 | `/chat/completions` |
| `BAIDU_APPID` | ✅ | 百度翻译 API APPID | `123456789` |
| `BAIDU_APPKEY` | ✅ | 百度翻译 API APPKEY | `abcdefghijklmnop` |
| `SLEEP_TIME` | ❌ | 轮询间隔 (秒) | `60` |
| `REPLY_COUNT` | ❌ | 回复内容长度限制 | `170` |

### 配置方法

**方法 1: 直接编辑脚本**
```python
# 在 wechatai.py 中修改配置区域
QWEN_BASE_URL = "https://your-api-url"
QWEN_API_KEY = "your-api-key"
# ...
```

**方法 2: 环境变量**
```bash
# Windows PowerShell
$env:QWEN_BASE_URL="https://api.example.com/v1"
$env:QWEN_API_KEY="your-key"
# ...

# 或在 .env 文件中配置
```

## 🎯 使用方法

### 启动运行

```bash
# 方式 1: 直接运行
uv run python wechatai.py

# 方式 2: 使用 npm 脚本
npm start

# 方式 3: 作为 OpenClaw skill
clawx skill run wechat-window-llm-translate
```

### 工作流程

```
1. 启动脚本 → 2. 轮询检测微信窗口 → 3. 识别新消息
                          ↓
6. 自动发送 ← 5. 翻译 (英文→中文) ← 4. 调用 Qwen 模型
```

## 📋 依赖项

```
requests>=2.28.0
pyautogui>=0.9.53
pyperclip>=1.8.2
pywin32>=305
```

## ⚠️ 注意事项

### 系统要求

- **操作系统**: Windows 10/11
- **Python**: 3.8+
- **依赖库**: 详见 `requirements.txt`

### 权限要求

- 屏幕控制权限 (用于窗口操作)
- 剪贴板访问权限 (用于复制粘贴)
- 网络访问权限 (用于 API 调用)

### 配置调整

**坐标配置**: 脚本根据屏幕分辨率自动调整坐标:



**窗口识别**: 默认查找标题包含"微信"的窗口，可在 `activategptwindow()` 函数中修改匹配条件。

## 🔧 故障排除

### 常见问题

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| 找不到微信窗口 | 窗口标题不匹配 | 修改 `activategptwindow()` 中的匹配条件 |
| API 调用失败 | 密钥错误/网络问题 | 检查环境变量配置和网络连接 |
| 点击位置不准确 | 屏幕分辨率不同 | 调整脚本中的坐标值 |
| 翻译失败 | API 配额不足 | 检查百度翻译 API 配额 |
| 中文乱码 | 编码问题 | 确保使用 UTF-8 编码 |

### 调试模式

```bash
# 启用详细日志
uv run python wechatai.py 2>&1 | tee debug.log
```

## 📄 许可证

MIT License

---

**作者**: 六弦如水  
**版本**: 1.0.9  
**平台**: Windows 10/11  
**最后更新**: 2024-04-05

## 🙏 致谢

- [Qwen](https://github.com/QwenLM/Qwen) - 通义千问大语言模型
- [百度翻译开放平台](https://fanyi-api.baidu.com/) - 翻译服务
- [OpenClaw](https://openclaw.ai) - AI 助理平台
