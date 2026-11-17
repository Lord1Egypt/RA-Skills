---
name: wbflow-story
description: 流水线第1环——把一句话主题变成结构化故事大纲与人物设定，输出 01_story/story.json（含 characters[].id 全局唯一、世界观、集数规划）。供 wbflow-script 消费。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）
allowed-tools: Read Write Edit Bash
---

# 流水线·企划人设（Story）

你是流水线第 1 环。职责边界：**只产出 story.json，不写剧本、不分镜。**

## 输入
- `seed_theme`：一句话故事主题
- `episode_count`：集数（默认 1）

## 输出（严格契约，字段名不得改）
写入 `01_story/story.json`：

```json
{
  "project": "项目名",
  "seed_theme": "原始主题",
  "logline": "一句话故事线（≤40字，含主角+目标+阻碍）",
  "worldview": { "era": "", "place": "", "rules": "" },
  "characters": [
    { "id": "C1", "name": "角色名", "role": "主角/配角/反派",
      "identity_lock": "永久标识：任何景别下都必须能认出是谁（≤15字，1个强符号，如'腰悬朱红葫芦'）",
      "props_lock": "随情节可变的道具（如'左手铁拐'——掷出后即消失）",
      "appearance_lock": "identity_lock + props_lock 的合并串，供下游注入与定妆图生成",
      "personality": "一句话性格（要有冲突感）",
      "ref_image": "05_chars/C1.png（第5环定妆后回写，此处先留空）" }
  ],
  "episodes": [ { "ep": 1, "title": "", "hook": "前3秒情绪炸点", "beats": ["", ""] } ],
  "style_guide": { "art_style": "", "palette": [], "forbidden": [] }
}
```

## 关键规则
- **`characters[].id` 是本流水线的主键**——后续 script/storyboard/prompt 全部引用同一 id，任何环节不得新建或改写。
- `appearance_lock` 必须是可直接粘贴进图像提示词的短语（≤30字，含发型/服饰/配色/标志性道具）。
- **必须区分两类特征**（2026-10-21 实测教训）：
  - `identity_lock`＝永久标识（葫芦、扇子、青鳞）：任何景别都要在，是校验的硬指标；
  - `props_lock`＝可变道具（铁拐、三叉戟）：会随剧情消失，**允许下游缺失**。
  早期版本要求"每个镜头注入全部锁定词"，导致远景被迫塞满细节、画面变差。**分级后契约才可用。**
- `hook` 必须能在 3 秒内被看见或听见，禁止心理描写。
- `style_guide.forbidden` 至少写 2 条（如"禁止现代物品""禁止文字水印"），下游环节必须遵守。

## 不做的事
- 不写完整对白（那是 script 的活）
- 不决定镜头（那是 storyboard 的活）
- 不生成图片

## 自检
输出前确认：每个 character 有 id、appearance_lock、personality；每集有 hook；forbidden 非空。
