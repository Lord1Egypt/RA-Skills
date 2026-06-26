# skill-evolve-pro — 技能进化引擎（Phase 1 + Phase 2）

> **版本**：Phase 1 + Phase 2  
> **基于**：SkillOpt / ReflACT 6步循环  
> **目标**：让 AI 技能像神经网络一样，通过"失败轨迹 → 反思 → 编辑 → 验证"自动进化

---

## 技能概述

- **名称**：skill-evolve-pro
- **类型**：自动化技能优化（类 ReflACT 框架）
- **描述**：对指定技能执行完整的 6 步进化循环，从失败轨迹中提取改进信号，生成原子编辑patch，应用并验证，最终输出进化后的技能版本。
- **关键词**：`进化`、`优化 skill`、`自动改进`、`失败轨迹`、`技能迭代`
- **阶段**：Phase 1（核心引擎 + 轨迹加载器）+ Phase 2（SESSION-STATE 轨迹捕获）

---

## 触发条件

**用户确认优先于直接执行**：Gate 审核完必须用户确认后才能执行修改，同意/确认才写入，拒绝则丢弃本次编辑。

**diff 展示环节**：在更新技能文件之前，必须先向用户展示修改内容的 diff 对比（包括新增/修改的段落）。必须等用户确认，回复「确认改」才写入。

| 触发话术 | 说明 |
|---------|------|
| 「进化一下 XXX skill」 | 对指定技能执行完整6步 |
| 「优化这个技能」 | 同上 |
| 「让技能自动进化」 | 同上 |
| 「执行 skill-evolve」 | 同上 |
| 「运行进化流程」 | 同上 |
| 「evolve XXX」 | 英文触发 |

> **Phase 1 限制**：用户需手动提供失败轨迹文件（JSON格式，放在 `temp/` 目录），暂不支持全自动 rollout 评测。

**diff 展示环节**：在更新技能文件之前，必须先向用户展示修改内容的 diff 对比（包括新增/修改的段落）。必须等用户确认是否覆盖原文件，用户确认后回复「确认改」才写入。

---

## 6步循环流程（核心）

```
┌─────────────────────────────────────────────────────────────┐
│                    ReflACT 6-Stage Pipeline                  │
│                                                             │
│  ① Rollout   ② Reflect   ③ Aggregate   ④ Select           │
│       ↓          ↓           ↓            ↓                  │
│  采集轨迹   错误分析    聚类合并      重要性排序            │
│                                                             │
│  ⑤ Update(Skill)   ⑥ Meta-Reflect                          │
│        ↓                 ↓                                   │
│  应用编辑patch      评估验证                               │
│       ↓                                                   │
│  ⑦ Slow Update（跨epoch纵向优化，保护慢更新区）               │
└─────────────────────────────────────────────────────────────┘
```

---

### Step ① Rollout — 轨迹采集

**用户确认环节**：应用编辑补丁到文档之前，必须先向用户展示要修改的内容摘要，必须等待用户确认后才执行

**用户确认环节**：在应用编辑补丁到文档之前，必须先向用户展示要修改的内容摘要（包括修改类型、目标位置和修改内容）。必须等待用户确认（回复「同意」或「确认」），确认后才执行修改。

**输入**：`temp/` 目录下的失败轨迹 JSON 文件  
**处理**：读取轨迹，记录每条任务的 `hard`(通过/失败)、`soft`(置信度)、`fail_reason`  
**输出**：`RolloutResult` 列表

**文件格式**（用户放置）：
```
temp/
  failed_trajectory_001.json
  failed_trajectory_002.json
  ...
```

每条轨迹 JSON 需包含字段：`id`, `task_description`, `question`, `fail_reason`, `predicted_answer`, `reference_text`

**决策点**：如果 `temp/` 为空，提示用户放入失败轨迹文件后再继续。

---

### Step ② Reflect — 错误分析与反思生成

**输入**：RolloutResult 列表  
**处理**：调用 DeepSeek API，对失败轨迹进行错误分类，生成 `ReviseSuggestions`（修改建议），每条建议包含：
- `type`：建议类型（add_rule / modify_step / fix_context / rewrite_section）
- `title`：简短标题
- `instruction`：具体修改指令
- `priority_hint`：优先级（high/medium/low）
- `support_count`：该建议来自多少条失败轨迹的支持

**输出**：`RawPatch`（含 `patch.edits` 列表）

**API 调用**：
```
model: deepseek-v4-pro
base_url: https://api.deepseek.com
```

---

### Step ③ Aggregate — 聚类合并

