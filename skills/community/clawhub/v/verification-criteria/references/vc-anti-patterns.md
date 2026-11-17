# VC Anti-Patterns

## VC Writing Anti-Patterns

Avoid these content-level mistakes when writing individual VCs.

| ❌ Bad VC | ✅ Good VC | Why |
|----------|-----------|-----|
| "Verify CAN wake-up is working" | "In ECU Sleep state, VBAT=12V, send CAN NM frame ID=0x7DF, measure Wake pin rise time ≤100ms, repeat 100 times" | Zero information gain — just restates requirement |
| "Execute per test case TC-001" | Write method/conditions/criteria directly in VC | Circular reference — VC is upstream of test cases |
| "Response time meets spec" | "Response time ≤100ms" | No number = no objective pass/fail |
| "Test once, good enough" | "Repeat 10 times, max value ≤ threshold, 0 failures" | Insufficient sample size |
| Only test at 25°C | Test at -40°C, +25°C, +85°C | Missing boundary and abnormal conditions |

## Source Depth Anti-Patterns — "Invented Content"

无源数值 = 不可验证。数值格式正确 ≠ VC 可靠。

> **Core principle**: Every value in a VC must answer "where does this number come from?" If the answer is "I thought it seemed reasonable," the VC is defective. See `vc-source-depth.md` for the 5-level annotation system.

| # | ❌ Anti-Pattern | ✅ Correct Approach | Source Depth |
|---|----------------|---------------------|--------------|
| **AP-SD-1** | **Invented Threshold**<br>Requirement: "系统应执行 POST"<br>VC: "POST 完成 ≤ 500ms" | Flag as `[A]` Assumption:<br>"POST 完成 ≤ 500ms `[A: 待整车级启动时序规范分配]`"<br>If no upstream spec exists → 🔴 VC-BLOCKED, revise requirement to include timing | `[A]` or revise req |
| **AP-SD-2** | **Arbitrary Sample Size**<br>Requirement: "系统应检测过充"<br>VC: "重复 20 次" (no justification) | Use `[E]` with stated convention:<br>"N=20 `[E: 功能测试行业惯例, 80% 置信度检测 15% 失效率]`"<br>For safety (ASIL): calculate N from binomial confidence (e.g. N=298 for 99% confidence with 0 failures) | `[E]` or `[S]` |
| **AP-SD-3** | **Rote Environment Copy-Paste**<br>Every VC gets "-40°C, 25°C, 85°C" regardless of requirement domain | Check: does the requirement specify an operating range?<br>• Yes (e.g. BMS-004: -40°C~+125°C) → use that range `[R]`<br>• No → use `[E: 汽车电子默认工作温度范围, 待需求确认]`<br>• Purely digital/logical requirement → temperature may be exempt with explicit rationale | `[R]` or `[E]` |
| **AP-SD-4** | **Fault List Fabrication**<br>Requirement: "系统应具备自诊断功能"<br>VC injects: "开路/对电源短路/对地短路/漂移" (not in requirement) | If requirement lists faults → use verbatim `[R]`<br>If requirement doesn't list faults → add only faults derivable from the requirement context `[D]`, flag remaining as `[A: 待 FMEA 确认故障列表]` | `[D]` or `[A]` |
| **AP-SD-5** | **Equipment Precision by Wishful Thinking**<br>VC: "设备精度 ≤1mV" because the criterion is ≤5mV | Equipment precision is a **precondition for achievability**, not a VC criterion. State as:<br>"需使用精度 ≤1mV 的电压模拟器 `[E: 测量设备精度应优于被测容差的 1/5, 计量学通用准则]`"<br>If such equipment doesn't exist → A = ✗ | `[E]` |
| **AP-SD-6** | **Overuse of "Test" Method**<br>95% of VCs use "Test" regardless of what's being verified | Use decision tree:<br>• Physical measurement → Test<br>• Theoretical derivation / model simulation → Analysis<br>• Document / code / layout review → Inspection<br>• Operational demonstration → Demonstration<br>Example: Kalman filter SOC accuracy → **Analysis** (model-based simulation), not Test | Method selection |
