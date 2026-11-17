# VC Source Depth Annotation System

> A mandatory element of VC quality: every value in a VC must have a traceable source.
> Loaded by Workflow A Step A.2a and Workflow B Step B.2.
> See also: `vc-anti-patterns.md` §Source Depth Anti-Patterns.

## Core Principle

> **"No Unsourced Content" (NUT)**: Every numeric value, environmental condition, fault injection type, equipment precision, and sample size in a VC must be traceable to a defined source. A VC with unsourced content is a VC with unverifiable content — no matter how professionally formatted.

---

## The Five Source Depth Levels

| Level | Tag | Definition | Example | Acceptable? |
|-------|-----|------------|---------|-------------|
| **0** | `[R]` | **Requirement-text**: value appears verbatim in the requirement | BMS-001 says "±5mV" → VC uses `≤ 5mV [R: BMS-001]` | ✅ Gold standard |
| **1** | `[D]` | **Derived**: logically deduced from the requirement wording, signed design documents, or published standards. Derivation chain must be independently verifiable — any engineer following the same logic reaches the same value. See `[D]` vs `[A]` boundary table below for the authoritative definition. | BMS-039 says "全生命周期" → VC adds `BOL/MOL/EOL [D: BMS-039 "全生命周期"]` | ✅ With derivation rationale |
| **2** | `[S]` | **Standard**: cited from a named standard, regulation, or upstream specification | FTTI values → `≤ 100ms [S: ISO 26262-4 §6.4.2.3, SG-01 HARA]` | ✅ With clause reference |
| **3** | `[E]` | **Engineering judgment**: domain convention or industry practice | N=20 repetitions → `N=20 [E: 功能测试行业惯例, 80%置信度检测15%失效率]` | ⚠️ Acceptable if convention is stated |
| **4** | `[A]` | **Assumption / Unknown**: value is unconfirmed, awaiting external input | POST time → `≤ 500ms [A: 待整车级启动时序规范分配]` | ⚠️ Acceptable only if documented; triggers **A (Achievable) = ✗** |

---

## Hard Gates

### Gate 1: Individual Value Check (per value)

```
每个数值有 source tag?
├─ Yes, [R]/[D]/[S] → ✅ Pass
├─ Yes, [E] → ⚠️ Pass, but convention must be stated
├─ Yes, [A] → ⚠️ Conditional pass: A (Achievable) = ✗ in SMARTR-OC
└─ No tag → 🔴 M = ✗ in SMARTR-OC
```

### Gate 2: Per-VC Aggregation (≥3 [A] → VC-BLOCKED)

```
单条 VC 中 ≥3 个值带 [A]?
├─ Yes → 🔴 VC-BLOCKED: requirement is too vague to support a verifiable VC. Rewrite the requirement.
└─ No → Proceed to SMARTR-OC
```

### Gate 3: [A] Automatically Forces A = ✗

```
VC 中有任何 [A] 标记?
├─ Yes → SMARTR-OC A (Achievable) = ✗ (unconfirmed assumption = achievability unknown)
│         → VC 最高分 = 7/8 → ⚠️ Acceptable with documented risk
└─ No → A scored normally
```

---

## What Gets Annotated — Mandatory Fields

Every VC field that contains a **specific value** (not a generic description) must carry a source tag:

| VC Field | What to Tag | Example |
|----------|-------------|---------|
| **Pass/Fail threshold** | Every numeric limit | `≤ 5mV [R: BMS-001]` |
| **Timing requirement** | Every time bound | `≤ 100ms [R: BMS-001]` |
| **Sample size (N)** | Every repetition count | `N=100 [E: 计量学通用准则, 1/5精度比]` |
| **Temperature range** | Every test temperature | `-40°C [R: BMS-004 operating range]` |
| **Fault injection type** | Every injected fault | `开路 [R: BMS-008 fault list]` |
| **Equipment precision** | Every stated precision | `精度 ≤1mV [E: 测量设备精度应优于被测容差1/5]` |
| **Supply voltage** | Every voltage condition | `9V~16V [S: 整车电气系统规范 V2.1]` |

