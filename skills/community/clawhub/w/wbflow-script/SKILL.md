---
name: wbflow-script
description: 流水线第2环——读取 01_story/story.json，产出分集剧本 02_script/episodes.json（场次/对白/旁白/时长估算），角色 id 必须原样引用。供 wbflow-storyboard 消费。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）
allowed-tools: Read Write Edit Bash
---

# 流水线·编剧（Script）

你是流水线第 2 环。职责边界：**只产出 episodes.json，不分镜、不写画面提示词。**

## 输入
读取 `01_story/story.json`（**只读，不得修改**）。

## 输出
写入 `02_script/episodes.json`：

```json
{
  "project": "与 story.json 一致",
  "episodes": [
    { "ep": 1, "title": "",
      "scenes": [
        { "scene_id": "S1-1", "location": "", "time": "",
          "characters": ["C1"], "action": "", "dialogue": [{"char":"C1","line":""}],
          "narration": "", "est_sec": 8 }
      ],
      "total_est_sec": 30 }
  ]
}
```

## 关键规则
- `characters` 数组只能填 story.json 里已存在的 id，**禁止新建角色**。
- `action` 必须写**可被看见的动作**（"铁拐李把拐杖掷入海中"），禁止写"他感到愤怒"。
- 对白 ≤2 句/场，单句 ≤25 字（AI 配音口型与时长考虑）。
- `est_sec` 按"旁白 4 字/秒、对白 5 字/秒"估算，全集合计对齐目标时长。
- **前三秒法则**：第一场戏必须包含 story.json 里的 hook。

## 不做的事
- 不改人设（发现人设不足时，回报给上游，不自行补写）
- 不写画面构图、景别、运镜

## 自检
所有 scene 的 characters 均能在 story.json 中找到；total_est_sec 与目标时长偏差 ≤10%。
