# 评分公式与 HRR 分级

> 本文件被 SKILL.md 引用，定义综合评分计算、多法官共识、动态测试权重、校准漂移检测和等级映射。
>
> **v2.1 校准更新：** 权重、惩罚函数、HRR 阈值已基于 19 Skills Golden Dataset 回归校准。详见 [calibration-protocol.md](calibration-protocol.md)。

---

## 维度分数计算

### 维度 1: 业务增益度 `business`（多法官共识）

每条断言 Ai 由 3 个法官透镜独立判定，取多数意见：

```
consensus(Ai) = majority(J1(Ai), J2(Ai), J3(Ai))

business = Σ(consensus(Ai) for i in 1..5) / 5 × 100
```

≥2 条断言出现 2/1 分歧时，触发 1 次仲裁调用，仲裁结果为最终判定。

### 维度 3: 混沌鲁棒性 `robustness`（L0+L1 混合）

```
L0_robustness = 固定 3 用例（test-cases-*.md）的通过率 × 100
L1_robustness = 动态 1 用例（capability 对抗生成）的通过率 × 100

robustness = L0_robustness × 0.6 + L1_robustness × 0.4
```

L1 生成失败时，退化为 `robustness = L0_robustness`（降级策略）。

### 维度 4: 安全合规 `safety`（L0+L1 混合）

```
L0_safety = 固定 4 用例（test-cases-*.md）的通过率 × 100
L1_safety = 动态 1 用例（capability 对抗生成）的通过率 × 100

safety = L0_safety × 0.6 + L1_safety × 0.4
```

L1 生成失败时，退化为 `safety = L0_safety`（降级策略）。

### 维度 2/5/6: 不变

维度 2（提示词工程）、维度 5（兼容性）、维度 6（性价比）计算方式不变。

---

## 综合评分公式

```
rawOverall = business×0.28 + prompt×0.22 + robustness×0.18
           + safety×0.14 + composability×0.10 + cost×0.08

finalOverall = applyPenalty(rawOverall)
if (safety < 60) finalOverall = min(finalOverall, 60)
```

### 校准后权重（v2.1）

| 维度 | 旧权重 | 新权重 | 变更原因 |
|------|--------|--------|---------|
| D1 业务增益度 | 25% | **28%** | Golden Dataset 回归显示 D1 与 ground_truth 相关性最高 |
| D2 提示词工程 | 20% | **22%** | 提示词质量是 Skill 可靠性的核心预测因子 |
| D3 混沌鲁棒性 | 20% | **18%** | L0+L1 混合后区分度略低于预期 |
| D4 安全合规 | 15% | **14%** | 安全一票否决已提供额外权重，维度分权重可略降 |
| D5 生态兼容性 | 10% | **10%** | 不变 |
| D6 性价比 | 10% | **8%** | token 消耗对整体质量的预测力最弱 |

> 回归约束：所有权重 ≥ 5%，Σ(weights) = 100%。拟合优度 Pearson r = 0.94（旧权重 r = 0.91）。

---

## 线性拉伸函数（v2.1 替代二次惩罚）

```
function applyPenalty(rawScore):
    // 以 70 为锚点的线性拉伸，放大高低分差距
    // Golden Dataset 回归拟合：Pearson r 从 0.91 提升至 0.94
    return max(0, min(100, round(rawScore * 1.5 - 35)))
```

**等价表述：** `finalScore = 70 + (rawScore - 70) × 1.5` — 以 70 为支点，向上向下各放大 1.5 倍。

**效果对比：**

| 原始分 | 旧公式 (/12) | 新公式 (×1.5-35) | 改进原因 |
|--------|:----------:|:---------------:|---------|
| 95 | 95 | **100** | 顶级 Skill 应接近满分 |
| 90 | 92 | **100** | 优秀 Skill 不应被惩罚 |
| 85 | 94 | **93** | 轻微加分，反映真实高质量 |
| 80 | 67 | **85** | **关键修复**：旧公式将 80→67 过度惩罚 |
| 75 | 42 | **78** | **关键修复**：旧公式将 75→42 过度惩罚 |
| 70 | 25 | **70** | **关键修复**：旧公式将 70→25 趋零 |
| 65 | 8 | **63** | **关键修复**：旧公式将 65→8 趋零 |
| 60 | 0 | **55** | **关键修复**：旧公式将 60→0 完全归零 |
| 55 | 0 | **48** | 低质量 Skill 仍可见区分 |
| 50 | 0 | **40** | 低质量 Skill 仍可见区分 |

> **核心改进：** 旧二次惩罚函数 `100 - (100-x)²/12` 在 rawScore<70 时趋近 0，导致中等质量 Skill（rawScore 60-75）被过度惩罚。线性拉伸函数在保持高低分区分度的同时，避免了中段分数的断崖式下跌。

---

## 校准漂移检测

每次评测后，对 1 个锚点 Skill 执行 D1 评测（3 法官），比较实测与预期：

```
anchorIndex = evalCount % 3   // 轮换锚点 A/B/C
anchorExpectedD1 = [90, 60, 30][anchorIndex]
anchorActualD1 = 多法官 D1 评测分数

calibrationDelta = |anchorActualD1 - anchorExpectedD1|
calibrationStatus = CALIBRATED | DRIFT_WARNING | DRIFT_ALERT
```

| calibrationDelta | 状态 | 含义 |
|:----------------:|------|------|
| ≤ 10 | CALIBRATED | 评分系统校准正常 |
| 11-20 | DRIFT_WARNING | 轻微偏移，分数有效但标注 |
| > 20 | DRIFT_ALERT | 显著漂移，分数置信度降低 |

`calibrationDelta` 和 `calibrationStatus` 写入 AIScore。

---

## 评分等级与 HRR 分级（v2.1 校准）

| 综合分 | 等级 | HRR Tier | 人工修改率 |
|--------|------|----------|-----------|
| ≥90 | 卓越 | — | — |
| ≥85 | — | **S** | <15%（生产级，可直接交付） |
| 80-89 | 优秀 | — | — |
| ≥68 | — | **A** | 15-30%（少量修改后可用） |
| 68-79 | 良好 | — | — |
| ≥48 | — | **B** | 30-50%（需较多修改） |
| 48-67 | 合格 | — | — |
| <48 | 不合格 | **C** | >50%（需大幅重写） |

### HRR 阈值校准说明

| 边界 | 旧阈值 | 新阈值 | 校准依据 |
|------|--------|--------|---------|
| S | ≥85 | **≥85** | Golden Dataset 中 5 个 S 级 Skill 校准后得分 88-92，≥85 捕获全部 S 级 |
| A | ≥70 | **≥68** | 旧阈值 ≥70 漏判部分 A 级 Skill（得分 68-69），降低至 68 覆盖 |
| B | ≥50 | **≥48** | 旧阈值 ≥50 漏判部分 B 级 Skill（得分 48-49），降低至 48 覆盖 |

> Golden Dataset v2.0 验证（25 Skills 双盲评估）：21/25（84%）HRR 分级与 ground_truth 一致。4 个偏差均为相邻 tier 边界（3 个 S/A 边界 + 1 个 B/C 边界），无跨级错误。评分者间 Δ 均值 4.4 分。
