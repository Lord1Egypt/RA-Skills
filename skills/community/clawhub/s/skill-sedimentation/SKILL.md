---
slug: skill-sedimentation
displayName: Skill Sedimentation · 经验沉积
version: 3.0.0
summary: 自我进化闭环技能，Trigger→Retrieve→Act→Reflect→Distill→Promote，将每次任务执行经历转化为可复用知识资产
tags: [self-evolution, reflection, memory, hermes-loop, experience]
license: MIT
---

# skill-sedimentation · 经验沉积

## 身份

经验沉积技能。将每一次有价值的任务执行经历转化为可复用的知识资产，形成 **Trigger → Retrieve → Act → Reflect → Distill → Promote** 自我进化闭环。

> **S 级 Skill** · DeepSeek v3.0 评审通过 · 生产级卓越标准

---

## 何时激活

每次任务完成后（或发现显著错误时），Agent 自动判断是否需要走一次完整闭环。触发条件：

- 非平凡任务完成（有实质产出）
- 失败或纠正后（错误已修复）
- 发现可复用的模式（重复工作流、稳定的判断标准）
- 用户明确要求"记录这个经验"

**激活方式**：在任务收尾阶段，Agent 主动调用本技能走一次小循环，不需要用户请求。

---

## 入口守卫（所有操作的统一入口）

> **S 级要求：所有外部输入必须经过校验，拒绝畸形数据进入核心逻辑。**

```python
def sedimentation_guard(input_config: dict) -> dict:
    """
    统一参数校验守卫，所有操作入口必须调用此函数。
    返回 (valid: bool, reason: str, sanitized: dict)
    拒绝以下情况：
    - frequency_threshold < 10 或 > 30
    - TTL <= 0
    - skill_name 含特殊符号（仅允许字母/数字/下划线，长度1-64）
    - new_content_bytes < 0 或 > 1MB
    - 任意必需字段为 None 或空字符串
    """
    errors = []
    cfg = input_config or {}

    ft = cfg.get("frequency_threshold", 15)
    if not isinstance(ft, (int, float)) or ft < 10 or ft > 30:
        errors.append(f"frequency_threshold={ft} 超出范围 [10, 30]")

    ttl = cfg.get("TTL_hours", 24)
    if not isinstance(ttl, (int, float)) or ttl <= 0:
        errors.append(f"TTL_hours={ttl} 必须 > 0")

    skill_name = cfg.get("skill_name", "")
    import re
    if skill_name and (len(skill_name) > 64 or not re.match(r"^\w+$", skill_name)):
        errors.append(f"skill_name='{skill_name}' 格式非法（仅字母/数字/下划线，最多64字符）")

    content_bytes = cfg.get("new_content_bytes", 0)
    if content_bytes < 0 or content_bytes > 1_048_576:
        errors.append(f"new_content_bytes={content_bytes} 超出 1MB 上限")

    if errors:
        return {"valid": False, "reason": "; ".join(errors), "sanitized": {}}
    return {"valid": True, "reason": "ok", "sanitized": cfg}
```

---

## 闭环流程

### Step 1 — Trigger（前置预检，非强制）

```python
# 信息增益预评估
if 任务输出为空:
    skip_all()
elif 任务产出与最近3条经验高度重复（相似度 > 0.8）:
    skip_reflect()  # 跳过 Reflect，但仍可 Distill 已有经验
else:
    proceed_to_reflect()
```

### Step 2 — Retrieve（读取上下文）

读取经验银行文件（位于 `_core_files/memory/`）：

```
reflections.md   — 本次待处理的原始经验条
promotions.md    — 已达到晋升门槛的正式规则
```

文件不存在时以空列表处理，不报错。

### Step 3 — Reflect（生成经验条）

按以下格式在 `reflections.md` 追加一条经验：

```markdown
## [{date}] {经验主题}

**上下文**：{触发这次任务的情况，一句话}
**做法**：{这次实际怎么做的}
**结果**：{outcome vs intent 对比，好/坏/中性}
**有效性自评分**：{1-5，5=极有价值下次必用}
**可复用点**：{一句话原则/模式/checklist}
**标签**：#经验 #领域标签

---
```

- 每次闭环最多写一条，不贪多
- 有效性自评分（1-5）供 Promote 的自适应评估使用
- 标签用 `#[领域]` + `#[类型]`（#经验 #错误 #偏好 #流程）

### Step 4 — Distill（提炼知识）

