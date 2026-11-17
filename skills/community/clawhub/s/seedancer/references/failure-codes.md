> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 失败诊断错误码系统

> **定位**：机器可读、可复测的失败诊断层。
> **用法**：生成失败时，先按 §1 责任层决策树定位故障层，再用 §2 错误码命名问题，最后按 §3 复测规则最小化修复。
>
> 与 `references/qa-checklists.md` Part C 的关系：Part C 是**人读的视觉图鉴**（"这看起来像死脸"）；本文件是**机读的诊断词汇**（"这是 `F-PERFORMANCE`，责任层=动作与表演"）。两者互补：Part C 帮你看见问题，错误码帮你命名问题、追踪问题、复测修复。

---

## §1 责任层决策树（先定位，再修复）

**"结果不好"不是错误码。** 先描述可观察症状，再按以下顺序排查责任层：

| 顺序 | 责任层 | 排查内容 |
|---|---|---|
| 1 | **资产事实** | 角色身份、状态、数量、参考范围是否正确？ |
| 2 | **镜头契约** | open/close state、beat、人数、时长是否与分镜表一致？ |
| 3 | **主提示词表达** | 主体、空间、动作、摄影、声音、连续性是否完整且无冲突？ |
| 4 | **模型能力边界** | 视频/图像模型的能力边界与工具差异是否已感知？（如时长上限、画幅支持、参考图机制） |
| 5 | **生成随机性** | 同参数抽样差异？换种子是否改善？ |
| 6 | **后期** | 剪辑、调色、声音、点修是否引入了新问题？ |

**铁律**：任何层失败先修该层，不要默认在末尾堆否定词。

> 例：角色换脸（`F-ID-DRIFT`）→ 责任层大概率在 1（资产事实：descriptor 不完整或参考图未锚定），而不是在 3（提示词表达：加一堆"do not change face"）。

---

## §2 33 个错误码（六类）

### A. 资产与身份（5）

| 错误码 | 症状 | 最小修复 |
|---|---|---|
| `F-ID-DRIFT` | 脸/体型/发型/轮廓漂移 | 只保留批准身份与明确引用范围；descriptor 逐字注入 |
| `F-STATE-DRIFT` | 服装/伤势/湿度/携带物回退 | 引用正确状态版本，写 `must_hold` |
| `F-REF-SCOPE` | 参考的构图/背景/光线被带入 | 只继承需要属性，排除其余（"不继承构图/角度/色调"） |
| `F-DUP-SUBJECT` | 同一角色出现两次 | 精确人数、每个 ID 一次、针对反射风险 |
| `F-ASSET-MERGE` | 两角色/道具特征融合 | 分离资产注入、站位与接触边界 |

### B. 空间与连续性（6）

| 错误码 | 症状 | 最小修复 |
|---|---|---|
| `F-COUNT` | 人数错误/额外人物 | 写精确人数、ID 与各出现一次 |
| `F-SCREEN-DIR` | 屏幕方向/解剖左右翻转 | 同写摄影机侧、解剖侧、鼻尖方向 |
| `F-AXIS` | 越轴导致关系混乱 | 保持方向或设计可见越轴桥梁 |
| `F-SPATIAL-RESET` | 场景布局重构 | 引用场景区域和唯一锚点，排除参考构图 |
| `F-PROP-DUP` | 家具/关键道具复制 | 声明唯一物体及接触关系 |
| `F-CONTINUITY` | 动作/伤势/天气/声音接不上 | 对齐 continuity_in/out，登记变化 |

### C. 动作与表演（5）

| 错误码 | 症状 | 最小修复 |
|---|---|---|
| `F-ACTION-OVERLOAD` | 动作被压缩/遗漏/顺序错 | 删、并或拆镜 |
| `F-PHYSICS` | 漂浮/无重量/碰撞无反作用 | 补完整物理链（准备→接触→反作用→落定） |
| `F-ACTION-ORDER` | 结果先于触发 | 按时间写触发与动作阶段 |
| `F-PERFORMANCE` | 僵硬/过度/情绪不读 | 选视线、呼吸、停顿、重心中的少数信号 |
| `F-UNSCRIPTED-MOVE` | 静止角色自动转头/手势/说话 | 列允许微动与禁止动作 |

### D. 摄影与剪辑（6）

| 错误码 | 症状 | 最小修复 |
|---|---|---|
| `F-CAMERA-CONFLICT` | 多个主运镜互相争夺 | 只留一个主运动或拆镜 |
| `F-CAMERA-PATH` | 起点/路线/距离/落点错 | 写物理可走通的完整路径 |
| `F-FRAMING` | 景别/主体占比/方向错 | 用可画构图与占比替代"电影感" |
| `F-FOCUS` | 对焦错/随机漂移 | 只留一个主对象或一次明确拉焦 |
| `F-CUT` | 镜头数/切点/转场错 | 写精确数量、每段时长与切点 |
| `F-JITTER` | 手持变故障抖动 | 写人体幅度/节奏；冲击震动绑定事件并恢复 |

