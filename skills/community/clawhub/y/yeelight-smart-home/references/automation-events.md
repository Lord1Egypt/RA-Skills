# Automation Event Reference

Use this reference when creating, explaining, diagnosing, or planning automation rules.

## Canonical Events

- 有人移动
- 无人移动
- 2分钟无人移动
- 5分钟无人移动
- 10分钟无人移动
- 20分钟无人移动
- 30分钟无人移动
- 有人移动且环境亮度低于指定值
- 门卡已插入
- 门卡已取出
- 门窗已打开
- 门窗已关闭
- 门窗打开后超1分钟未关闭
- 照度上升至
- 照度下降至
- 光照度上升至
- 光照度下降至
- 有人移动且照度上升至
- 有人移动且照度下降至
- 无人移动且照度上升至
- 无人移动且照度下降至
- 有人靠近
- 有人远离
- 持续一段时间有人
- 持续一段时间无人

## Condition Device Guidance

- Human presence, motion, contact, illuminance, button, and knob events are valid candidates only after Runtime confirms the entity and capability.
- Time windows, duration, threshold, target room, and action device must be explicit or returned as the smallest clarification question.
- The following device words are not enough for an automation condition unless Runtime confirms an installed entity and supported event/capability: 温控器、全景屏、窗帘、开合帘、卷帘、梦幻帘、电机、电源、驱动、模块、模组。
- Normalize event wording to the canonical event list before planning. Examples: 人来/有人经过 -> 有人移动; 没人/无人 -> 无人移动; 门磁打开 -> 门窗已打开; 光线变暗 -> 照度下降至.
- Conditions and actions are different. If an unsupported device appears as a condition, remove or downgrade only that condition; do not remove the same device when it is merely an action target and Runtime supports that action.
- If a requested event implies missing hardware, never create a live sensor silently. For new lighting design imports, you may add a clearly labeled design slot or installer recommendation only when the user asked for design materialization; for real automation execution, ask for or rely on Runtime-verified existing sensor capability.
- For full-home lighting design materialization, map missing trigger hardware before deciding rule feasibility: motion/presence/no-motion events imply a presence or motion sensor slot; door/window events imply a contact sensor slot; illuminance events imply an illuminance-capable sensor slot; button/knob gestures imply a control-surface slot. Keep these as design notes/recommendations unless the user explicitly asked to include future slots.
- When multiple condition types appear together, keep trigger-like conditions (`alarm`, `event`, `fact_change`) in the trigger group and state checks (`fact`) in the fact group. Do not put `fact` rows into the trigger group.

## Automation Recipe Templates

Use these as planning patterns only. Runtime still validates target entities, capability support, time windows, limits, and write policy.

| Template | Trigger | Action | Constraints |
| --- | --- | --- | --- |
| 玄关迎宾灯 | 门窗已打开 + 晚间时间窗 | 玄关灯 60-80% 暖白，数分钟后恢复或关闭 | 需要门磁和玄关灯能力；避免全天触发 |
| 走廊人来灯亮 | 有人移动 + 夜间或低照度 | 走廊路径灯 20-35% 暖光，无人后关闭 | 动作范围限制到走廊；不要驱动全屋 |
| 卫生间人来灯亮 | 有人移动 | 卫生间 60-80% 中性白，5-10 分钟无人后关闭 | 无人时长不能太短，避免洗澡中误关 |
| 客厅日落补光 | 照度下降至阈值 + 有人在家 | 客厅缓升到 50-60% 3500K | 加防抖，避免云层变化频繁触发 |
| 深夜起夜灯 | 夜间 + 有人移动 | 路径灯 5-8% 暖光，5 分钟后关闭 | 禁止主灯和冷白；优先沿途灯 |
| 儿童房睡前仪式 | 固定晚间时间 | 20-30 分钟缓降亮度和色温 | 不加入彩光；让用户确认作息时间 |
| 全屋离家 | 离家时间窗 + 全屋无人 | 执行离家场景并关闭必要设备 | 双因子确认；不要只靠一个传感器 |
| 开窗节能 | 门窗已打开 | 关闭同房间空调或新风 | 空调新风能力必须验证；恢复逻辑单独确认 |
| 晨间唤醒链 | 工作日或周末定时 | 卧室渐亮，随后走廊和厨房亮起 | 需要明确日期规则和每阶段目标 |
| 防盗模拟有人 | 离家期间固定时间点 | 指定房间交替亮灯和熄灯 | 不宣称随机；用多个固定时间点模拟变化 |
| 客厅离家回家 | 手动情景或到离家状态 | 回家时入口到客厅逐步点亮；离家时客厅到入口逐步关闭 | 优先创建场景；自动触发需要明确传感器、时间窗或成员状态证据 |
| 主卧定时亮灯 | 每天 09:00 定时 | 主卧灯组或指定灯具缓亮到 50-70% 暖中性白 | 如果只是照明设计导入，可先作为设计自动化元数据；真实自动化需 Runtime 验证目标和时间规则 |

