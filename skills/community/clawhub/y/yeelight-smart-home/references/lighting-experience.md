# Lighting Experience Reference

Use this reference for ambience, lighting design, scene planning, and mood translation.

## Design Rules

- Treat recipes as candidate guidance, not executable truth.
- Apply only properties that Runtime validates on the target entities.
- Temporary ambience can use Runtime-reviewed control intents; persistent scenes, automations, groups, and device settings use direct Runtime execution after any caller-side confirmation.
- Prefer warm, low-brightness, slow transitions for rest and sleep. Prefer neutral or cooler task light for focus and reading.
- Avoid colorful or dynamic effects when the user dislikes color effects, asks for sleep, or asks for low stimulation.
- Decode subjective language into intent, activity, time, room role, intensity, and constraints before choosing any parameter.
- Current-turn instructions override saved preferences; explicit dislikes override recipes and weak behavior signals.

## Scene Recipes

| Recipe | Guidance |
| --- | --- |
| 回家模式 | brightness=80-100; colorTemperature=4000-4500; transitionSeconds=3-5; behavior=入口到室内逐步点亮; intent=建立到家的安全感和欢迎感 |
| 离家模式 | brightness=0; transitionSeconds=2-5; behavior=从室内到入口逐步关闭; intent=让离开前的全屋状态可感知 |
| 日常模式 | brightnessMax=80; colorTemperature=3500-4000; transitionSeconds=0-3; intent=全天候不刺眼不缺光的平衡状态 |
| 会客模式 | brightnessMax=100; colorTemperature=4500; transitionSeconds=0-3; intent=明亮、清爽、面部观感自然 |
| 清洁模式 | brightness=100; colorTemperature=5000-5700; transitionSeconds=0-1; intent=提高辨识度和阴影可见性 |
| 午后休憩 | brightness=40-60; colorTemperature=3000-3500; transitionSeconds=600-1800; behavior=逐步降亮降色温; intent=浅休息，不突然进入睡眠 |
| 黄昏过渡 | brightnessRamp=80_to_30; colorTemperatureRamp=4000_to_2700; transitionSeconds=1800; intent=模拟日落，平滑进入晚间状态 |
| 深夜归家 | brightness=15-25; colorTemperature=2700; transitionSeconds=5-8; behavior=只开路径灯; intent=不惊扰家人，保留行走安全 |
| 阅读模式 | brightness=70-85; colorTemperature=4000-5000; stripColorTemperature=2700; stripBrightness=30; intent=任务光清晰，背景光降低对比疲劳 |
| 书房专注 | brightness=80-90; colorTemperature=4500-5500; backgroundBrightnessMax=40; intent=桌面高辨识度，环境不过度刺激 |
| 儿童作业 | brightness=85-100; colorTemperature=4000-5000; backgroundBrightnessMax=50; intent=桌面充足照明，环境光消除阴影 |
| 品茗模式 | brightnessMax=80; colorTemperature=3000-4000; transitionSeconds=300; intent=温润、低压、适合交谈 |
| 瑜伽冥想 | brightness=30-50; colorTemperature=2700-3000; transitionSeconds=300-600; behavior=地面或间接光优先; intent=低重心柔光，引导放松 |
| 烛光晚餐 | brightness=10-40; colorTemperature=2200-2700; behavior=餐桌重点，环境极低; intent=保留餐桌焦点和亲密氛围 |
| 浪漫模式 | brightness=30-60; colorTemperature=3000; stripBrightness=20; transitionSeconds=5-30; intent=柔和包围感，不喧宾夺主 |
| 观影模式 | mainLight=off_or_low; backgroundBrightnessMax=20; colorTemperature=2700-3500; intent=降低屏幕与环境亮度差 |
| 沉浸观影 | mainLight=off; backgroundBrightnessMax=8; colorTemperature=2700; behavior=屏幕后方偏光优先; intent=最大化画面沉浸且保护眼睛 |
| 游戏模式 | brightness=30-60; colorTemperature=4000; stripBrightness=20; intent=降低屏幕眩光，保持反应清醒 |
| 聚会模式 | brightness=80-100; colorTemperature=4000; stripBrightnessMax=30; intent=活跃、明亮、不过度彩光化 |
| 派对模式 | brightness=60-80; colorTemperature=3500-4500; color=allowed_if_supported; effect=allowed_if_supported; intent=娱乐氛围；必须尊重彩光偏好和设备能力 |
| 睡前准备 | brightnessRamp=60_to_25; colorTemperatureRamp=3500_to_2700; transitionSeconds=1800; intent=比睡眠更早的生理过渡 |
| 睡眠模式 | brightness=5-10; colorTemperature=2700; delayedOffSeconds=300; intent=最后微光，短延迟后关闭 |
| 夜灯模式 | brightness=5-10; colorTemperature=2700; intent=方位参考，不干扰睡意 |
| 起夜模式 | brightness=5-8; colorTemperature=2200-2700; delayedOffSeconds=300; behavior=只开沿途灯; intent=保护暗适应和伴侣睡眠 |
| 早安唤醒 | brightnessRamp=5_to_70; colorTemperatureRamp=2700_to_3500-4000; durationMinutes=1-15; intent=模拟日出，温和唤醒 |
| 周末慵懒 | brightnessRamp=10_to_50; colorTemperatureRamp=2700_to_3200; durationMinutes=15; intent=比工作日更慢的唤醒节奏 |
| 安全巡视 | brightness=50; colorTemperature=4000; delayedOffSeconds=120; intent=短时看清环境，不长期耗电 |
| 节电模式 | brightness=current_60_percent; colorTemperature=keep; transitionSeconds=0-3; intent=保留可用照明，降低功耗 |

