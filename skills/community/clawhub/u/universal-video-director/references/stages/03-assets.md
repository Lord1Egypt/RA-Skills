# 子技能 03 · 视觉设定与资产锁定 assets
**来源**：drama-skills 的 short-drama-assets（连戏锁 / 锁定词、换装造型、道具状态、角色声线）和 image-prompts（Lookdev 风格帧），shuohao novel-characters / novel-art / character-refs（正面全身锚点图、其余视角只参考锚点、无人空镜白板图、图片过期追踪）。

## 目标
让每个角色、场景、道具在所有镜头里看起来都是同一个，并且能直接拿来做参考图。

## 方法
1. **style_bible**：画风、色板、光线、镜头感、负面词。可以先出 2–3 张 lookdev 风格帧，让用户定调。
2. **锁定词（LOCK-*）**：跨镜头不变的外观，写成可以原样粘贴的短语，例如 `pine-green lapel service jacket`。规则：
   - 每条锁定词必须原样出现在该资产的 ref_prompt 里
   - 下游每个用到这个资产的首帧提示词里，也必须原样出现
3. **variants**：换装、受伤、湿身这类状态变化，用 `when` 和 `delta` 描述，不要另建一个资产。
4. **参考图层级**：
   - 角色先出 `anchor_full`（正面全身）
   - headshot、profile90、back、detail 只参考锚点图来生成
   - 场景出 `plate`（无人、无手的空镜）和各种状态图
   - 描述一改，就把对应参考图标为 `stale:true`，然后重出
5. **声线**：为每个角色写 voice.tts_voice 和 tts_prompt。
6. **关卡**：asset_approval=true 时，展示参考图，等用户确认，确认后标 `approved:true`。

## 常见错误码
CHAR_NO_ASSET、LOCK_NOT_IN_REF、REF_STALE、NO_ANCHOR（WARNING）