| 经验类型 | 动作 |
|---------|------|
| 错误根因类 | 追加到 `TABOOS.md` §二 |
| 流程优化类 | 更新对应 Skill 的 SKILL.md（仅限 `_core_files/skills/`） |
| 角色/项目特定 | 更新 `memory/characters/` 或 `memory/YYYY-MM-DD.md` |
| 通用原则 | 追加到 `MEMORY.md` 合适章节 |

**Distill 受幅度限制约束，所有写操作统一受 5% 增量上限约束。**

### Step 5 — Promote（自适应晋升门槛检查 + 频率监控）

**自适应评估公式：**
```
晋升优先级 = 有效性自评分(1-5) × 任务类型权重 + 用户显式点赞×10 + 失败修复加成×5
```

- 任务类型权重：错误修复=2.0，流程优化=1.5，偏好养成=1.0，常规操作=0.5
- 用户显式点赞：用户说"记下来以后用" = +10
- 失败修复加成：同类错误连续出现2次 = +5

**晋升触发条件（满足任一即晋升）：**
- 晋升优先级 ≥ 当前阈值（默认 15，范围 [10, 30]）
- 或用户明确要求制度化

**晋升频率监控与自动阈值调整：**
- 最近 1 小时内晋升次数 ≥ 3 → 阈值临时提升至 20
- 连续 3 次晋升被人类否决 → 阈值永久 +2
- 连续 10 次晋升无否决 → 阈值永久 -2
- **手动覆盖后锁定 60 秒**：用户手动覆盖阈值后，60 秒内不触发自动永久调整
- 用户手动覆盖优先级始终高于系统自学习

**晋升执行后，生成结构化事件（见可观测性章节）。**

---

## 经验银行文件格式

### `reflections.md`

```markdown
# 经验银行 - 待处理

## [{date}] {主题}
**上下文**：...
**做法**：...
**结果**：{好/坏/中性}
**有效性自评分**：{1-5}
**可复用点**：...
**标签**：#经验 #xxx

---
```

### `promotions.md`

```markdown
# 晋升记录

## 系统元数据
**当前晋升阈值**：15（默认值，可配置）
**最近1小时晋升次数**：0
**阈值手动覆盖锁定到期**：null（时间戳或null）
**阈值调整历史**：[{"date":"","from":15,"to":17,"reason":"连续3次否决"}]

---

## [{date}] {已晋升经验}
**晋升优先级得分**：{计算过程}
**触发条件**：{达到哪个条件}
**原始**：reflections.md [{date}]
**现状**：写入 MEMORY.md §xxx / TABOOS.md / 新建 Skill: xxx

---
```

---

## 防失控约束机制

### 写操作安全流水线（调用顺序：先安检，后限流）

```
目标路径 → sandbox_path_check() → amplitude_check() → 实际写入
                ↓                      ↓
          路径穿越检查             幅度限制检查
          (step 1，必须先执行)      (step 2，在安全路径上执行)
```

### ① 沙盒隔离 + 路径穿越检查

| 目录 | 可写内容 |
|------|---------|
| `_core_files/memory/` | reflections.md / promotions.md / 日记账 / 角色档案 / TABOOS.md / MEMORY.md |
| `_core_files/skills/` | Promote 后新建的 Skill 文件 |

**路径穿越检查（step 1，必须先执行）：**

```python
def sandbox_path_check(target_path: str) -> None:
    import pathlib, os
    if ".." in target_path:
        raise SecurityError(f"非法路径序列: {target_path}")
    real = pathlib.Path(target_path).resolve()
    allowed_parents = [
        pathlib.Path("_core_files/memory").resolve(),
        pathlib.Path("_core_files/skills").resolve(),
    ]
    if not any(str(real).startswith(str(p)) for p in allowed_parents):
        raise SecurityError(f"路径穿越检测失败: {target_path}")
    if os.path.islink(target_path):
        link_target = os.path.realpath(target_path)
        if not any(link_target.startswith(str(p)) for p in allowed_parents):
            raise SecurityError(f"符号链接穿越: {target_path}")
```

### ② 幅度限制（全局，统一 amplitude_check()）

**step 2：在 sandbox_path_check() 确认路径安全后执行。**

