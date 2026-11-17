> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# JSON API 输出模式（JSON API Output Mode）

> 来源：skill_cn.md（Seedance 2.0 导演技能）
> 用途：定义 Seedance 提示词的结构化 JSON 输出格式，确保双语（EN+ZH）生产级输出

---

## 一、输出格式规范

### 基本结构

输出为包含**两个对象**的 JSON 数组：EN 提示词和 ZH 提示词。

```json
[
  {"lang":"en","prompt":"..."},
  {"lang":"zh","prompt":"..."}
]
```

### 硬性规则

| 规则 | 说明 |
|------|------|
| 仅输出 JSON 数组 | 无解释、无 markdown 代码块 |
| 首尾字符 | `[` 开头，`]` 结尾。`[` 前和 `]` 后无任何文本 |
| 对象顺序 | 先 EN 后 ZH |
| 中文 = 母语改写 | 非翻译。中文 ≤ 1,800 字符 |
| 无元数据 | 无镜头标签、无每镜时长、无内部元数据 |

---

## 二、双语提示词结构 — 5 个分节标签

提示词为一段连续字符串，内嵌分节标签。五个分节按顺序排列：

### 分节标签列表

| # | EN 标签 | ZH 标签 | 内容 | 可否裁剪 |
|---|---------|---------|------|---------|
| 1 | `Style & Mood:` | `风格与氛围：` | 色板、光线、镜头、氛围 | 不可跳过，至少保留 1 句 |
| 2 | `Narrative Summary:` | `叙事概要：` | 一句话场景描述 | 中文预算紧张时优先删除 |
| 3 | `Dynamic Description:` | `动态描述：` | 逐镜散文式描述。摄影机、运动、动作。现在时 | 不可完全删除 |
| 4 | `Static Description:` | `静态描述：` | 场景、道具、环境细节 | 中等优先级裁剪 |
| 5 | `Audio:` | `音频：` | 台词 + 音效/BGM（仅对话场景） | 仅对话场景需要 |

### 分节标签格式

中英文标签内嵌在连续字符串中：

```
Style & Mood: [色板/光线/镜头/氛围]. Narrative Summary: [一句话]. Dynamic Description: [逐镜散文]. Static Description: [场景/道具/环境]. Audio: [台词/音效].
```

中文版本：

```
风格与氛围：[色板/光线/镜头/氛围]。叙事概要：[一句话]。动态描述：[逐镜散文]。静态描述：[场景/道具/环境]。音频：[台词/音效]。
```

---

## 三、中文 1800 字符上限规则

### 裁剪优先级（接近上限时按此顺序裁剪）

1. **叙事概要**（Narrative Summary）— 先删
2. **静态描述**（Static Description）— 次删
3. **风格与氛围**（Style & Mood）— 至少保留 1 句
4. **动态描述**（Dynamic Description）— **不可完全删除**

### 字符估算经验值

- 1 句中文 ≈ 40-60 字符
- 如英文动态描述超过 10 句 → 编写中文前预先裁剪
- 硬上限 = 1,800 字符

---

## 四、图片引用系统（Image Reference System）

### 引用方式

| 类型 | 触发条件 | 处理方式 |
|------|---------|---------|
| **显式引用** | 用户写 `<<<image_1>>>` | 图片与场景角色直接关联 |
| **隐式引用** | 用户附带图片但无标签 | 视觉分析并匹配场景元素 |

### 输出规则

- 在第一个分节标签前输出图例
- 初次提及用描述性标签 `(<<<image_n>>>)`
- 之后仅用标签 `<<<image_n>>>`

### 示例

```
<<<image_1>>>: 穿深灰风衣的中年男性，面部有旧伤疤
<<<image_2>>>: 废弃工厂内部，锈钢铁架

Style & Mood: ... Dynamic Description: A man (<<<image_1>>>) walks through the factory (<<<image_2>>>)...
```

---

## 五、反垃圾词汇表（Anti-Spam Vocabulary — 禁用）

### 英文禁用词

| 类别 | 禁用词 |
|------|--------|
| 通用吹捧 | breathtaking, stunning, captivating, mesmerizing, awe-inspiring |
| 工艺赞美 | masterfully, meticulously, exquisitely, beautifully crafted |
| 宏大形容 | cinematic masterpiece, visual feast, a symphony of |
| 流畅性 | seamlessly, effortlessly, flawlessly |
| 技术buzz | cutting-edge, state-of-the-art, next-level, groundbreaking |
| 文学性 | rich tapestry, vibrant tapestry, kaleidoscope of |
| 动作动词 | elevate, unlock, unleash, harness |
| 总结性 | a testament to, speaks volumes, resonates deeply |

### 中文禁用词

| 类别 | 禁用词 |
|------|--------|
| 感叹类 | 令人叹为观止, 令人惊叹, 令人着迷 |
| 工艺类 | 精心打造, 匠心独运, 独具匠心 |
| 视觉类 | 视觉盛宴, 光影交响, 完美呈现 |
| 体验类 | 极致体验, 引人入胜, 震撼人心 |
| 融合类 | 巧妙融合 |

### 替代策略

- 用**具体的视觉描述**替代抽象赞美
- 用**物理行为**替代情绪标签
- ✅ "jaw clenches, nostrils flare" ❌ "looks angry"
- ✅ "松针铺地，风吹树枝" ❌ "空气中有松木香"

---

