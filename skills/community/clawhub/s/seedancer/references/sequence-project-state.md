# 序列项目状态管理 (Sequence Project State)

> 当项目超过单次生成时长，进入序列项目管理。
> 项目状态是真相之源；提示词是为一次生成编译的临时指令。
> 参考 `model-mechanics.md` 机制 5：误差复合。

---

## 运营模型

用户想法 → 故事脊椎 → 世界与连续性圣经 → 序列计划 → 当前镜头合约 → 当前镜头提示词 → 生成素材 → 观察素材评审 → 典律调和 → 下一镜头合约 → 下一提示词。

**全局计划，局部生成。观察实际结果。更新典律。从实际接受素材续接。**

---

## 典律状态分离

保持**典律**（不可变）和**瞬态**（可变）状态分离。

### 典律参考（控制身份和不可变设计）

- 角色身份
- 产品身份
- 服装
- 产品几何
- 持久道具
- 地点
- 批准的参考标签

### 接受的素材（控制瞬态开头状态）

- 姿势
- 动作阶段
- 屏幕位置
- 镜头阶段
- 环境布局
- 音频阶段
- 开放运动
- 未完成手势

---

## 必需项目字段

至少包含：

| 字段 | 说明 |
|------|------|
| `project_id` | 项目唯一标识 |
| `project_mode` | 单镜头/序列项目 |
| `surface` | 目标平台 |
| `clip_budget_sec` | 每镜头目标时长 |
| `prompt_budget` | 提示词预算（字数） |
| `story` | 故事字段（目标/结局/节拍） |
| `world_bible` | 世界与连续性圣经 |
| `reference_registry` | 参考标签注册表 |
| `beats` | 有序节拍列表 |
| `clips` | 镜头列表（含状态） |
| `take_history` | 生成历史 |
| `current_clip_id` | 当前镜头 ID |
| `canon_revision` | 典律版本号 |
| `updated_at` | 最后更新时间 |

### 故事字段

- `logline`：一句话故事
- `story_promise`：故事承诺
- `objective`：故事目标
- `initial_condition`：初始条件
- `final_outcome`：最终结局
- `target_duration_sec`：目标总时长
- `tone`：基调
- `medium`：媒介（实拍/动画/混合）

### 节拍字段

- `beat_id`：节拍唯一标识
- `description`：节拍描述
- `narrative_function`：叙事功能
- `status`：状态（计划中/当前/已完成/省略/替换）
- `assigned_clip_id`：分配的镜头 ID
- `dependencies`：依赖关系

### 镜头字段

- `clip_id`：镜头唯一标识
- `parent_clip_id`：父镜头 ID（续接来源）
- `sequence_index`：序列索引
- `prompt_version`：提示词版本
- `generation_mode`：生成模式（T2V/I2V/V2V/R2V/FLF2V/Edit/Extend）
- `source_clip_tag`：源素材标签
- `status`：状态（待生成/生成中/评审中/已接受/已拒绝）
- `narrative_job`：叙事任务
- `already_happened`：已发生内容
- `this_clip_only`：本镜头内容
- `reserved_for_later`：后续保留内容
- `planned_start_state`：计划开头状态
- `planned_end_state`：计划结尾状态
- `observed_start_state`：观察开头状态（实际）
- `observed_end_state`：观察结尾状态（实际）
- `continuity_locks`：连贯性锁定
- `allowed_changes`：允许变化
- `continuity_breaks`：连贯性破坏
- `accepted_deviations`：接受的偏差
- `transition_in`：过渡进入
- `transition_out`：过渡出去
- `open_motion_vectors`：开放运动矢量
- `handoff_requirements`：交接要求
- `extension_depth`：续接深度（警告：>=2 时风险增加）

---

## 视觉状态

只追踪重要的，不编造不清楚的细节。

### 角色

- 典律身份 ID
- 服装
- 发型
- 世界中的位置
- 画面中的位置
- 姿势
- 动作阶段
- 情绪状态
- 注视方向
- 视线
- 行进方向
- 速度
- 身体朝向

### 道具

- 身份
- 所有者
- 位置
- 状态
- 运动
- 交互状态

### 环境

- 地点
- 地理
- 背景布局
- 时间
- 天气
- 氛围
- 持久实用元素

### 镜头

- 景别
- 高度
- 角度
- 支撑
- 路径
- 方向
- 速度
- 运动阶段
- 主体关系
- 焦点状态
- 曝光状态
- 端点

### 光照

- 主光方向
- 强度
- 色彩关系
- 实用光源
- 过渡状态

### 音频

- 氛围
- 已完成对白
- 活动对白
- 音乐阶段
- 音效阶段
- 活动引擎或环境音
- 音频参考所有权

### 开放运动

- 主体方向和速度
- 镜头方向和速度
- 运动道具
- 未完成手势
- 布料或头发跟随
- 车辆运动
- 待恢复冲击

### 观察质量

- `observation_confidence`：观察置信度
- `uncertainties`：不确定性
- `requires_user_confirmation`：是否需要用户确认

---

## 调和

当接受的镜头与计划不同时：

1. **记录偏差**
2. **决定**：接受为典律/修复/拒绝重生成/重新锚定下一镜头
3. **如果接受**，更新下游计划
4. **移除**任何意外完成的节拍
5. **携带**任何未完成的计划节拍到下一个合适的镜头
6. **永远不要**假装计划的结局发生了（当它没有发生时）

**拒绝的素材不改变典律，不能作为续接父素材。**

---

## 项目状态胶囊

跨会话续接用可读胶囊。新会话不能被假设有隐藏的先验记忆。

必需字段：

```
PROJECT ID:
STORY GOAL:
FINAL OUTCOME:
SURFACE:
REFERENCE TAGS:
CANONICAL REFERENCES:
ACCEPTED CLIPS:
CURRENT ACTUAL STATE:
OPEN MOTION:
COMPLETED BEATS:
NEXT CLIP JOB:
CONTINUITY LOCKS:
ALLOWED CHANGES:
RESERVED FUTURE BEATS:
EXTENSION DEPTH:
UNRESOLVED UNCERTAINTIES:
```

---

## 核心洞察

**实际观察覆盖计划状态**——这是序列项目的铁律。

**典律与瞬态分离**——身份锁定（典律），姿势位置可变（瞬态）。

**误差复合**（机制 5）——续接深度 >=2 时警告，考虑重新锚定。

**拒绝素材不更新典律**——防止错误传播。

---

> 🎬 **Seedancer v3.0.0** — 全局计划，局部生成，观察实际，更新典律。