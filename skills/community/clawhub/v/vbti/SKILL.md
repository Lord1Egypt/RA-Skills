---
name: vbti
description: Vibe-coding Type Indicator — 扫你 vibe coding 历史记录，把你审判为 16 型 vibe coder 中的一种，生成一张诊断书风格的 HTML 卡片到桌面，可直接截图发小红书。当用户输入 /vbti、说"测一下我的 vibe coding 人格"、"我是哪型 vibe coder"、"生成我的 VBTI"时触发。
---

# VBTI · Vibe-coding Type Indicator

把用户的 vibe coding 使用习惯审判为 16 型 vibe coder 之一，生成诊断书卡片。

## 触发

- 用户输入 `/vbti`
- 用户说"测我的 VBTI"、"我是哪型 vibe coder"、"vibe coding 人格"

## 怎么跑

直接调用（按用户实际安装路径选一个）：

```bash
python3 ~/.claw/skills/vbti/run.py      # OpenClaw / Claw
python3 ~/.claude/skills/vbti/run.py    # Claude Code
```

它会：
1. 扫 `~/.claude/projects/*/` 下所有 transcript JSONL
2. 统计 16 个维度的信号（关键词词频、Bash 命令分布、文件操作类型、时间分布等）
3. 给 16 个类型打分，挑分数最高的
4. 把真实数据填进诊断书模板，输出 HTML 到 `~/Desktop/我的-VBTI-{TYPE}.html`
5. 自动 open 在浏览器里

## 16 个类型一览

SOON · MONK · SHOW · VIBE · BLAM · YEET · GHST · LOOP · MOSS · SORY · NODE · DUMP · TOYS · TIDY · LERN · TEST

详细定义见 `vbti_types.py`。

## 跑完之后

告诉用户：
- TA 是哪个型（中文名 + emoji）
- 一句话 tagline
- 桌面文件路径
- 让 TA 截图发小红书时 #VBTI

不要解释信号怎么算的（破坏魔性）。