### E. 对白与声音（6）

| 错误码 | 症状 | 最小修复 |
|---|---|---|
| `F-DIALOGUE-TEXT` | 加词/漏词/说话者错 | 写精确文本、唯一发声窗口与说话者 |
| `F-DIALOGUE-TIME` | 台词太快/截断/挤掉动作 | 延长/缩短台词或拆镜 |
| `F-DIALOGUE-VISUALIZED` | 台词变闪回/额外人物 | 写对白不视觉化、当前允许集合 |
| `F-LIPSYNC` | 未说话者嘴动/口型错 | 只允许说话者在指定时间口型（仅适用于支持原生音频的模型：Kling 3.0 Omni / Veo 3） |
| `F-AUDIO-POLLUTION` | 自动音乐/旁白/字幕/无关声 | 保留指定轨道，禁额外音轨 |
| `F-AUDIO-MIX` | 人声/音效/底床优先级错 | 重排前景/中层/底床与 duck（仅适用于支持原生音频的模型） |

### F. 光色与材质（5）

| 错误码 | 症状 | 最小修复 |
|---|---|---|
| `F-LIGHT-DIR` | 光源换边/无来源 | 写真实来源、方向与人物关系 |
| `F-EXPOSURE` | 高光溢出/暗部压死 | 选必须保留的主体与范围 |
| `F-COLOR-DRIFT` | 主色/色温/强调色漂移 | 锁叙事色与跨镜变化事件 |
| `F-MATERIAL` | 皮肤/布/金属/骨全塑料化 | 分别写粗糙度、反射、透光、磨损 |
| `F-WEATHER` | 雨雪雾风像贴层 | 让天气作用于人物、地面、光、声音 |

---

## §3 复测规则（最小修复纪律）

1. **每次只改变一个主要责任层。**（与五条黄金规则 #3"一次只改一处"一致）
2. 写明 `changed_variables`、`hypothesis`、`expected_improvement`。
3. 列出必须保持的资产/动作/摄影/声音字段。
4. 用相同评审门比较上一次与本次结果。
5. **连续两次迭代无改善时停止同一路径**——换责任层或简化镜头（拆镜/删动作/换角度）。

> 迭代记录写入 `06-logs/iteration-log.md`，格式：
> ```
> 镜XXX · 迭代N
> - 错误码: F-ID-DRIFT
> - 责任层: 1 资产事实
> - changed_variables: descriptor 增加"broad jaw, scar above left eyebrow"
> - hypothesis: 缺少下颌与疤痕描述导致脸型漂移
> - expected_improvement: 脸型与参考图一致率从 6/10 提升至 9/10
> - 必须保持: 服装、站位、光照方向
> - 结果: [成功/失败/部分改善] — [说明]
> ```

---

## §4 与 Part C slop 图鉴的映射

`references/qa-checklists.md` Part C 的 14 条 slop 与本文件错误码的对应关系：

| Part C # | slop 缺陷 | 对应错误码 | 责任层 |
|---|---|---|---|
| 1 | 多余手指/肢体增生 | `F-MATERIAL` / `F-PHYSICS` | 5 随机性 → 6 后期 |
| 2 | 「沸腾」纹理 | `F-MATERIAL` | 3 提示词 → 5 随机性 |
| 3 | 假文字/招牌乱码 | `F-AUDIO-POLLUTION`（视觉版） | 3 提示词 |
| 4 | 死脸（无眼神光） | `F-PERFORMANCE` | 1 资产事实 |
| 5 | 换脸/换衣/身份漂移 | `F-ID-DRIFT` / `F-STATE-DRIFT` | 1 资产事实 |
| 6 | 人物瞬移/跳轴 | `F-AXIS` / `F-SPATIAL-RESET` | 2 镜头契约 → 3 提示词 |
| 7 | 塑料皮/对称脸 | `F-MATERIAL` | 3 提示词（违反点修改铁律） |
| 8 | 巨人缩水 | — （SCALE LAW 专属） | 3 提示词 |
| 9 | 群演数量失控 | `F-COUNT` | 3 提示词 |
| 10 | 多出人物/克隆家具 | `F-DUP-SUBJECT` / `F-PROP-DUP` | 3 提示词 |
| 11 | 自带配乐 | `F-AUDIO-POLLUTION` | 3 提示词 |
| 12 | 模型自创台词/尬笑 | `F-DIALOGUE-TEXT` / `F-UNSCRIPTED-MOVE` | 3 提示词 |
| 13 | 表演平/假 | `F-PERFORMANCE` | 3 提示词 → 1 资产事实 |
| 14 | 节奏拖沓 | `F-CUT` | 6 后期 |

