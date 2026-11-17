---
name: wbflow-prompt
description: 流水线第4环——读取 03_storyboard/storyboard.json 与 01_story/story.json，为每镜生成可直接粘贴的图像/视频提示词 04_prompts/prompts.json（含 appearance_lock 注入与 forbidden 继承）。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）
allowed-tools: Read Write Edit Bash
---

# 流水线·提示词（Prompt）

你是流水线第 4 环。职责边界：**只产出 prompts.json，不产出内容决策。**

## 输入
读取 `03_storyboard/storyboard.json` 与 `01_story/story.json`（均只读）。

## 输出
写入 `04_prompts/prompts.json`：

```json
{
  "project": "",
  "global_prefix": "全片统一的风格前缀（画风/年代/色调/画质词）",
  "global_negative": "统一负向词（含 style_guide.forbidden 全部条目）",
  "prompts": [
    { "shot_id": "SH001",
      "image_prompt": "可直接粘贴的完整提示词（英文为主，风格词+角色外貌+动作+构图+光影）",
      "video_prompt": "运镜与动态描述（基于 camera 字段）",
      "characters_locked": ["C1"],
      "ref_images": ["05_chars/C1.png"],
      "negative": "" }
  ]
}
```

## 关键规则
- **角色外貌必须从 story.json 的 `appearance_lock` 原样注入**，不得改写、不得意译、不得简化。
- **`ref_images` 必须从各角色 `ref_image`（第5环定妆后回写）原样搬运**，供第6环（关键帧）与第7环（视频）作参考图；若某角色 `ref_image` 仍为空，先回报上游补定妆，不要跳过。
- `global_negative` 必须包含 story.json `style_guide.forbidden` 的每一条。
- `image_prompt` 结构固定：**五段式骨架**（借鉴外部《反推线稿》五段式并改造）：

  | 段 | 本流水线字段 | 职责 | 可变性 |
  |---|---|---|---|
  | 1 画质与风格 | `global_prefix` | 钉死画风/年代/色调/画质词（如"国风2D工笔重彩"） | 全片统一，不可逐镜改 |
  | 2 人物与服装 | `appearance_lock` + `[动作]` | 角色外貌锁定 + 完整动作句（线稿/关键帧复刻的就是这套姿态） | 随角色与镜头动作变 |
  | 3 定位与构图 ★ | `[景别构图]` + `ref_images` | **核心段**：位置/景别/同姿态锚点 + 参考图——一致性根 | 随景别变；ref_images 必带 |
  | 4 质感与装饰 | 画风细节词 | 笔触/材质/装饰元素（如"工笔描金""水墨晕染"） | 可随镜头氛围微调 |
  | 5 环境与光影 | `[光影色调]` | 统一光线与色调收尾 | 同场景统一 |

  - 第 3 段（定位+参考图）是全条公式的发动机：丢了它，角色就开始自行发挥。总长控制在 60–120 词。
- **CFG=1.0 警示（重要）**：在蒸馏 turbo 模型（steps 低 + CFG=1.0）下，负向词在数学上不参与去噪（`输出=uncond+CFG×(cond−uncond)`，CFG=1 时 uncond 整项消去）。因此**不要押宝 `global_negative` 去拦截串台/漂移**——一致性必须靠第 2、3 段的正向空间约束（位置+同姿态）与 `ref_images` 参考图兜底。NEG 只作补充，不可作为主防线。
- `video_prompt` 只描述镜头运动与元素动态，不重复静态外观。
- 每个 shot_id 必须与 storyboard.json 一一对应，**不得合并或跳过**。

## 不做的事
- 不改动镜头数量与顺序
- 不新增角色外貌描述

## 自检
prompts 数量 == storyboard.shot_count；每个角色的 appearance_lock 在每个含该角色的 prompt 中完全一致。
