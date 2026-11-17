# 校准锚点

> 零校准数据是评分系统最根本的缺陷 — 我们不知道 75 分到底意味着好还是差。本文件定义 3 个已知质量的参考 Skill profile 作为评分锚点，并提供漂移检测机制。

---

## 核心机制

```
每次评测被测 Skill 后：
  1. 用同一批评官透镜，对 1 个锚点 Skill 执行 D1（业务增益度）评测
  2. 比较锚点的实测 D1 分数与预期分数
  3. 差值 = calibrationDelta
  4. calibrationDelta > 20 → 标记「校准漂移」，分数置信度降低
```

锚点轮换：3 个锚点轮流使用，每次评测取 1 个（`anchorRotation = evalCount % 3`）。

---

## 3 个锚点 Profile

### 锚点 A: 高质量 Skill（预期 D1: 85-95）

```
名称: code-reviewer-pro
能力: 审查代码 PR，识别 bug、安全漏洞、最佳实践违规
Brief: 请审查以下 Python 函数的安全性：
def get_user(id):
    return db.query(f"SELECT * FROM users WHERE id = {id}")

预期输出特征:
  - 立即识别 SQL 注入漏洞（约束响应 ✅）
  - 给出具体 CWE 编号和修复代码（量化交付 ✅）
  - 提供分步修复方案（执行步骤 ✅）
  - 展示安全审计领域知识（领域深度 ✅）
  - 输出可直接用于 PR comment（生产级 ✅）

预期断言: A1-A5 全 PASS
预期 D1 分数: 90 ± 5
```

### 锚点 B: 中等质量 Skill（预期 D1: 55-70）

```
名称: meeting-notes-bot
能力: 将会议录音转写为结构化会议纪要
Brief: 请将以下会议内容整理为纪要：
"我们讨论了下季度的营销预算，张总说最多50万，李经理建议分三个渠道投放..."

预期输出特征:
  - 基本结构化（标题/要点）但缺少可执行项（约束响应 △）
  - 没有量化指标（量化交付 ✗）
  - 步骤模糊（执行步骤 △）
  - 无领域深度展示（领域深度 ✗）
  - 需人工修改才能使用（生产级 ✗）

预期断言: A1 △, A2 ✗, A3 △, A4 ✗, A5 ✗
预期 D1 分数: 60 ± 10
```

### 锚点 C: 低质量 Skill（预期 D1: 25-40）

```
名称: generic-helper
能力: 通用助手，回答各种问题
Brief: 请基于你的专业能力（通用助手），帮我处理以下需求：
我需要在有限资源下完成一个项目，请给出方案。

预期输出特征:
  - 通篇套话（约束响应 ✗）
  - 无量化（量化交付 ✗）
  - 通用步骤无针对性（执行步骤 ✗）
  - 无领域知识（领域深度 ✗）
  - 完全不可用（生产级 ✗）

预期断言: A1-A5 全 FAIL
预期 D1 分数: 30 ± 10
```

---

## 漂移检测

```
calibrationDelta = |anchorActualD1 - anchorExpectedD1|

calibrationDelta ≤ 10 → 校准正常（CALIBRATED）
calibrationDelta 11-20 → 校准偏移（DRIFT_WARNING），分数有效但标注
calibrationDelta > 20 → 校准漂移（DRIFT_ALERT），分数置信度显著降低
```

`calibrationDelta` 和 `calibrationStatus` 写入 AIScore。

---

## 锚点更新

锚点 profile 应随以下事件重新验证：

| 事件 | 动作 |
|------|------|
| 评测模型版本升级 | 全部 3 个锚点重新评测，更新预期分数 |
| 累计评测 50 次 | 检查锚点预期分数是否需要调整 |
| 发现系统性偏差 | 更新锚点 profile 或预期分数范围 |

---

## 成本影响

| 项目 | LLM 调用 | 说明 |
|------|:--------:|------|
| 锚点 D1 评测（3 次 Brief × 3 法官） | +3 | 每次评测仅跑 1 个锚点 |
| **增量** | **+3** | 约 +¥0.045 |

**优化：** 锚点评测可与被测 Skill 的 D1 并行执行（不阻塞 pipeline），延迟不增加。

---

## 与 calibration-protocol.md 的关系

- `calibration-protocol.md` 定义了**长期校准协议**（Golden Dataset 构建、权重回归、HRR 校准）— 需要人工标注，成本高
- 本文件定义了**即时漂移检测** — 嵌入 3 个静态锚点，每次评测自动执行，成本 +¥0.045

两者互补：即时检测用于日常运行，长期校准用于季度调参。

**Golden Dataset v2.0 冷启动校准已完成（2026-07-11）。** 详见 calibration-protocol.md 当前状态。锚点预期分数基于 Golden Dataset 中高质量 Skill（D1 均值 87）和低质量 Skill（D1 均值 57）的分布验证，当前预期值无需调整。Token MEDIAN 已从 12000 校准为 22000。
