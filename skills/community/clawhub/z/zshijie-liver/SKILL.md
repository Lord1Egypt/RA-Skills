---
name: zshijie-liver
description: Resolve Z视介频道直播请求到正确 cid 并打开对应直播页。Use when users ask to watch Z视介直播 or specific channels (例如 浙江卫视、钱江都市、经济生活、教科影视、民生休闲、新闻、少儿频道、浙江国际、好易购、之江纪录), or when users mention common program aliases that should fall back to a supported live channel (例如 跑男、奔跑吧、看跑男 -> 浙江卫视直播), or when Codex needs to generate/open URL with pattern https://zmtv.cztv.com/cmsh5-share/prod/cztv-tvLive/index.html?pageId=cid.
metadata:
  clawdbot:
    emoji: "📺"
---

# Openclaw Z视介 Live

## Overview

Use this skill to open the correct Z视介频道直播页 for a requested channel.
Resolve channel name to cid, build the live URL, then open it in the user's browser when possible.
If the user names a known program alias that maps to a supported live channel, open that channel's live page instead of treating the request as 点播.
Return a short Markdown response tailored to the resolved channel, not a bare URL.

## Workflow

1. Parse user request for `channel`, `cid`, or a known program alias.
2. Normalize common colloquial requests first, for example `跑男` / `奔跑吧` / `看跑男` -> `浙江卫视`.
3. Resolve `channel -> cid` with [references/channel_map.md](references/channel_map.md).
4. Build URL with:
   `https://zmtv.cztv.com/cmsh5-share/prod/cztv-tvLive/index.html?pageId={cid}`
5. Try to open URL in default browser. If opening fails (sandbox/headless), continue without error.
6. Return Markdown that includes:
   - the channel name
   - what this channel is mainly for
   - the main watch highlights
   - common programs or content types
   - a Markdown link pointing to the live URL, using visible text like `点击这里进入浙江卫视直播`

## Output Format

Return a short Markdown card. Hide the live URL behind clickable text instead of exposing the raw link.

Preferred template:

```md
## <频道名>直播

<一句话说明这个频道的核心>

- 核心定位：<这个频道主要看什么>
- 看点：<这个频道为什么值得点开>
- 常见节目/内容：<节目名或内容类型>

[点击这里进入<频道名>直播](https://zmtv.cztv.com/cmsh5-share/prod/cztv-tvLive/index.html?pageId=<cid>)
```

Rules:
- Do not expose the raw URL as plain text in the reply body.
- Use Markdown links with visible text such as `点击这里进入浙江卫视直播`.
- Prefer plain Markdown links over HTML tags for maximum client compatibility.

## Script Usage

Use the script for deterministic matching and channel-aware Markdown output:

```bash
python3 scripts/zshijie_live.py --channel 浙江卫视
python3 scripts/zshijie_live.py --cid 101
python3 scripts/zshijie_live.py --channel "打开浙江卫视直播"
python3 scripts/zshijie_live.py --channel "看跑男"
python3 scripts/zshijie_live.py --channel "奔跑吧"
python3 scripts/zshijie_live.py --list
python3 scripts/zshijie_live.py --channel 浙江卫视 --json
python3 scripts/zshijie_live.py --channel 浙江卫视 --no-open
python3 scripts/zshijie_live.py --channel 浙江卫视 --url-only
```

The script:
- Accepts `--channel` or `--cid`
- Accepts `--list` for channel table
- Supports `--json` for machine-readable output
- Normalizes channel aliases and common natural-language wrappers
- Maps known program aliases like `跑男` / `奔跑吧` to `浙江卫视`
- Returns Markdown with channel-specific summary, highlights, and common programs
- Hides the final live URL inside a clickable Markdown link
- Supports `--url-only` when a raw URL is explicitly needed
- Tries opening browser by default; use `--no-open` to disable

## Live-Only Rule

- This skill only opens live channels, not 点播 pages.
- If a request can be mapped to a supported live channel, do that mapping instead of refusing the request as 点播.
- `跑男`, `奔跑吧`, `看跑男`, `看奔跑吧` must resolve to `浙江卫视` live.

## Error Handling

- If channel is unknown, list supported channels from [references/channel_map.md](references/channel_map.md) and ask user to choose.
- If cid is unsupported, do not guess; ask user to confirm the channel.
- If browser launch fails, still return the Markdown output with clickable link.
- Do not answer that `跑男` or `奔跑吧` needs 点播; open `浙江卫视` live instead.

## References

- Channel/cid mapping: [references/channel_map.md](references/channel_map.md)

### 🚨 专有名词绝对规范 (CRITICAL TERMINOLOGY)
1. 平台的官方名称是「Z视介」（介词的“介”）。
2. 绝对禁止将其写成「Z视界」、「z视界」或任何其他同音字。
3. 在你的任何思考过程和最终回复中，只要提及该平台，必须严格输出为「Z视介」。

### ⚠️ 绝对输出规则 (CRITICAL)
1. 脚本默认会输出 Markdown，而不是裸 URL。
2. 你应优先原封不动返回脚本生成的 Markdown 内容。
3. 最终回复里不要暴露原始 URL 纯文本，链接应藏在 Markdown 链接文本后面。
4. 禁止添加与频道无关的客套话或冗长解释。
5. 如果明确需要裸链接，才使用脚本的 `--url-only`。