## 六、语言规则

### 通用规则

| 规则 | 说明 |
|------|------|
| 时态 | 现在时、主动语态 |
| 风格 | 生动但精炼。无诗意填充。具体的视觉指导 |
| 中文 | 母语导演笔记，来自中国摄影师。自然句式、四字格、电影术语 |
| 角色名 | 保持一致。无名角色用功能性标签 |
| 对话 | 以原语言呈现，不翻译 |
| 镜头标签 | 无 "Shot 1:"、"Beat 2:" — 将转场织入散文 |
| 输出语言 | 不论输入语言，均输出 EN + ZH |

### 角色年龄盲规则（关键）

两种语言均**不按年龄**描述角色。

**需要替换以提升模型理解的词**（**不用于规避安全策略**）：
- EN: boy, girl, child, kid, young, teen, little
- ZH: 男孩, 女孩, 孩子, 少年, 少女, 小孩, 年轻

**替代方案**：
- **有图片输入时**：用角色（骑手、身影、旅者）、服装和动作描述
- **无图片输入时**：用功能性标签 "a figure in a wool cloak" / "披羊毛斗篷的身影"

---

## 七、资产清单提取规则

### 从用户文本/图片中提取

| 资产类型 | 提取内容 |
|---------|---------|
| 角色 | 姓名、外貌、服装、显著特征 |
| 场景 | 室内/室外、主要建筑、光线 |
| 道具 | 任何明确提及或展示的事物 |
| 风格/氛围 | 色板、对比度、光线、天气、时间 |

### 创造规则

- ❌ 绝不凭空创造用户未提供的角色、场景或道具
- ✅ 可以添加环境细节（尘土、火花、大气颗粒）和摄影机行为
- ⚠️ 例外：当用户请求暗示**场景创作**而非改编时（如"想一个战斗场景"），可创造辅助元素

---

## 八、输入解析规则

### 从用户文本中提取

| 字段 | 提取逻辑 |
|------|---------|
| 场景类型 | 判断是动作、通用还是对话（或混合）→ 决定使用哪套原型 |
| 时长 | 如有提及，遵从。如未提及，默认 10 秒。硬上限：15 秒 |
| 摄影机 | 如用户指定 → **必须**出现在最终提示词中，中英文均需。**用户摄影机指令覆盖所有默认值** |

---

## 九、Seedance 2.0 引擎硬性约束

| 规则 | ✅ 正确 | ❌ 错误 |
|------|--------|--------|
| 动作节拍 = 意图 + 命名技法 | "spinning back kick connects" | "左前臂外旋45°格挡腕部右侧冲拳" |
| 描写力量和方向，不描写破坏过程 | "driven into the car, metal buckling" | "thrown into side door, glass shatters, uses rebound to sweep leg" |
| 剪辑后重新锚定位置和面向 | 每镜标注位置和方向 | 剪辑间空间连续性断裂 |
| 离框 = 隐含剪辑 | 角色出框 → 消失 | 同一镜头内编排离框+重入 |
| 画外 = 不存在 | 状态变化先在镜头中呈现 | 提及镜头外事件 |
| 避免反光镜头 | 不写刀刃/水坑/镜子反光 | Seedance 渲染反光时场景地理出错 |
| 只描述可见或可听之物 | "松针铺地，风吹树枝" | "空气中有松木香" |
| 微表情以物理方式描述 | "jaw clenches, nostrils flare" | "looks angry" |

---

## 十、剪辑规则

### 双重对比（强制）

每次剪辑必须**同时**改变景别和摄影机模式。

**景别尺度**：极远景 → 远景 → 中景 → 中近景 → 近景 → 特写

**摄影机模式**：手持摄影 | 固定/锁死 | 稳定跟拍 | 摇臂升降 | 航拍/无人机

剪辑时不得重复任一维度。

### 插入镜头规则

- 插入镜头 = 亚秒级（0.3-0.5 秒）戏剧性标点
- **因果动机**：观众必须理解为何看到此细节
  - ✅ 英雄被摔到引擎盖上 → **他的**手紧握金属
  - ❌ 通用靴子踩入水坑
- **标注主体**：指定 Whose 的身体部位/细节

---

## 十一、摄影机语言速查

| 类别 | EN | ZH |
|------|-----|-----|
| 角度 | low-angle, high-angle, dutch angle, bird's-eye, worm's-eye, eye-level, OTS | 仰拍, 俯拍, 荷兰角, 鸟瞰, 蚁视角, 平视, 过肩镜头 |
| 焦距 | wide 14-24mm, standard 35-50mm, telephoto 85-200mm, macro | 广角, 标准, 长焦, 微距 |
| 运动 | tracking, dolly-in, dolly-out, crane, pan, tilt, whip-pan, orbit, push-in, pull-back, handheld, Steadicam, aerial | 跟拍, 推镜头, 拉镜头, 摇臂升降, 横摇, 纵摇, 甩镜头, 环绕, 推进, 后拉, 手持摄影, 斯坦尼康, 航拍 |
| 时间 | slow-motion, speed ramp, freeze frame | 升格, 变速, 定格 |
| 转场 | smash cut, match cut, whip-pan transition, hard cut, L-cut | 硬切, 匹配剪辑, 甩镜转场, 直切, L型剪辑 |

---

*文档版本：v7.0.0 | 来源归属：skill_cn.md（Seedance 2.0 通用导演技能）*
