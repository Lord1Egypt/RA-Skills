# Lighting Experience Reference

Use this reference for ambience, lighting design, scene planning, and mood translation.

## Design Rules

- Treat recipes as candidate guidance, not executable truth.
- Apply only properties that Runtime validates on the target entities.
- Temporary ambience can use Runtime-reviewed control intents; persistent scenes, automations, groups, and device settings require a pending plan.
- Prefer warm, low-brightness, slow transitions for rest and sleep. Prefer neutral or cooler task light for focus and reading.
- Avoid colorful or dynamic effects when the user dislikes color effects, asks for sleep, or asks for low stimulation.

## Scene Recipes

| Recipe | Guidance |
| --- | --- |
| 回家模式 | brightness=80-100; colorTemperature=4500; behavior=全屋灯光由近及远逐步点亮 |
| 离家模式 | behavior=全屋灯光从门口由远及近逐步关闭 |
| 清洁模式 | brightness=100; colorTemperature=5700 |
| 日常模式 | brightnessMax=80; colorTemperature=3500-4000 |
| 会客模式 | brightnessMax=100; colorTemperature=4500 |
| 品茗模式 | brightnessMax=80; colorTemperature=3000-4000 |
| 聚会模式 | brightness=80-100; colorTemperature=4000; stripBrightnessMax=30 |
| 观影模式 | mainLight=off_or_low; backgroundBrightnessMax=20; colorTemperature=2700-3500 |
| 阅读模式 | brightness=80; colorTemperature=4000-5500; stripColorTemperature=2700; stripBrightness=30 |
| 浪漫模式 | brightness=50-80; colorTemperature=3000; stripBrightness=20 |
| 睡眠模式 | brightness=5-10; colorTemperature=2700; delayedOffSeconds=300 |
| 夜灯模式 | brightness=5-10; colorTemperature=2700 |
| 早安模式 | brightnessRamp=5-10_to_70; colorTemperatureRamp=2700_to_3500-4000; durationMinutes=1-10 |

## Mood Recipes

| Expression | Guidance |
| --- | --- |
| 放松 | brightness=low_to_mid; colorTemperature=warm; transition=slow |
| 睡前 | brightness=very_low; colorTemperature=warm; avoid=color_dynamic_effect |
| 专注 | brightness=mid_to_high; colorTemperature=neutral_or_cool |
| 阅读 | brightness=mid; colorTemperature=not_too_cool; priority=local_task_light |
| 观影 | brightness=low; mainLight=off_or_low; backgroundLight=low_ambient |
| 聚餐 | brightness=mid; colorTemperature=warm; priority=dining_table |
| 起床 | brightness=gradual_up; colorTemperature=natural_light |
| 夜间起身 | brightness=very_low; colorTemperature=warm; duration=short |
| 派对 | color=enabled_if_supported; effect=dynamic_if_supported; requiresPreference=color_allowed |
| 有点累 | mapsTo=放松 |
| 太刺眼 | brightness=lower; colorTemperature=warmer |
| 想有氛围一点 | mapsTo=浪漫模式 |

## Memory And Preference Policy

- Negative preferences can adjust future recommendations only after Runtime memory policy allows it.
- A single complaint such as "太亮了" can become a candidate preference, not an automatic persistent device change.
- Explain proposed lighting results in user language; do not expose internal recipe fields unless asked for technical detail.
