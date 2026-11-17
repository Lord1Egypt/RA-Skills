# Worked Example — AI Coding Models Tier List

A full sample run showing the interview and the resulting board. This topic
(AI models/tools) overlaps highly with TierVibe's audience — a good default
example.

Note the shape of it: **one question at a time**, every option list ends with an
open escape, and the agent shows **one sample** before doing all of them.

## The interview

**Step 0 — mode**

> **Agent**: 图片版还是文字版?(image tier list, or text?) 文字版最快最稳,适合
> 模型名这类抽象条目;图片版好看,但每个条目都要有图。或者你说说你想怎么排。
> **User**: Text — these are model names, a label is enough.

Text mode → skip Step 3½ entirely.

**Step 1 — topic**

> **Agent**: 这个榜单排什么?
> **User**: AI coding models.

**Step 2 — tiers (count, then titles)**

> **Agent**: 分几层?(1-15)
> **User**: 5.

> **Agent**: 每层叫什么?默认是 `T1`-`T5`,通用不挑语言。也可以用
> `S/A/B/C/D`、`夯/顶级/人上人/NPC/拉完了`、`Love/Like/Okay/Meh/Dislike`,
> 或者你自己起 —— 标题栏很窄,每层一个短词最好。
> **User**: 用 夯/顶级/人上人/NPC/拉完了.

No "light or dark board?" question here — `bgBrightness` gets derived in Step 4.

**Step 3 — items & placement**

> **Agent**: 要排哪些?列给我。
> **User**: GPT-4, Claude, Gemini, Copilot, Codex, Llama, Mistral, Qwen.
> GPT-4 and Claude top, Llama and Qwen lower.

> **Agent**: 那我先这么放:夯 = Claude / GPT-4,顶级 = Gemini / Codex,
> 人上人 = Copilot,NPC = Mistral,拉完了 = Llama / Qwen。这样对吗?
> **User**: Yeah.

**Step 4 — color style (ask, then generate)**

> **Agent**: 想要什么配色感觉?柔和马卡龙 / 高饱和鲜艳 / 暗黑沉稳 / 暖色 /
> 冷色 / 单色系,或者你描述一个你想要的。
> **User**: Vibrant, saturated.

> **Agent**: 先给你看一张样卡和一条层级栏 —— 卡片是 `#ffffff` 字 + `#e11d48`
> 底(深底浅字),层级栏 `#FF0000`。整板背景走深色
> (`bgBrightness: 6`),这种高饱和的卡压在深板上会「发光」。这个感觉对吗?
> **User**: 对,就这样。

**Step 5 — commentary depth**

> **Agent**: 每张卡的讲解要多深?① 不要 ② 每张一句话 ③ 每张几个要点
> ④ 每张详细展开(≤1000 字符) ⑤ 你说个你想要的长度/风格。
> **User**: ③ — a few bullets.

> **Agent**: 先给你看 Claude 这张的讲解,确认语气和长度对不对……
> **User**: 可以,其余照这个来。

Then the agent builds the JSON and runs the open command.

## The resulting board

```json
{
  "title": "AI 编程模型 — 从夯到拉",
  "bgBrightness": 6,
  "layoutMode": "horizontal",
  "tiers": [
    {
      "name": "夯",
      "color": "#FF0000",
      "fontSize": 72,
      "cards": [
        { "type": "text", "text": "Claude", "textColor": "#ffffff", "bgColor": "#e11d48",
          "detail": "## 夯\n长上下文推理和谨慎改代码最稳。\n\n- 跨文件重构可靠\n- 边界情况考虑得细\n- prose 与代码都好" },
        { "type": "text", "text": "GPT-4", "textColor": "#ffffff", "bgColor": "#be123c",
          "detail": "## 夯\n全能型,贵但硬任务最可靠。\n\n- 一次性大改首选\n- 通用知识面最广\n- 便宜任务上有点浪费" }
      ]
    },
    {
      "name": "顶级",
      "color": "#FF8C00",
      "fontSize": 56,
      "cards": [
        { "type": "text", "text": "Gemini", "textColor": "#ffffff", "bgColor": "#c2410c",
          "detail": "## 顶级\n超长上下文是杀手锏。\n\n- 整仓读入不费劲\n- 代码质量中上\n- 长任务里偶尔跑偏" },
        { "type": "text", "text": "Codex", "textColor": "#ffffff", "bgColor": "#a16207",
          "detail": "## 顶级\n命令行代理跑得顺。\n\n- 循环式改代码很合适\n- 工具调用稳\n- 需要盯着点方向" }
      ]
    },
    {
      "name": "人上人",
      "color": "#EAB308",
      "fontSize": 36,
      "cards": [
        { "type": "text", "text": "Copilot", "textColor": "#ffffff", "bgColor": "#4d7c0f",
          "detail": "## 人上人\nIDE 内补全体验最好。\n\n- 顺手,几乎无感\n- 自主性弱,不做大改\n- 补全之外能力一般" }
      ]
    },
    {
      "name": "NPC",
      "color": "#22C55E",
      "fontSize": 48,
      "cards": [
        { "type": "text", "text": "Mistral", "textColor": "#ffffff", "bgColor": "#0f766e",
          "detail": "## NPC\n开源里性价比不错。\n\n- 本地部署友好\n- 代码任务偶有翻车\n- 复杂重构别指望" }
      ]
    },
    {
      "name": "拉完了",
      "color": "#3B82F6",
      "fontSize": 36,
      "cards": [
        { "type": "text", "text": "Llama", "textColor": "#ffffff", "bgColor": "#1e40af",
          "detail": "## 拉完了\n本地跑可以,代码明显落后。\n\n- 通用对话还行\n- 多文件任务扛不住" },
        { "type": "text", "text": "Qwen", "textColor": "#ffffff", "bgColor": "#4338ca",
          "detail": "## 拉完了\n中文场景还行,代码深度不够。\n\n- 中文理解是强项\n- 复杂逻辑容易断" }
      ]
    }
  ],
  "candidates": []
}
```

## The final step

The agent base64-encodes that JSON (standard `A-Za-z0-9+/`, NOT base64url), percent-encodes it, and opens the user's default
browser — **it does not save a file**:

```powershell
Start-Process "https://tiervibe.com/t/import#data=<base64>"
```

(macOS `open`, Linux `xdg-open`, Windows cmd/Git Bash `start "" "<url>"`.)

Then, in Chinese to match the list:

> 榜单已经在浏览器里打开了。
> 1. 如果提示登录,登录完会自动回到这个榜单
> 2. 5 个层级 + 8 张卡片 + 讲解都已经填好了
> 3. 拖动卡片排好最终顺序
> 4. 点「发布」

## Notes

- All cards are text cards — zero network/CORS risk, import is instant.
- Every text card carries **both** `textColor` and `bgColor` (Step 4 rule 3). A
  lone color would be dropped by the reader.
- `bgBrightness: 6` is **derived**, not asked for: dark is the default (Step 4
  rule 1) and these saturated card colors glow against it. Only pale,
  low-saturation cards would have flipped the board to 90-97.
- Tier bars run warm→cool top to bottom, saturation high to match the "vibrant"
  style the user picked.
- No `candidates` — the user ranked everything; an empty array is fine (or omit).
- This board's URL comes to ~2,800 characters (2,038 bytes of JSON × ~1.4), so it
  fits every shell comfortably. The ceiling only bites on longer runs — the same
  8 cards at Step 5 depth ④ would land near 10,000 and blow past cmd.exe's 8,191.
  See `SKILL.md` → "Emit + auto-open" for the limits.