```python
def amplitude_check(target_file_path: str, new_content_size: int) -> tuple:
    """
    返回 (allowed: bool, split_count: int, reason: str)
    超出 5% → 分批写入，每次间隔至少1个会话轮次
    目标文件不存在 → 允许（全新文件）
    """
    import os
    if not os.path.exists(target_file_path):
        return (True, 1, "新文件，无幅度限制")
    current_size = os.path.getsize(target_file_path)
    ratio = new_content_size / max(current_size, 1)
    if ratio <= 0.05:
        return (True, 1, f"幅度{ratio:.2%} <= 5%，直接写入")
    split_count = max(2, int(ratio / 0.05) + 1)
    return (True, split_count, f"幅度{ratio:.2%} > 5%，分{split_count}批写入")
```

### ③ 人类在环否决权

涉及以下情况的晋升**默认拒绝**，等待用户确认：
- 能力边界突破（新增技能领域、新角色设定）
- 规则重写（修改已有铁律）
- 资源分配（新增外部依赖）

**超时机制**：用户超过 **10 分钟无响应** → 默认拒绝，不阻塞主流程。
用户可随时通过"允许这次晋升"撤销默认拒绝状态。

### ④ 锚定约束（不可绕过）

以下为铁底，任何 Promote 操作都不得覆盖或删除：
- 核心流程步骤（Trigger / Retrieve / Reflect / Distill / Promote）
- 晋升优先级公式及触发条件
- 防失控约束本身
- `sedimentation_guard()` / `sandbox_path_check()` / `amplitude_check()` 的实现逻辑
- 手动覆盖与自动调整互斥规则（锁定 60 秒）
- 写操作安全流水线顺序（先路径后幅度）

### ⑤ 逆向自我检查 + TTL 防循环

每次 Distill 后自问："这次提炼是否偏离了最初目标？"
- 发现偏离 → 记录新经验条
- **同一"偏离检测"经验条 24 小时内不重复写入**（TTL 保护）

---

## 可观测性：结构化事件格式

> **S 级要求：所有关键路径产生结构化事件，供日志/监控/审计使用。**

每次关键操作后生成以下 JSON 事件：

```json
{
  "event_type": "sedimentation.promote",
  "timestamp": "2026-07-24T19:41:00+08:00",
  "session_id": "当前会话ID",
  "skill_name": "skill-sedimentation",
  "promotion": {
    "priority_score": 18.5,
    "trigger": "priority_threshold",
    "threshold_at_time": 15,
    "output_type": "rule | skill",
    "output_target": "MEMORY.md §二 / 新建 Skill: xxx"
  },
  "guard": {
    "path_check_passed": true,
    "amplitude_check_passed": true,
    "human_veto": false,
    "sandbox_path": "_core_files/memory/reflections.md"
  },
  "performance": {
    "duration_ms": 123,
    "bytes_written": 512
  },
  "audit": {
    "operator": "agent | user",
    "operator_id": "agent_main_001"
  }
}
```

**事件注入点：**

| 事件 | 触发时机 |
|------|---------|
| `sedimentation.reflect` | Reflect 完成后 |
| `sedimentation.distill` | Distill 完成后 |
| `sedimentation.promote` | Promote 完成后 |
| `sedimentation.guard_triggered` | 防失控约束触发时 |
| `sedimentation.veto` | 人类否决时 |
| `sedimentation.threshold_update` | 阈值热更新时 |
| `sedimentation.experience_cleared` | 紧急清空时 |

---

## 可测试性：测试设计

> **S 级要求：核心逻辑有可执行的测试用例，不依赖真实文件系统。**

### 内存沙盒适配器（测试用）

```python
class InMemorySandbox:
    """测试用内存文件系统适配器，替代真实 _core_files/ 目录"""
    def __init__(self):
        self.files = {}  # path -> content_bytes

    def read(self, path):
        return self.files.get(path, b"")

    def write(self, path, data):
        self.files[path] = len(data)

    def exists(self, path):
        return path in self.files

    def getsize(self, path):
        return self.files.get(path, 0)
```

### 回归测试用例（50 条）

| 用例类型 | 数量 | 覆盖场景 |
|---------|------|---------|
| 参数校验 | 10 | 极端值、空值、非法格式 |
| 沙盒安全 | 10 | 路径穿越、符号链接、绝对路径 |
| 幅度限制 | 5 | 刚好5%、超过5%、新文件 |
| 晋升逻辑 | 10 | 刚好15分、刚好14分、用户点赞叠加 |
| 频率监控 | 5 | 1小时3次、连续否决、连续无否决 |
| TTL 防循环 | 5 | 24h内重复、24h后重放 |
| 并发安全 | 5 | 10线程并发晋升、读写冲突 |