> 注：Part C #8（巨人缩水）由 SCALE LAW 体系覆盖，不归入 33 错误码——SCALE LAW 是独立的尺度锁定机制，不是失败诊断。

---

## 使用示例

### 示例 1：角色换脸

**症状**：第 3 镜的角色脸与第 1 镜不一致。

**诊断流程**：
1. 责任层排查 → 层 1（资产事实）
2. 错误码命名 → `F-ID-DRIFT`
3. 最小修复 → 检查角色 descriptor 是否逐字注入；参考图是否锚定

**迭代记录**：
```
镜003 · 迭代2
- 错误码: F-ID-DRIFT
- 责任层: 1 资产事实
- changed_variables: 在 ACTIVE REFERENCES 中追加 "@mei 100% matches the reference"
- hypothesis: 缺少显式参考锚定导致模型自由发挥
- expected_improvement: 脸部一致率从 5/10 提升至 9/10
- 必须保持: 服装、站位、光照方向
- 结果: 成功 — 脸部一致率 9/10
```

### 示例 2：人物瞬移

**症状**：切镜后角色从画面左侧跳到右侧。

**诊断流程**：
1. 责任层排查 → 层 2（镜头契约）
2. 错误码命名 → `F-AXIS`
3. 最小修复 → 检查 GEO SPATIAL LAYOUT 是否锁定 180° 轴线；切镜后是否重述位置

**迭代记录**：
```
镜005 · 迭代1
- 错误码: F-AXIS
- 责任层: 2 镜头契约
- changed_variables: 在 GEO 中追加 "180° AXIS: camera ALWAYS stays on door side"；在 FIRST FRAME 中重述 "@mei at frame-LEFT, facing frame-RIGHT"
- hypothesis: 缺少轴线锁定导致摄影机越轴
- expected_improvement: 左右关系稳定
- 必须保持: 角色外观、动作、光照
- 结果: 成功 — 左右关系稳定
```

### 示例 3：死脸

**症状**：角色眼睛像玻璃珠，无生命感。

**诊断流程**：
1. 责任层排查 → 层 1（资产事实）
2. 错误码命名 → `F-PERFORMANCE`
3. 最小修复 → 在 Style Prefix 的 Acting 条款中追加 `wet living eyes with catch-lights`；在 CHARACTER ACTING 中描述眼生命

**迭代记录**：
```
镜007 · 迭代3
- 错误码: F-PERFORMANCE
- 责任层: 1 资产事实
- changed_variables: 在 STYLE 中追加 "wet living eyes with catch-lights"；在 CHARACTER ACTING 中追加 "eyes scan the room, blink rate slows as tension builds"
- hypothesis: 缺少眼生命描述导致死眼
- expected_improvement: 眼睛有生命感
- 必须保持: 脸部外观、光照
- 结果: 部分改善 — 眼睛有生命感但表情仍僵硬，下一迭代聚焦面部微表情
```

---

## 检查清单

生成失败时：

- [ ] 描述可观察症状（不用"结果不好"）
- [ ] 按责任层决策树排查（从层 1 到层 6）
- [ ] 用错误码命名问题
- [ ] 写明 `changed_variables`、`hypothesis`、`expected_improvement`
- [ ] 列出必须保持的字段
- [ ] 用相同评审门比较上一次与本次结果
- [ ] 连续两次迭代无改善时停止同一路径

---

**参考**：视觉图鉴详见 `references/qa-checklists.md` Part C；完整 16-block 架构详见 `references/cinedance-video-prompt.md`。


---

## §5 硬门类错误码（v6.0.0 新增；v9 从 SKILL.md 归位到此）

> 这 5 个码此前**只写在 SKILL.md 的失败现象对照表里**，本文件缺失
> （`REV-20261005-008` C-4）。v9 归位，使"诊断词汇"只有一处权威。

| 错误码 | 现象 | 根因 | 解法所在 |
| --- | --- | --- | --- |
| `F-DIALOGUE-CAPACITY` | 台词被压缩 / 语速不合理 | 未做台词容量预检 | `dialogue-capacity.md` |
| `F-GROUP-CONTINUITY` | 组尾不稳定 / 承接断裂 | 未遵守承接等式 | `grouping-density.md` |
| `F-DENSITY` | 密度不足 / 空档过长 | 未过镜头密度四道门 | `grouping-density.md` |
| `F-HIDDEN-CUT` | 隐藏切镜（单镜内多视点） | 违反"一镜一视点" | `grouping-density.md` |
| `F-SPATIAL-VAGUE` | 模糊方位 / 代词指代 | 未遵守空间与指代硬门 | `output-format.md` |

**合计**：6 类 + 5 个硬门码 = **38 个码**（v8.0.0 文档中"33 码"的计数已过时）。