Fields that are **descriptive labels** (not specific values) do not need tags:
- Verification method ("Test")
- Rig type ("BMS HIL")
- Measurement target description ("ADC sampled value")

---

## Annotation Format

### Inline (for VC tables)

```markdown
| 判定标准 | ... ≤ 5mV [R: BMS-001]; 采样周期 ≤ 100ms [R: BMS-001]; N=100 [E: 1/5精度准则] |
```

### Block (for structured VC templates)

```markdown
**Pass/Fail Criterion**:
- |误差| ≤ 5mV [R: BMS-001]
- 采样周期 ≤ 100ms [R: BMS-001]
- N=100 次/温度点 [E: 计量学通用准则, 测量设备精度应优于被测容差 1/5]
- 24h 漂移 ≤ 2mV [E: 工程经验值, 对应年漂移 ≤ 50mV]
```

### Explicit Assumption Record

When `[A]` is used, append an assumption record at the end of the VC document:

```markdown
## Assumption Log

| VC ID | Field | Assumed Value | Rationale | Resolution | Owner | Due Date |
|-------|-------|---------------|-----------|------------|-------|----------|
| VC-BMS-099 | POST completion time | ≤ 500ms | Typical MCU POST < 200ms; margin added | Await vehicle-level startup timing spec | SysEng | 2026-07-01 |
| VC-BMS-099 | ADC calibration result | Alerts but allows HV | Non-safety-critical sensor; degraded accuracy acceptable short-term | Confirm with FSC | SafetyEng | 2026-06-30 |
```

---

## Quick Decision Flow

For each value you're about to write into a VC, ask:

```
这个值来自哪里？
├─ 需求原文写了 → 用 [R: REQ-ID]
├─ 需求没写, 但可以从需求原文/已签署设计文档/已发布标准逻辑推导
│  → 用 [D: derivation logic]
│  └─ ⚠️ 红线: 若推导依赖"待确认的设计规范/待分配的指标/未签署的文档" → 不是 [D], 降级为 [A]
│     例: "库仑计基准 ≤0.1%" 若设计规范未定稿 → [A], 不是 [D]
├─ 某个标准/规范定义了 → 用 [S: standard clause]
├─ 行业惯例/工程判断 → 用 [E: stated convention]
│  └─ 能说出是哪个惯例吗？不能 → 降级为 [A]
└─ 不知道, 拍脑袋的 → 🔴 这就是问题！
    └─ 是否必须要有这个值？
        ├─ 是 → [A: assumption] + 记录假设 + 计划确认
        └─ 否 → 删除这个值, 不强加需求没有的约束
```

### `[D]` vs `[A]` 判定边界（高频误用点）

| 判据 | `[D]` Derived（✅ Pass） | `[A]` Assumption（⚠️ A=✗） |
|------|------------------------|---------------------------|
| 推导输入 | 需求原文 / 已签署设计文档 / 已发布标准 | 待确认设计规范 / 待分配指标 / 未定义协议字段 |
| 可独立验证 | 任何工程师重走推导链得同一值 | 依赖外部输入，不同人给不同值 |
| 典型正例 | `BOL/MOL/EOL [D: BMS-039 "全生命周期"]` | `FTTI [A: 待整车级分配确认]` |
| 典型误用 | ❌ `库仑计精度 ≤0.1% [D]`（设计未定稿） | ✅ `库仑计精度 ≤0.1% [A: 待BMS硬件设计规范v1.2确认]` |

---

## Relationship to SMARTR-OC

| SMARTR-OC Dimension | How Source Depth Affects It |
|--------------------|-----------------------------|
| **M (Measurable & Sourced)** | Unsourced value → M = ✗ |
| **A (Achievable)** | Any `[A]` flag → A = ✗ (assumption unconfirmed = achievability unknown) |
| **R (Repeatable)** | Unsourced values → different engineers may pick different values → not repeatable |
| **T (Traceable)** | Source tags create bidirectional traceability from VC values back to their origin |
