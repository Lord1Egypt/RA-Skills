# Harness Governance：四权分离治理执行层

> 本文件由 SKILL.md 引用。定义执行层面的治理机制：Task Contract 格式、四代理拓扑、调度规则、常见作弊与对策。

## 权责分离：治理架构与角色分工

以下为五权分离治理架构。治理专用角色的"审查权力"仅针对合约合规性——不评判其它 P8 任务代码的技术正确性。

| 权力角色 | 对应西游角色 | 职责 | 权限边界 |
|---------|------------|------|---------|
| **合约定义者** | 🟠 如来佛祖 | 在任务开始时创建 Task Contract，声明交付物、验收命令、禁区 | 定义什么算成功、踩什么线即否决 |
| **风险扫描者** | 🟢 太上老君 | 在任务执行中扫描所有操作，标记高风险路径 | 只标记风险，不修改代码 |
| **验收验证者** | 🟡 百眼魔君 | 任务交付后运行验收命令，验证"任务完成"声明 | 只验证命令输出，不验证代码逻辑 |
| **终审裁决者** | 🟣 沙悟净 | 在确认验收全绿、无禁区触碰后，做最终 Gate 裁定 | 裁定依据是验证结果，不是主观判断 |
| **执行任务者** | 🔵 孙悟空 | 执行 Task Contract 中的任务，不碰 verify/gate | 不评判自己的交付是否通过验收 |

**防冲突规则**：同一角色不能同时担任合约定义者和终审裁决者。**审查边界**：治理角色的"审查"是针对合约合规性、输出与声明的匹配——不评判技术方案是否正确。

## 组件映射

| Harness 概念 | 对应组件 | 实现方式 |
|-------------|---------|---------|
| Task Contract | 项目级或任务级 | `python scripts/harness-engine.py contract ...` |
| Verifier | scripts/harness-engine.py verify | 运行验证命令并返回结果 |
| Gate | scripts/harness-engine.py gate | 读取 Contract + Verifier 结果，通过或驳回 |
| Scan Risk | scripts/harness-engine.py scan-risk | 在每次文件操作前自动扫描 |
| Load | scripts/harness-engine.py load | 加载 `data/harness.md` 治理状态，返回活跃合约与违规统计 |
| Runner | P8 agent (执行角色孙悟空) | 执行 Task Contract 中的交付项 |

## 四代理上下文隔离拓扑

```
主Agent (P10·玄奘 · 全局)
├── P8-1 (执行角色孙悟空) — contract_1.json
├── P8-2 (执行角色孙悟空) — contract_2.json
├── 风险扫描代理 (太上老君) — 跨合约全局扫描
├── 验收代理 (百眼魔君) — 串行执行，逐合约验证
└── 终审代理 (沙悟净) — 接收百眼魔君输出，执行 gate
```

**隔离规则**：
- 每个 P8 在自己的 contract_*.json 沙箱中运行
- 不跨合约共享状态，不读取别人的合约
- 风险扫描代理拥有全局读权限，但只标记不修改
- 验收代理在任何给定时刻只处理一个合约
- 终审代理的裁决是只读的

## Agent 文件与权力边界

| 代理 | 文件域 | 可读 | 可写 | 执行命令 |
|------|--------|------|------|---------|
| 执行 Agent | codebase/* | ✅ | ✅ (仅限合同规定区域) | ✅ |
| 风险扫描代理 | 全局 | ✅ | ❌ | ✅ (仅 scan-risk) |
| 验收代理 | contract_*.json + P8 output | ✅ | ❌ | ✅ (仅 verify) |
| 终审代理 | contract_*.json + verify output | ✅ | ❌ | ✅ (仅 gate) |

**绝对禁止**：风险扫描代理、验收代理、终审代理不写代码；执行 Agent 不跑 verify/gate 流程；任何角色不删除或修改 contract 文件。

## 调度规则（7条）

1. **自动先行**：P8 每次运行工具前，scan-risk 自动检查目标文件
2. **验证延迟**：P8 声称"任务完成"时，先运行 verify，再运行 gate
3. **裁决独立**：verify 输出不直接给 P8 看——直接给沙悟净做 gate 裁决
4. **否决即停**：gate 被否决 → P8 必须修复，不能绕开 gate 说自己完成
5. **日志必然**：所有 contract/verify/gate/scan-risk 操作写入 `data/harness.md`
6. **重试限制**：同一合同 gate 最多 3 次否决，超过 → 自动升级到 P9 介入。若升级伴随角色切换，执行 [`references/role-switch-protocol.md`](role-switch-protocol.md)
7. **调度间隔**：高频扫描间隔最短 500ms

## 常见作弊面与对策

| 作弊方式 | 对策 |
|---------|------|
| 修改 verify.py 放宽检查 | Git 哈希对比 verify 脚本 |
| 删除 contract 逃避 gate | contract 创建后权限锁定，禁止删除 |
| 绕过 verify 直接 gate | gate 检查 verify 的时间戳和输出完整性 |
| 虚假标"已完成" | P8 声明 ≠ 完成；完成 = gate 通过 |
| 同一个代理既写代码又写 verify | 角色互斥强制隔离 |
| P8 修改测试文件让测试通过 | Git 文件修改记录 + scan-risk 标记测试区 |

## 交付前治理循环

```
P8 完成 coding
  → python scripts/harness-engine.py verify <contract_path>
  → python scripts/harness-engine.py gate <contract_path>
  → 通过：任务完成
  → 否决：分析原因 → 修复 → 重新 verify → 重新 gate
  → 3 次否决：自动升级，通知 P9 介入
```

## 可接受信心定义

P8 在提交交付前，对结果信心做客观评估：

```
可接受信心 = 交付前强检清单（全部必须 ✅）：
  □ 所有验收命令已运行且全部通过（verify 输出为绿）
  □ 所有禁止区文件未被修改（scan-risk 输出为无触碰）
  □ 所有交付物有明确证据（输出、截图或 log）
  □ 无残留 console.log / print / 忽略的错误处理
  □ 无 /tmp 残留 / 未跟踪的临时文件
  □ gate 终审已通过
```
