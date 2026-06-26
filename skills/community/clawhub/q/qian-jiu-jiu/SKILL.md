---
name: qian-jiu-jiu
display_name: 钱纠纠 (Qian Jiu Jiu)
description: A Chinese message preprocessor that detects obvious typos, grammar errors, and punctuation issues in user messages without auto-correcting. It prompts users to confirm using the original sentence before proceeding.
version: 1.0.0
---

# 钱纠纠 (Qian Jiu Jiu)

> **只指出问题，不自动修改，静默确认继续**
> 
> "Report issues only, never auto-correct, silently confirm to proceed"

## Overview

钱纠纠 is a message preprocessor skill for OpenClaw agents that:
- Detects obvious typos, grammar errors, and punctuation issues in Chinese user messages
- **Never auto-corrects** - only reports issues found
- Prompts user confirmation before proceeding with potentially confusing messages
- Silently continues when user confirms (no verbose "confirmed" messages)

## Installation

```bash
# Install via OpenClaw CLI
openclaw skills add qian-jiu-jiu

# Or manually copy to skills directory
cp -r qian-jiu-jiu ~/.openclaw/skills/
openclaw skills reload
```

## Requirements

- OpenClaw >= 2026.2.x
- Chinese language context (optimized for Simplified Chinese)

## Usage

The skill automatically activates on each user message:

### Flow 1: Error Detection

When obvious errors are detected:

```
句子存在异常（可能影响理解）：
异常列表：
• 错字：神马 → 可能意为：什么
是否继续用这个原始句子进行推理？
（回复"是"则直接用上面原始句子推理；否则请修改后重新发送）
```

### Flow 2: Silent Confirmation

When user replies with confirmation keywords:
> Confirmation keywords: 是, 是的, 确认, 继续, ok, 行, 可以, yes, y, 好

The skill **silently proceeds** with the original sentence - no verbose confirmation, no "original sentence:" display, just normal response.

### Flow 3: Clean Pass-through

If no obvious errors - message flows through normally without any output.

## Error Types Detected

| Type | Description | Example |
|------|-------------|---------|
| `多字` | Redundant characters | 这不是行啊 → 这不行啊 |
| `少字` | Missing characters | 你吃饭 → 你吃饭了吗 |
| `重复字` | Repeated characters | 我我我要出门 → 我要出门 |
| `错字` | Wrong/typo characters | 平果 → 苹果 / 神马 → 什么 |
| `错用字` | Misused homophones | 的/得/地 混用 |
| `语序错乱` | Wrong word order | 吃饭了我已经 → 我已经吃饭了 |
| `搭配不当` | Collocation errors | 喝饭 → 吃饭 |
| `标点缺失` | Missing punctuation causing ambiguity | 我想出去玩球没买 → 出去玩，球没买? / 出去玩球，没买? |
| `空格异常` | Invalid spaces in words | 假 如 → 假如 |
| `单位遗漏` | Missing units after numbers | 身高178 → 身高178厘米 |
| `拼音错` | Pinyin instead of characters | uf → 效果 / nihao → 你好 |

## Response Format

### Error Detection Format (Strict line-by-line):
```
句子存在异常（可能影响理解）：\n
异常列表：\n
• [type]: [error] → 可能意为：[possible meaning]\n
是否继续用这个原始句子进行推理？\n
（回复"是"则直接用上面原始句子推理；否则请修改后重新发送）
```

### Confirmation Response Format:
```
[Normal response to the original sentence]
```

## Key Constraints

1. **Never auto-correct** - Only report, never suggest "correct version"
2. **Silent confirmation** - No "confirmed", "proceeding", or "OK" messages
3. **Conservative detection** - Better to miss than over-report
4. **No empty lines** between output lines (use `\n` only)
5. **Context-aware** - Considers conversation history for ambiguous cases

## License

MIT

## Contributing

Issues and PRs welcome at https://github.com/[your-username]/qian-jiu-jiu