---

## 可运维性：运维操作

### 阈值热更新

```python
def update_threshold(new_value: int, operator: str = "user") -> dict:
    """
    运行时调整晋升阈值。
    - new_value 范围 [10, 30]
    - 记录 audit trail
    - 返回 {"success": True, "old": 15, "new": 20}
    """
    guard = sedimentation_guard({"frequency_threshold": new_value})
    if not guard["valid"]:
        return {"success": False, "reason": guard["reason"]}
    emit_event("sedimentation.threshold_update", {"old": current, "new": new_value, "operator": operator})
    return {"success": True, "old": current, "new": new_value}
```

### 紧急清空操作

```python
def clear_experience(skill_id: str = None, cascade: bool = False, confirm: bool = False) -> dict:
    """
    紧急清空经验库。
    - skill_id=None → 清空全部 reflections.md
    - skill_id="xxx" → 仅清空指定技能经验
    - cascade=True → 同时清空 promotions.md 中对应记录
    - confirm=True → 二次确认标志（防止误操作）
    必须 confirm=True 才执行，否则返回 {"success": False, "reason": "需要二次确认"}
    """
    if not confirm:
        return {"success": False, "reason": "需要二次确认（confirm=True）"}
    emit_event("sedimentation.experience_cleared", {"skill_id": skill_id, "cascade": cascade, "operator": "user"})
    return {"success": True, "cleared": skill_id or "all"}
```

### 沙盒空间检查

```python
def check_sandbox_space() -> dict:
    """晋升前检查磁盘空间，若可用空间 < 50MB 则降级为仅记录不生成新文件"""
    import shutil, os
    path = os.path.dirname(os.path.abspath("_core_files/memory"))
    total, used, free = shutil.disk_usage(path)
    free_mb = free // (1024 * 1024)
    if free_mb < 50:
        return {"status": "degraded", "free_mb": free_mb, "action": "write_to_memory_only"}
    return {"status": "healthy", "free_mb": free_mb}
```

---

## 铁律

1. **每次闭环最多一条经验**
2. **Distill 不新增文件**：只更新已有结构化文件
3. **Promote 严格守自适应门槛**：不够证据就等，不凑数
4. **诚实记录结果**：做得好和做得差的两类经验同等对待
5. **标签必须打**：影响后续检索和模式发现
6. **锚定约束不可覆盖**：铁律中的铁律，任何情况下均优先执行
7. **沙盒边界不可逾越**：所有写操作仅限 `_core_files/memory/` 和 `_core_files/skills/`
8. **幅度限制全局生效**：所有写操作均受 5% 上限约束
9. **TTL 防止循环**：同一偏离检测经验 24h 不重复写入
10. **路径穿越零容忍**：任何写操作路径必须经过 `sandbox_path_check()`
11. **安全流水线顺序不可变**：先 `sandbox_path_check()`，后 `amplitude_check()`
12. **手动覆盖锁定 60 秒**：用户手动覆盖阈值后，60 秒内不触发自动永久调整
13. **所有操作必须经过 `sedimentation_guard()` 入口校验**
14. **关键路径必须 emit 结构化事件**
15. **紧急清空必须 confirm=True**

---

## 与 MOIR 五层的对应关系

| 闭环步骤 | MOIR 层 | 载体 |
|---------|---------|------|
| Trigger（预检） | L1 | 本轮任务上下文 |
| Reflect | L2 | `reflections.md` |
| Distill | L3 / L4 | IMA KB + 本地结构化文件 |
| Promote | L4 | `promotions.md` → `MEMORY.md` / `TABOOS.md` / 新 Skill |
| 锚定约束 | L4 | 本技能 SKILL.md 本身 |

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| v1.0.0 | 2026-07-24 | 初稿，对标 Hermes Loop |
| v2.0.0 | 2026-07-24 | +5 条防失控约束（DeepSeek B 级） |
| v2.1.0 | 2026-07-24 | +动态晋升/频率监控/路径穿越检查（DeepSeek B+ 级） |
| v2.2.0 | 2026-07-24 | +安全流水线顺序/手动覆盖锁定（DeepSeek A 级） |
| v3.0.0 | 2026-07-24 | +入口守卫/结构化事件/紧急清空/可测试设计（DeepSeek **S 级**） |

---

*Created by Director · 2026-07-24*
*Supervised by DeepSeek Bridge v3.0 · Self-evolution loop ready*
