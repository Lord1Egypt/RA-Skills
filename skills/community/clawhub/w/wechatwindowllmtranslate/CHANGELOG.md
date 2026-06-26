# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-04-05

### Added

- 🎉 Initial release of wechat-window-llm-translate
- 🔍 Automatic WeChat window monitoring and new message detection (MBTI style)
- 🌐 Integration with Baidu Translation API for English-to-Chinese translation
- 🤖 Qwen LLM integration for intelligent response generation
- ⚡ Automatic response sending via clipboard automation
- 🔧 Configurable polling interval and response length limits
- 📝 Window management with visibility and focus restoration
- 🎯 Smart text detection using cursor position tracking

### Technical Details

- **Platform**: Windows 10/11
- **Python**: 3.8+
- **Dependencies**: requests, pyautogui, pyperclip, pywin32
- **APIs**: Qwen LLM API, Baidu Translation API

### Configuration

Required environment variables:
- `QWEN_BASE_URL` - Qwen model API base URL
- `QWEN_API_KEY` - Qwen model API key
- `QWEN_URL_PATH` - Qwen API endpoint path
- `BAIDU_APPID` - Baidu Translation app ID
- `BAIDU_APPKEY` - Baidu Translation app key

Optional environment variables:
- `SLEEP_TIME` - Polling interval in seconds (default: 60)
- `REPLY_COUNT` - Response length limit (default: 170)

---

[1.0.0]: https://github.com/openclaw/clawhub/releases/tag/v1.0.0