## Design Patterns

| Pattern | Use | Rule |
| --- | --- | --- |
| 双因子确认 | 离家、安防、节能类自动化 | 时间窗、无人、门窗、照度等至少两个独立条件共同约束大范围动作。 |
| 时间窗口限定 | 人感、照度、门磁触发 | 同一触发在白天、晚间、深夜应有不同动作或不动作。 |
| 防抖窗口 | 门磁、光照突变、按钮重复触发 | 短时间内重复触发应被合并或忽略，避免闪烁和乒乓。 |
| 范围最小化 | 房间和路径照明 | 传感器所在房间优先，不把局部触发扩大为全屋控制。 |
| 手动覆盖优先 | 所有自动化 | 用户手动调整后短时间内不要被自动化立即改回。 |
| 回滚保障 | 开窗节能、临时安全巡视 | 能恢复原状态才承诺恢复；不能恢复就只提出独立关闭或提醒。 |

## Anti Patterns

| Anti-pattern | Risk | Correction |
| --- | --- | --- |
| 单传感器直驱全屋 | 误触发影响过大 | 限制到传感器所在房间或增加第二条件。 |
| 时间盲信 | 季节和天气变化导致体验差 | 优先加入照度或人在条件；没有传感器时明确是定时近似。 |
| 短循环或乒乓 | A 触发 B，B 又反向触发 A | 加入防抖、时间窗或合并为一条规则。 |
| 过度自动化 | 用户难以理解和维护 | 单房间保留少量核心自动化，推荐季度审查。 |
| 没有退出路径 | 用户无法手动覆盖 | 保留物理开关、面板或手动场景优先级。 |
| 把设计槽位说成真实设备 | 用户误以为设备已经配网、在线或可控制 | 允许创建照明设计槽位；同时明确槽位只是云端设计占位，真实控制仍需设备入网和 Runtime 证据。 |
| 缺传感器就创建真实传感器 | 虚构自动化触发条件或污染家庭配置 | 只能把传感器列为设计槽位或采购建议；真实自动化触发必须由 Runtime 验证已存在的传感器能力。 |

## Persistent Rule Policy

- Creating or updating automation is persistent configuration and must go through Runtime execution after caller-side user confirmation when needed.
- Do not create a rule from an inferred habit, complaint, or one-time preference.
- Do not auto-add real sensors or paired devices when a template needs missing hardware. For whole-home lighting design, missing lights may become design slots through lighting.design.import; missing triggers remain design metadata or recommendations until Runtime verifies real sensors.
- Do not claim random timing, dynamic sunset, manual override recovery, air-conditioning control, audio playback, or panel/knob binding unless Runtime returns explicit support.
- If Runtime returns blocked, clarification_required, or a write-verification mismatch, explain the returned reason and keep any unexecuted proposal as local guidance.
- Never invent background trigger behavior, gateway synchronization behavior, or execution success.
