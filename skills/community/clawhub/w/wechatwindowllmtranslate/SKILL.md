---
name: wechat-window-llm-translate
description: 微信聊天窗口自动监控、翻译和智能回复工具，集成 Qwen 大语言模型和百度翻译 API。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - QWEN_BASE_URL
        - QWEN_API_KEY
        - QWEN_URL_PATH
        - BAIDU_APPID
        - BAIDU_APPKEY
    primaryEnv: QWEN_API_KEY
    emoji: "🤖"
    homepage: https://github.com/openclaw/clawhub
    os: ["win32"]
---

# wechat-window-llm-translate - 微信窗口智能翻译回复

微信聊天窗口自动监控、翻译和智能回复工具。通过监控微信聊天窗口，自动提取问题并调用 Qwen 模型生成智能回复MBTI个性化回复（可选），支持自动翻译成中文。

## 功能特性

- **自动监控**: 轮询监控微信聊天窗口，自动检测新问题
- **智能翻译**: 集成百度翻译 API，自动翻译英文内容为中文
- **LLM 回复**: 调用 Qwen 模型生成智能回答
- **个性化聊天**: 可选MBTI 16种个性语气
- **自动发送**: 将回复内容自动复制并发送
- **可配置**: 支持配置 API 地址、密钥、轮询间隔等参数

## 安装

```bash
clawhub install wechat-window-llm-translate
```

## 配置

使用前需要配置以下环境变量:

```bash
# Qwen 模型配置
export QWEN_BASE_URL="https://your-model-api-base-url"
export QWEN_API_KEY="your-qwen-api-key"
export QWEN_URL_PATH="/v1/chat/completions"

# 百度翻译配置
export BAIDU_APPID="your-baidu-appid"
export BAIDU_APPKEY="your-baidu-appkey"
export BAIDU_ENDPOINT="http://api.fanyi.baidu.com"
export BAIDU_PATH="/api/trans/vip/translate"

# 运行配置
export SLEEP_TIME="60"           # 轮询间隔 (秒)
export REPLY_COUNT="170"         # 回复内容长度限制
```

## 使用方法
1. **先登陆桌面端微信**
2. **通过openclaw后台运行或者cmd命令行终端启动wechatai.py**
3. **鼠标移到最左边等待退出运行**
### 直接运行

```bash
uv run python wechat-window-llm-translate.py
```

### 作为 OpenClaw Skill 运行

```bash
clawx skill run wechat-window-llm-translate
```

## 工作原理

1. **窗口激活**: 自动查找并激活包含"微信"字样的窗口
2. **内容监控**: 通过鼠标滚动和光标检测，识别新的聊天消息
3. **文本提取**: 双击选中并复制最后一条消息内容
4. **智能处理**: 调用 Qwen 模型生成精简回答 (200 字以内)，生成MBTI个性回答
5. **翻译优化**: 如果回答是英文，自动翻译成中文
6. **自动回复**: 将回复内容复制到剪贴板并自动发送

## 依赖

```python
requests>=2.28.0
pyautogui>=0.9.53
pyperclip>=1.8.2
pywin32>=305
```

## 使用说明

### 前提条件

1. 安装所有 Python 依赖
2. 配置 Qwen 模型 API 地址和密钥
3. 配置百度翻译 API 的 APPID 和 APPKEY
4. 确保微信窗口标题包含"微信"字样
5. 屏幕分辨率和坐标基于当前环境配置
6. 关闭微信窗口退出运行
7. 需要在openclaw.json文件中env字段配置环境变量
          "QWEN_BASE_URL": "",
          "QWEN_API_KEY": "",
          "QWEN_URL_PATH": "",
          "BAIDU_APPID": "",
          "BAIDU_APPKEY": "",
          "BAIDU_ENDPOINT": "http://api.fanyi.baidu.com",
          "BAIDU_PATH": "/api/trans/vip/translate",          
          "mbti_selected": "ISTJ",
          "refresh": "30"
### 坐标调整

脚本中使用了一些屏幕分辨率的坐标值，可能需要根据您的屏幕分辨率和窗口位置进行调整:


### 注意事项

⚠️ **重要提示**:

1. 此脚本需要运行在 Windows 系统上
2. 需要授予脚本屏幕控制和剪贴板访问权限
3. 请妥善保管 API 密钥，不要提交到公共仓库
4. 建议先测试 API 连接是否正常
5. 根据实际窗口位置调整坐标参数

## 故障排除

### 常见问题

**问题**: 找不到微信窗口
- **解决**: 确保微信窗口标题包含"微信"字样，或修改 `activategptwindow()` 函数中的匹配条件

**问题**: API 调用失败
- **解决**: 检查环境变量配置是否正确，验证 API 密钥是否有效

**问题**: 坐标点击不准确
- **解决**: 根据您的屏幕分辨率调整脚本中的坐标值

**问题**: 翻译失败
- **解决**: 检查百度翻译 API 配额是否充足，APPID 和 APPKEY 是否正确

## 许可证

MIT License

---

**作者**: Created for 六弦如水  
**版本**: 1.0.10  
**平台**: Windows 10/11