**输入**：多个 RawPatch（可能来自不同批次的失败轨迹）  
**处理**：
- 按 `support_count` 降序排序
- 合并相同类型/目标的建议（避免重复编辑）
- 去重后输出合并后的 `Patch`

**输出**：`Patch`（含 `edits` 列表 + `reasoning`）

---

### Step ④ Select (Clip) — 重要性排序与编辑预算选择

### 停止机制
- **最大轮次限制**：每个进化周期最多执行 N 轮（Round 0-5），达到上限后自动停止，等待下一版本或人工干预
- **改善检测**：每轮比较 edits 与上一轮的重复度，若连续两轮相同或无改善则停止，输出最终报告

**输入**：`Patch`（大量 edits）+ 当前技能文档 + `max_edits`（编辑预算）  
**处理**：
- 如果 edits 数量 ≤ `max_edits`：直接透传
- 如果 edits 数量 > `max_edits`：调用 optimizer LLM 对 edits 排名，选出 top-L（类比梯度裁剪，控制有效步长）

**输出**：`Patch`（已裁剪至 `max_edits` 条编辑）

**调度器**（LRScheduler）：
| 模式 | 行为 |
|------|------|
| `constant` | 固定编辑预算（如 max_edits=8）|
| `linear` | 线性衰减（max→min）|
| `cosine` | 余弦退火（max→min）|
| `autonomous` | 无限制，模型自决 |

### 用户确认流程
1. **展示修改摘要**：向用户展示本次将修改的内容类型、目标位置和内容概要
2. **等待用户同意**：用户回复「同意」或「确认」后继续，「拒绝」则丢弃本次编辑
3. **执行写入**：确认后写入文件，输出最终报告

---

### Step ⑤ Update (Skill) — 应用编辑 patch

**输入**：当前技能文档 + `Patch`  
**处理**：依次应用 4 种原子编辑操作：

| 操作 | 说明 | 示例 |
|------|------|------|
| `append` | 在文档末尾追加内容 | 新增一整块规则 |
| `insert_after` | 在指定目标文本后插入 | 在某步骤后插入新子步骤 |
| `replace` | 替换一段目标文本 | 修改已有指令措辞 |
| `delete` | 删除目标文本 | 移除冗余/错误段落 |

**慢更新保护区**：
- 标记：``
- 保护区内容**不受 Step ⑤ 编辑影响**，仅在 Slow Update 阶段由 optimizer 改写
- `append` 操作若命中保护区，插入保护区之前

**输出**：新的技能文档 + 每步编辑的执行报告

---

### Step ⑥ Meta-Reflect — 元反思与验证

**输入**：新技能文档 + 失败轨迹（用于对比）  
**处理**：快速检查新技能是否解决了已知的失败模式  
**决策点**：
- 若关键失败模式已修复 → 进化成功，输出新技能
- 若关键失败模式仍存在 → 记录未解决问题，进入下一轮循环

---

### Step ⑦ Slow Update — 跨 Epoch 纵向优化（Epoch 级别）

> 此步骤在多个进化 epoch 之后执行，非每个循环都触发

**输入**：上一 epoch 的技能 + 当前 epoch 技能 + 两轮 rollout 对比结果  
**处理**：
- 构建对比表：improved / regressed / persistent_fail / stable_success
- 优先处理 **regressed**（正确→错误的退化）
- 然后处理 **persistent_fail**（持续失败）
- optimizer 分析后生成自由格式的指导文本
- 将指导文本写入技能的 `` 内的内容不受 Step ⑤ 编辑影响
2. **编辑预算上限**：默认 `max_edits=8`，防止一次性大幅修改
3. **用户确认**：Phase 1 进化结果需用户确认后才覆盖原技能文件

---

## 使用示例

```
用户：进化一下 copywriting skill

Agent：
  1. 检查 temp/ 目录，找到 failed_trajectory_*.json
  2. 加载轨迹 → Reflect（生成修改建议）
  3. Aggregate（聚类合并去重）
  4. Select（按重要性选 top-8 编辑）
  5. Update（应用编辑到技能文档）
  6. 输出：进化后的技能文档（用户确认后生效）
```

---

## Phase 2: SESSION-STATE 轨迹捕获

### 概述
Phase 2 新增从 `SESSION-STATE.md` 自动解析失败轨迹的能力，不再依赖用户手动放置 JSON 文件。

### SESSION-STATE.md 期望格式
```markdown
## Outcomes
- hard_success: true
- soft_score: 0.9
- fail_reason: ""
- task_description: "用户要求生成 skill-evolve-pro 蓝图文档"
```