## Mood Recipes

| Expression | Guidance |
| --- | --- |
| 放松 | brightness=30-50; colorTemperature=2700-3200; transition=slow; reason=降低视觉刺激总量 |
| 睡前 | brightness=5-25; colorTemperature=2200-2700; avoid=color_dynamic_effect/cool_white; reason=保护褪黑素节律 |
| 专注 | brightness=70-90; colorTemperature=4000-5500; reason=提升警觉度和辨色能力 |
| 阅读 | brightness=70-85; colorTemperature=4000-5000; priority=local_task_light; reason=任务光清晰，环境光降低眩光 |
| 观影 | brightness=5-20; mainLight=off_or_low; backgroundLight=low_ambient; reason=缩小屏幕和环境亮度差 |
| 聚餐 | brightness=40-70; colorTemperature=2700-3500; priority=dining_table; reason=食物和面孔更自然 |
| 起床 | brightness=gradual_up; colorTemperature=3500-4000; reason=模拟自然光唤醒 |
| 夜间起身 | brightness=5-8; colorTemperature=2200-2700; duration=short; reason=只满足行走安全 |
| 派对 | color=enabled_if_supported; effect=dynamic_if_supported; requiresPreference=color_allowed; reason=娱乐向，必须尊重偏好 |
| 有点累 | mapsTo=放松; brightness=lower; colorTemperature=warmer |
| 太刺眼 | brightness=lower_to_below_50; colorTemperature=warmer_by_500K; transition=soft |
| 太暗了 | brightness=raise_to_70-80; priority=main_or_task_light |
| 太冷了 | colorTemperature=warmer_by_800-1000K; brightness=slightly_lower |
| 不舒服或头疼 | brightness=20-30; colorTemperature=2700; avoid=color/dynamic_effect; transition=slow |
| 焦虑或烦躁 | brightness=30-40; colorTemperature=warm; transition=very_slow |
| 刚运动完 | brightness=50-60; colorTemperature=4000; avoid=very_warm_high_brightness |
| 想有氛围一点 | mapsTo=浪漫模式 |
| 困了 | mapsTo=睡前准备 |
| 开心或兴奋 | brightness=70-80; colorTemperature=natural; askBefore=party_or_color_effect |
| 无聊 | brightness=slightly_raise; askBefore=switch_scene |

