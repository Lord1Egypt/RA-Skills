# VC Hard Gates Card

> 子Agent Prompt 内联组件。11 条硬性门控，违反任一即不合格。子Agent 必须逐条对照执行。
> 由 `../SKILL.md §并行子Agent调度` 引用。

---

## Gate 1: 禁止主观词 — O 维度自动判否

Pass/Fail Criterion 中扫描以下词，发现 → 自动 **O = ✗**：

`良好` `合理` `足够` `适当` `正常` `快速` `稳定` `必要` `最小`
`good` `sufficient` `appropriate` `adequate` `reasonable` `fast enough` `robust`

替代：必须用 `≤ X` / `≥ Y%` / `= Z` + 单位。

---

## Gate 2: Domain-Boundary 覆盖 — C 维度自动判否

涉及物理量（电压/电流/温度/功率）的 VC → 必须在需求自身运行域的 **3 类温度点** 验证：
- 需求运行域**下限**（从需求/SOR/系统规范中提取）
- **名义温度**（通常 +25°C，除非需求另有规定）
- 需求运行域**上限**（从需求/SOR/系统规范中提取）

仅在名义温度 → 自动 **C = ✗**。

**豁免**: 纯数字/逻辑需求（CAN 协议解析、DTC 存储逻辑、Bootloader 握手），在 VC 中声明豁免理由。

---

## Gate 3: Source Depth — ≥3[A] → VC-BLOCKED

每个数值标注来源：
- `[R]` 需求原文 | `[D]` 逻辑推导 | `[S]` 标准/规范 | `[E]` 工程判断 | `[A]` 未确认假设

- 未标注 → M = ✗
- ≥3 个 `[A]` → 🔴 VC-BLOCKED（标记后继续下一条）
- 任意 `[A]` → 自动 A = ✗

---

## Gate 4: Double-100（安全功能）

涉及 ASIL / 保护 / 安全的需求 → 必须满足：

| 条件 | 要求 |
|------|------|
| 故障存在时 | N ≥ 100，触发率 = 100% |
| 正常运行时 | N ≥ 100，误触发率 = 0% |

违反 → C = ✗。

---

## Gate 5: 不复述需求原文（反模式 #1）

VC 必须比需求更具体：加方法、条件、数值判据。仅复述需求 → 零信息增量 → 不合格。

---

## Gate 6: 不引用 Test Case 编号（反模式 #2）

VC 中禁止写 "详见 TC-001"。VC 是 TC 的上游输入，不能循环引用。直接写明方法/条件/判据。

---

## Gate 7: 验证方法决策树（反模式 #5）

不允许所有 VC 统一用 "Test"：

- 物理量（电压/电流/温度/振动/EMC）→ **Test** (HIL/车辆/环境箱)
- 数学推导/仿真可验证 → **Analysis** (WCA/仿真/统计建模)
- 文档/布局/外观 → **Inspection** 或 **Demonstration**
- 不确定 → 组合多种方法

---

## Gate 8: 不编造数值（反模式 #6）

每个阈值/样本量/温度/设备精度必须标注 Source Depth tag (`[R]/[D]/[S]/[E]/[A]`)。

拍脑袋写的数值 → 看似专业实则不可验证。不知道来源 → 标记 `[A]` 并记录假设。

---

## Gate 9: 不静默失败（反模式 #8）

子Agent 遇到异常（需求无法理解、关键参数缺失）→ 标注 `⚠️ degraded: {原因}` 继续下一条。

禁止静默跳过、禁止编造补充、禁止自行猜测。

---

## Gate 10: SMARTR-OC 自检（反模式 #9）

每条 VC 必须执行 SMARTR-OC 8 维自检，结果附在 VC 后面。

- 8/8 → ✅
- 6-7/8 → ⚠️（标注弱项）
- <6/8 → ❌（修订 VC 或标记 VC-BLOCKED）

> 输出格式 + Gate Compliance Checklist 格式 → `references/vc-subagent-prompt.md`

---

## Gate 11: 表格单元格换行 — 必须用 `<br>`

VC 表格的 `Test Conditions` 和 `Pass/Fail Criterion` 列**必须**使用 `<br>` 分隔独立条件项，每行一个条件。
禁止使用 `; ` 或空格把多个条件拼在同一行。

✅ 正确：
```
| ... | Rig: HIL + 电池模拟器<br>Temp: -40°C, +25°C, +85°C<br>Precondition: BMS 上电自检通过 |
```

❌ 错误：
```
| ... | Rig: HIL; Temp: -40°C, +25°C, +85°C; Precondition: BMS 上电自检通过 |
```

违反 → 整体格式不合格，需重写该 VC 的表格行。详见 `assets/vc-template.md`。
