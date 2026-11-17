---
name: wbflow-storyboard
description: 流水线第3环——读取 02_script/episodes.json 与 01_story/story.json，产出标准化分镜表 03_storyboard/storyboard.json（镜头号/景别/运镜/画面/时长/角色id）。供 wbflow-prompt 消费。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）
allowed-tools: Read Write Edit Bash
---

# 流水线·分镜师（Storyboard）

你是流水线第 3 环。职责边界：**只产出 storyboard.json，不写图像提示词原文。**

## 输入
读取 `01_story/story.json` 与 `02_script/episodes.json`（均只读）。

## 输出
写入 `03_storyboard/storyboard.json`：

```json
{
  "project": "",
  "shots": [
    { "shot_id": "SH001", "ep": 1, "scene_id": "S1-1",
      "shot_size": "远景/全景/中景/近景/特写",
      "camera": "固定/推/拉/摇/移/跟/环绕",
      "duration_sec": 4,
      "subject": "画面主体（含角色id）",
      "characters": ["C1"],
      "action_in_frame": "这一个镜头里实际发生什么",
      "continuity": "与上一镜的衔接点（保持连贯的关键）",
      "audio_note": "此镜的声音（对白/旁白/音效）" }
  ],
  "shot_count": 0,
  "total_duration_sec": 0
}
```

## 关键规则
- 一场戏可拆多个镜头，**镜头数 = 时长需求 ÷ 单镜时长**，单镜电视觉疲劳控制在 3–6 秒。
- `characters` 只能引用已有 id。
- `continuity` 必须写——这是角色一致性与视觉连贯的核心字段（服装/光线/位置/朝向）。**跨镜角色外观必须与第5环定妆图一致**，出现"换装/换脸"式变化要在此显式标注（如"葫芦已发光，余温未散"）。
- **禁止同一镜头塞两个动作**：一镜一事。
- 景别要有节奏，禁止连续 3 个同景别。

## 不做的事
- 不写完整的图像生成提示词（那是 prompt 环节的活，此处只给画面描述）

## 自检
所有 characters id 合法；总时长与剧本 total_est_sec 偏差 ≤10%；无连续 3 个同景别。
