# 钱纠纠 (Qian Jiu Jiu)

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://docs.openclaw.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/your-username/qian-jiu-jiu/releases)

> **只指出问题，不自动修改，静默确认继续**

A Chinese message preprocessor for OpenClaw agents that detects obvious typos, grammar errors, and punctuation issues **without auto-correcting**.

## Features

- 🔍 **Conservative Detection** - Only reports obvious errors, avoids false positives
- 🚫 **Never Auto-corrects** - Respects user autonomy, only points out issues
- 🤫 **Silent Confirmation** - No verbose "confirmed" messages, just seamless continuation
- 📝 **Context-Aware** - Considers conversation history for semantic understanding

## Supported Error Types

| 类型 | Type | 示例 |
|------|------|------|
| 多字 | Redundant | 这不是行啊 → 这不行啊 |
| 少字 | Missing | 你吃饭 → 你吃饭了吗 |
| 重复字 | Repeated | 我我我出门 → 我出门 |
| 错字 | Wrong char | 平果 → 苹果 |
| 错用字 | Misused | 的/得/地 混用 |
| 语序错乱 | Word order | 吃饭了我已经 → 我已经吃饭了 |
| 搭配不当 | Collocation | 喝饭 → 吃饭 |
| 标点缺失 | Missing punct | 出去玩球没买 → 出去玩，球没买? |
| 空格异常 | Spaces | 假 如 → 假如 |
| 单位遗漏 | Missing unit | 178 → 178厘米 |
| 拼音错 | Pinyin | uf → 效果 |

## Installation

```bash
# Via OpenClaw CLI
openclaw skills add your-username/qian-jiu-jiu

# Or manual install
git clone https://github.com/your-username/qian-jiu-jiu.git ~/.openclaw/skills/qian-jiu-jiu
openclaw skills reload
```

## Requirements

- OpenClaw >= 2026.2.x
- Simplified Chinese language support

## How It Works

### Scenario 1: Error Detected
**User:** 我我我要吃饭

**System:**
```
句子存在异常（可能影响理解）：
异常列表：
• 重复字：我我我 → 可能意为：我
是否继续用这个原始句子进行推理？
（回复"是"则直接用上面原始句子推理；否则请修改后重新发送）
```

### Scenario 2: User Confirms
**User:** 是

**System:** (直接回答原句内容，不显示"已确认")
```
好的，你饿了想吃饭。想吃什么呢？
```

### Scenario 3: No Errors
**User:** 我要吃饭

**System:** (静默通过，直接回答)
```
好的，想吃什么菜系？
```

## Format Specification

Error detection output must follow strict line-by-line format:
```
Line 1: 句子存在异常（可能影响理解）：
Line 2: 异常列表：
Line 3+: • [type]: [error] → 可能意为：[meaning]
Line N: 是否继续用这个原始句子进行推理？
Line N+1: （回复"是"则直接用上面原始句子推理；否则请修改后重新发送）
```

## Confirmation Keywords

当用户发送以下词汇时视为确认：
- 是 / 是的
- 确认 / 继续
- ok / yes / y
- 行 / 可以 / 好

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Inspired by the need for respectful, non-intrusive text preprocessing in Chinese conversational AI.
