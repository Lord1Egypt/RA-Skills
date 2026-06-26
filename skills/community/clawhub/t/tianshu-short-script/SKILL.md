---
name: tianshu-short-script
description: >
  根据主题与时长生成短视频口播分镜表：镜号、秒数、画面、口播、花字/字幕提示。
  Use when: 用户要做短视频、口播、分镜、抖音/B 站/视频号脚本；用户说「口播脚本」「分镜表」「60 秒视频怎么拍」。
  NOT for: 直接导出剪映工程文件；复杂多机位院线级分镜（本 skill 偏口播/Vlog 结构）。
metadata:
  openclaw:
    primaryEnv: ""
---

# 短视频口播分镜表 (tianshu-short-script)

按**主题 + 总时长 + 镜头数**生成可执行的 Markdown 分镜表，便于拍摄与剪辑对齐。纯本地生成模板，深度文案可由模型先写好主题要点再运行脚本。

## When to Run

- 「帮我写个 60 秒口播脚本」「分镜怎么拆」「抖音口播大纲」
- 已有选题/卖点，需要拆成镜头与时间轴

## Workflow

1. 向用户确认：主题一句话、目标时长（秒）、希望几条镜头（默认按时长自动算）
2. 执行：
   ```bash
   node ~/.openclaw/skills/tianshu-short-script/scripts/make_script.js \
     --topic "选题描述" \
     --seconds 60 \
     --shots 6
   ```
3. 将输出的表格交给用户；台词列可再根据品牌语气由模型润色

## 参数说明

| 参数 | 说明 |
|------|------|
| `--topic` / `-t` | 视频主题/卖点（必填） |
| `--seconds` / `-s` | 总时长（秒），默认 `60` |
| `--shots` / `-n` | 镜头条数；默认按 `seconds/10` 估算，范围 3～12 |
| `--platform` / `-p` | `douyin` \| `wechat` \| `bilibili`（影响片头/尾提示文案），默认 `douyin` |

## Output

Markdown 表格：**镜号 | 时长(秒) | 画面/景别 | 口播要点 | 花字/字幕**，并附**片头钩子**与**结尾 CTA** 占位说明。