### 核心数据结构：RolloutResult
```python
@dataclass
class RolloutResult:
    id: str                    # 唯一标识，如 "rollout_20260603_001"
    skill_id: str              # 技能ID
    task_type: str             # 任务类型：search/tool_use/persona/decision
    task_description: str      # 任务描述
    user_message: str          # 用户原始消息
    predicted_answer: str      # AI 预测的回答
    reference_answer: Optional[str]  # 参考答案
    hard: float               # 硬指标：1.0=通过，0.0=失败
    soft: float               # 软指标：置信度 0.0~1.0
    fail_reason: Optional[str]  # 失败原因
    feedback: Optional[str]    # 用户反馈内容
    timestamp: str             # 执行时间 ISO格式
    metadata: dict            # 其他元数据
```

### Phase 2 模块

| 文件 | 说明 |
|------|------|
| `scripts/rollout_result.py` | RolloutResult 数据类定义 |
| `scripts/session_state_parser.py` | SESSION-STATE.md 解析器 + 失败检测 |
| `scripts/trajectory_loader.py` | Phase 2 新增 `load_from_session_state()` + `save_rollout_result()` |

### Phase 2 新增接口

```python
# 从 SESSION-STATE.md 解析失败轨迹
def load_from_session_state(session_state_path: str) -> List[RolloutResult]

# 保存单条 RolloutResult 到 JSON
def save_rollout_result(result: RolloutResult, output_dir: str = "temp/rollouts") -> str

# 统一加载入口
def load_all_rollouts(
    session_state_path: Optional[str] = None,
    json_dir: Optional[str] = None,
) -> List[RolloutResult]
```

### 失败检测规则
1. 用户纠正了AI的错误（"路径不对"、"芯片型号错了"）
2. AI执行失败（工具调用报错）
3. 用户说了"不是"或"重来"
4. 任务状态含 ❌ / 失败 / 错误

### 硬/软指标判定

| 场景 | hard | soft |
|------|------|------|
| 用户问题完全解决 | 1 | 1.0 |
| 部分解决（有遗留） | 0 | 0.5-0.9 |
| 解决但有副作用 | 0 | 0.3-0.7 |
| 完全没解决 | 0 | 0.0 |

---

## 未来扩展（Phase 3+）

- [x] Phase 1: 核心引擎 + 轨迹加载器 ✅
- [x] Phase 2: SESSION-STATE 轨迹捕获 ✅
- [x] Phase 3: skill_reflect.py 反思生成 ✅
- [x] Phase 4: skill_ap

### 用户确认流程
1. **展示修改摘要**：向用户展示本次将修改的内容类型、目标位置和内容概要
2. **等待用户同意**：用户回复「同意」或「确认」后继续，「拒绝」则丢弃本次编辑
3. **执行写入**：确认后写入文件，输出最终报告

ply.py 四种原子操作 ✅
- [x] Phase 5: skill_gate.py 验证门控 ✅
- [x] Phase 6: skill_scheduler.py 调度器 ✅
- [x] Phase 7: slow_update.py 月度guidance ✅
- [ ] 全自动 Rollout 评测
- [ ] 多技能并行进化
- [ ] 进化历史可视化（diff 对比）
- [ ] 进化质量评分（基于通过率提升）

---

*最后更新：2026-06-03 · Phase 1-7 全部完成*

<!-- SLOW_UPDATE_START -->
<!-- SLOW_UPDATE_START -->
## Long-Term Guidance (Epoch 1)

### Core Principles
1. **结构性优先**：优先使用 `replace` 和 `rewrite_section` 操作，直接修改技能核心逻辑，避免仅追加边缘规则。
2. **聚焦高频失败**：分析失败轨迹中重复出现的 `fail_reason`（如“上下文缺失”、“步骤顺序错误”），针对性地重写相关步骤。
3. **验证驱动**：每次编辑后必须通过至少一条失败轨迹的验证，确保修复有效。
4. **拒绝低效编辑**：若编辑预算有限，优先选择 `support_count` 最高的建议，拒绝低优先级（priority_hint=low）的修改。

### Persistent Failure Modes to Address
- 技能无法处理多步推理任务，需增加中间检查点。
- 对模糊输入缺乏鲁棒性，需添加输入预处理规则。
- 输出格式不一致，需强制标准化。

### Edit Strategy
- 每轮至少应用1条 `replace` 操作，修改最关键的失败步骤。
- 避免连续多轮无编辑（如Round 3-4），若gate=PASS但无编辑，应主动生成高impact建议。
- 记录每次编辑的验证结果，用于后续epoch的对比分析。
<!-- SLOW_UPDATE_END -->
<!-- SLOW_UPDATE_END -->

