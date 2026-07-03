# Scene Recipes

Use this reference for converting user mood words into objective scene or design-import actions. For broader ambience principles and compound flows, also load `references/lighting-experience.md`.

## Objective Conversion

Convert mood words before `scene.create`, `scene.update`, or `lighting.design.import`.

- 回家: entrance/path first, then living areas; 3500-4500K, 70-90%, short staggered delay.
- 离家: turn off target room/home lights; use orderly ranks or small delays when helpful.
- 清洁: 5000-5700K, 90-100%, direct and functional.
- 日常/会客: 3500-4500K, 60-85%, low glare.
- 观影: main light off or 5-15%, background/accent 2700-3200K, avoid screen glare.
- 阅读/学习: task target 4000-5000K, 70-85%; ambient lower.
- 品茗: 3000-4000K, no more than 80%, soft transition and low visual pressure.
- 聚会: 4000K, 80-100%, keep strip or accent lights below roughly 30% unless the user asks for stronger ambience.
- 睡眠/夜灯: 2700K, 5-15%, no color/dynamic effect by default.
- 早安: gradual warm wake, 2700K toward 3500-4000K, brightness from 5-10% toward 60-70% when transition support exists.
- 派对/浪漫: color/effects only when the user allows it and Runtime/product evidence supports it.

## Naming And Update Rules

- Keep scene names meaningful and at most 14 Chinese characters when possible.
- If a duplicate name is required in the same home, append a small sequence instead of inventing an unrelated name.
- For `scene.update`, call `scene.detail.get` first when possible and resend the complete `actions[]`.
- Use `references/payload-shapes.md` for action row shape, light parameters, and read-modify-write rules.

## Lighting Design Import Scenes

In `lighting.design.import`, scenes use `actions[]` with `targetType`, `targetKey`, and `set`. The `targetKey` must refer to a room, device slot, group, scene, or home key from the same import model.

```json
{
  "key": "living-home",
  "name": "客厅回家模式",
  "actions": [
    {
      "targetType": "group",
      "targetKey": "living-grille-group",
      "targetName": "客厅格栅灯组",
      "rank": 0,
      "set": {
        "power": true,
        "brightness": 70,
        "colorTemperature": 3500
      }
    }
  ]
}
```