## Compound Scene Flows

Use these only when the user asks for a multi-step ritual, routine, or design plan. Applying a flow requires separate Runtime-supported scene or automation plans.

| Flow | Sequence | Use |
| --- | --- | --- |
| 晚安仪式 | 日常模式 -> 睡前准备 -> 睡眠模式 -> 夜灯模式 | 适合用户要求晚上逐步放松或固定睡前流程 |
| 周末早晨 | 早安唤醒 -> 周末慵懒 -> 日常模式 | 适合不想被强光或闹钟突然叫醒的周末 |
| 居家电影夜 | 黄昏过渡 -> 观影模式 -> 沉浸观影 -> 夜灯模式 | 适合从傍晚自然切换到电影氛围 |
| 聚会全流程 | 日常模式 -> 聚会模式 -> 派对模式 -> 品茗模式 -> 夜灯模式 | 适合有客人到访、活动高潮和散场收尾 |
| 瑜伽冥想 | 日常模式 -> 瑜伽冥想 -> 品茗模式 | 适合从活动到静心的光线节奏 |

## Lighting Design Principles

| Principle | Detail | Guardrail |
| --- | --- | --- |
| 分层照明 | 环境光提供基础照度，任务光服务活动，重点光突出墙面、柜体或装饰。 | 不要用一个顶灯承担所有需求。 |
| 先结构后效果 | 完整家庭设计按房间和区域、设备槽位、同类分组、情景、自动化的顺序组织。 | 不要在未确定空间归属时先保存情景或自动化。 |
| 设计槽位优先 | 用户尚未安装设备但要求设计落地时，可以创建可审计的设备槽位并附产品身份与设计说明。 | 不要回答不能创建槽位；也不要宣称槽位已配网、在线或可实时控制。 |
| 产品约束优先 | 颜色、安装方式、光束角、开孔、形状、系列、功率和能力标签是选品硬线索。 | 不要只按最高分候选或模糊品类随便选。 |
| 睡眠保护 | 睡前和夜间优先 2200-2700K、低亮度、慢渐变。 | 不主动使用冷白、彩光或动效。 |
| 任务优先 | 阅读、厨房、清洁、手工优先提高任务面照度和中性白光。 | 不要把全屋都调成高亮冷白，先限定目标区域。 |
| 观影偏光 | 主灯关闭或极低，屏幕后方保留弱背景光。 | 避免屏幕周边强光和正面反射。 |
| 夜间缓升 | 夜间任何明显提亮都应使用缓亮。 | 避免 40% 以上亮度突跳。 |
| 彩光克制 | 彩光只用于娱乐、派对或用户明确偏好。 | 有负偏好、睡眠、观影、放松时默认不用彩光。 |
| 空间限定 | 用户说路径、桌面、餐桌、沙发时，应把动作限定到相关目标。 | 不要把局部需求扩大成全屋控制。 |
| 能力实证 | 任何亮度、色温、RGB、渐变、窗帘、联动能力都必须由 Runtime 验证。 | 产品词和营销词不是执行证据。 |

## Memory And Preference Policy

- Negative preferences can adjust future recommendations only after Runtime memory policy allows it.
- A single complaint such as "太亮了" is current-turn feedback unless the user explicitly asks to remember it.
- Strong phrases such as "以后默认", "记住", "别再", or "我不喜欢" should be structured by the Skill and saved through `memory.remember` before changing future defaults.
- Repeated corrections are a reason for the Skill to ask whether to remember a preference; Runtime will not infer subjective preferences or return implicit candidates.
- Explain proposed lighting results in user language; do not expose internal recipe fields unless asked for technical detail.
