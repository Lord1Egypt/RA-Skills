# Seedance Combat Director v3

> 为 [Seedance 2.5](https://www.bytedance.com/) 设计的通用动作 / 打斗视频提示词导演技能。  
> 覆盖徒手格斗、武器对决、一对多、团队连携、Boss 战、追逐战、现代动作、武侠、奇幻、科幻、动画 / CG 等场景。

**English summary** — Seedance Combat Director v3 is a director-style skill for designing, diagnosing, continuing, and rewriting combat / action prompts for Seedance 2.5. It enforces a strict "no brief, no prompt" workflow, requires evidence-based diagnosis from real generated footage, and ships a combat-pattern library, intake contract, brief template, and a JSON validator so every prompt is built on a complete Combat Brief rather than improvised assumptions.

---

## 核心原则

**No Brief, No Prompt.** 信息不齐就**只**输出缺失项询问，不出草稿、不替用户做决定、不默认时长画幅。

证据优先。 修改成片时，必须先实际查看视频证据，不得凭历史对话或旧提示词推断。

具体规则参见 [`SKILL.md`](./SKILL.md) 第 0 节和第 14 节（最终质检 Gate）。

---

## 适用场景

| 场景 | 是否支持 | 说明 |
| --- | --- | --- |
| 新生成打斗 / 动作提示词 | ✅ | 默认入口 |
| 修改已有成片 | ✅ | 必须提供视频 + 用户最不满意的点 |
| 续接已有片段 | ✅ | 必须读取源视频末段实际状态 |
| 参考某视频节奏重写 | ✅ | 参考视频必须可访问 |
| 徒手格斗 / 武器对决 / 一对多 / 团队连携 / Boss 战 / 追逐战 | ✅ | 模块化加载，见 [`references/combat-patterns.md`](./references/combat-patterns.md) |
| 武侠 / 奇幻 / 科幻 / 动画 CG | ✅ | 视觉媒介可换，动作规则不变 |
| 文生图 / 非动作类视频 | ❌ | 不在范围内 |

---

## 仓库结构

```
seedance-combat-director-v3/
├── SKILL.md                  # 技能主文档（必读）
├── README.md                 # 本文件
├── references/
│   ├── intake-contract.md    # 必要输入门槛（硬字段 / 软字段）
│   ├── combat-patterns.md    # 通用战斗结构库（9 个编排模块）
│   └── research-notes.md     # 公开案例摘要与抽象方法
├── templates/
│   └── brief.md              # 用户可填写的 Combat Brief 模板
└── scripts/
    └── validate_brief.py     # JSON 形态 Brief 的完整性校验脚本
```

---

## 快速开始

### 1. 填写 Combat Brief

复制 [`templates/brief.md`](./templates/brief.md) 到本地，按字段填齐。**必填项缺一不可**：

- 任务类型（新生成 / 修改成片 / 续接 / 参考重写）
- 时长（秒）
- 画幅（16:9 / 9:16 / 4:3 / 1:1）
- 人物资产与角色映射（或明确"允许文字设计"）
- 战斗关系与结局 / 目标
- 场景（或"由你设计"）
- 战斗方式（或"由你设计"）
- 节奏 / 摄影方向（或"由你设计"）

把 Brief 整理成 JSON 后，运行校验脚本：

```bash
python scripts/validate_brief.py brief.json
# 输出 COMPLETE  → 可以发给 Agent 生成提示词
# 输出 INCOMPLETE: <缺失字段> → 补齐后再发
```

校验脚本只检查**字段是否齐备**，不评判创作质量，也不替你决定 Seedance 接口能力。

### 2. 交给 Agent

把完整 Brief + 素材（参考图 / 源视频）一起发给 Agent。Agent 会：

1. 建立内部 Combat Brief（Format / Reference Manifest / Combatants / Geography / Goal / Tempo / Camera / Escalation / Continuity Locks / Audio）；
2. 按当前任务加载 [`references/combat-patterns.md`](./references/combat-patterns.md) 中需要的模块；
3. 按时长分段写战斗功能和摄影目标；
4. 输出可直接复制到 Seedance 的 `text` 代码块。

### 3. 成片修改的额外流程

修改已有成片时，**先看视频**，再写提示词。流程见 [`SKILL.md`](./SKILL.md) 第 10.3 节：

1. 全片建立时间轴概览；
2. 对问题段加密检查；
3. 只报告实际可见现象；
4. 形成"时间范围 → 问题 → 改写策略"；
5. 保留成功部分，只针对失败原因改。

无法访问视频时，明确说明无法完成基于成片的诊断，不凭旧提示词猜。

---

## 工作流概览

```
用户输入（素材 + 文字）
        │
        ▼
   intake-contract.md   ── 硬字段是否齐？ ── 否 ──► 只输出缺失项询问
        │ 是
        ▼
   内部建立 Combat Brief
        │
        ▼
   加载 combat-patterns.md 所需模块
        │
        ▼
   时长分段 → 战斗功能 + 摄影目标 + 退出状态
        │
        ▼
   最终质检 Gate（SKILL.md §14）── 不通过 ──► 回询问或重写
        │
        ▼
   输出可复制的中文 text 代码块
```

---

## 战斗模式库（节选）

完整版本见 [`references/combat-patterns.md`](./references/combat-patterns.md)。

| 编号 | 模式 | 核心约束 |
| --- | --- | --- |
| 1 | Grounded Duel 写实单挑 | 距离、接触、双方主动权变化 |
| 2 | Weapon Duel 武器对决 | 武器长度 / 握法 / 攻击距离前后一致 |
| 3 | One vs Many 一对多 | 远景维持人数压迫，近景只让少数主要接触 |
| 4 | Team Combo 团队连携 | 必须有"A 制造条件 → B 利用条件"因果 |
| 5 | Boss Fight 强敌 | Boss 至少有两种不同性质的反制 |
| 6 | High-VFX Fantasy 高特效奇幻 | VFX 放大动作，不替代动作 |
| 7 | Chase Combat 追逐战 | 每个动作交换改变追逐状态 |
| 8 | Entrance Beat 重要角色登场 | 在动作中识别身份，不是远景黑影 |
| 9 | Finisher 终结 | 机会 → 通道 → 接触 → 即时结果 |

---

## 与"普通动作提示词模板"的区别

| 一般模板 | 本技能 |
| --- | --- |
| 用户说一句就开始写 | 硬字段不齐就只问不写 |
| 默认 30 秒、16:9、24fps | 全部不默认，逐项确认 |
| 招式名堆砌 | 每个关键交换要求 威胁 → 路径 → 接触 → 反馈 → 下一动作 |
| 主角无伤连招 / 对手是木桩 | 双方都要主动；允许并要求明显的优势变化 |
| 切镜后位置 / 方向 / 动量丢失 | 高速硬切必须继承动量、屏幕方向、接触关系、受伤状态 |
| Boss 只是巨型沙袋 | Boss 至少有两种不同性质的有效反制 |
| VFX 越多越好 | VFX 来源绑定角色 / 武器，不替代接触 |
| 结尾蓄力展示 / 持续发光 | 终结必须立即产生结果（击倒 / 脱战 / 死亡 / 逃脱 / 开放结局） |
| 改稿只看旧提示词 | 必须先实际查看成片，只针对证据改 |
| 直接复用参考视频的角色 / 招式 | 只继承抽象节奏方法，不复制具体人物 / 招式 / IP |

冲突优先级：**用户当前明确要求 > 当前素材事实 > 当前成片 / 参考视频实际证据 > 本技能的创作建议 > 社区案例经验。**

---

## 学习边界

可以从公开案例（如 lansenai、Strength04_X 等）中提取**抽象方法**，例如：

- 参考素材需要明确分工；
- 高速动作必须保持位置、方向和动量；
- 关键接触需要物理反馈；
- 强敌必须具有能动性；
- 时间段应有明确战斗功能和退出状态。

**不**把某个案例的角色颜色、武器、寺庙、雨夜、时长、画幅、镜头数、慢动作比例等保存成新任务默认值。  
**不**把社区案例参数（如 "4K""24fps"）误写成 Seedance 官方硬限制。

公开案例仅是经验来源，不是模型保证。摘要与原始链接见 [`references/research-notes.md`](./references/research-notes.md)。

---

## 脚本依赖

`scripts/validate_brief.py` 仅使用 Python 标准库（`json`, `sys`），无需 `pip install`。

---

## 贡献

欢迎提交 Issue / PR 改进以下方面：

- 新的战斗模式（请同时给出**抽象方法**而非复制具体案例）；
- Brief 模板字段扩展；
- 校验脚本的更严格检查；
- 公开案例的**方法级**摘要（不要直接搬运原提示词正文）。

**禁止**把社区案例的具体人物、招式、场景、画幅、时长作为新任务默认。

---

## 许可

本仓库的具体许可证由仓库所有者决定。如未声明，默认视为仅供学习与个人使用，商用前请联系作者。

---

## 相关链接

- [`SKILL.md`](./SKILL.md) — 技能主文档
- [`references/intake-contract.md`](./references/intake-contract.md) — 输入门槛
- [`references/combat-patterns.md`](./references/combat-patterns.md) — 战斗结构库
- [`references/research-notes.md`](./references/research-notes.md) — 案例摘要
- [`templates/brief.md`](./templates/brief.md) — Brief 模板
- [`scripts/validate_brief.py`](./scripts/validate_brief.py) — JSON 校验脚本