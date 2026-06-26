# 缺陷模式统一 Schema（L4 缺陷库）

> 版本：v1.0.0 | 创建日期：2026-04-19 | 作者：小猿（test_codingworker）
> 本文档定义 L4 缺陷模式库的统一数据 schema，所有缺陷条目必须符合此规范。

---

## Schema 定义

每条缺陷模式记录必须包含以下字段：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `defect_id` | string | ✅ | 缺陷模式唯一标识，格式：`DP-{domain}-{seq}`，如 `DP-TRADE-001` |
| `domain` | string | ✅ | 业务域，枚举值：trade / clearing / asset_mgmt / risk_ctrl / compliance / crm / platform / derivatives / investment_banking / data |
| `module_path` | string | ✅ | 模块路径，格式：`{系统}/{子系统}/{模块}`，如 `交易系统/委托管理/限价委托` |
| `symptom` | string | ✅ | 缺陷症状描述（用户可观测的异常表现） |
| `root_cause` | string | ✅ | 根因分析（代码/设计/架构层面的本质原因） |
| `trigger_condition` | string | ✅ | 触发条件（精确描述在什么输入/状态/时序下触发） |
| `affected_state` | string | ✅ | 受影响状态（缺陷发生时系统所处的状态或状态转移） |
| `reproduction_summary` | string | ✅ | 复现摘要（最小复现步骤，3-5步） |
| `test_hint` | string | ✅ | 测试点提示（针对此缺陷的回归测试建议） |
| `negative_pattern` | string | ✅ | 反例排除条件（描述哪些相似场景不属于此缺陷模式） |
| `severity` | string | ✅ | 严重程度：critical / major / minor / trivial |
| `defect_type` | string | ✅ | 缺陷类型：functional / performance / security / data / ui / reliability / integration / compatibility |
| `fix_pattern` | string | ❌ | 修复模式（通用修复方案描述） |
| `related_defects` | list[string] | ❌ | 关联缺陷ID列表 |
| `tags` | list[string] | ❌ | 标签（如：并发、状态机、边界值、幂等） |
| `created_at` | string | ✅ | 创建时间，ISO 8601 格式 |
| `source_project` | string | ❌ | 来源项目名称 |

---

## Schema JSON 格式

```json
{
  "defect_id": "DP-TRADE-001",
  "domain": "trade",
  "module_path": "交易系统/委托管理/限价委托",
  "symptom": "用户快速双击提交按钮后产生两笔相同委托，资金被双倍冻结",
  "root_cause": "前端未做防重处理，后端幂等键校验存在时间窗口（先查后写非原子操作）",
  "trigger_condition": "用户在200ms内连续点击提交按钮2次，且后端两个请求落在不同的应用实例上",
  "affected_state": "委托状态 PendingSubmit → Submitted 产生两条记录",
  "reproduction_summary": "1. 登录交易账户 2. 选择股票下限价买入单 3. 快速双击提交按钮 4. 查看委托列表，出现两笔相同委托",
  "test_hint": "验证 clientOrderId 幂等键在分布式场景下的原子性，使用数据库唯一索引而非先查后写",
  "negative_pattern": "用户主动提交两笔不同价格/数量的委托不属于此模式；网络重传导致的重复请求由网关层去重，不属于此模式",
  "severity": "critical",
  "defect_type": "functional",
  "fix_pattern": "数据库唯一索引 + INSERT ON CONFLICT 原子操作替代先查后写",
  "related_defects": ["DP-TRADE-002"],
  "tags": ["并发", "幂等", "防重"],
  "created_at": "2026-04-19T00:00:00+08:00",
  "source_project": "差异化交易SMT"
}
```

---

## 字段完整性校验规则

1. 所有必填字段不得为空字符串
2. `domain` 必须是枚举值之一
3. `module_path` 至少包含两级路径（`/` 分隔）
4. `trigger_condition` 必须包含具体的输入条件或状态前提，不得使用"某些情况下"等模糊描述
5. `reproduction_summary` 必须是可执行的步骤（编号列表），步骤数 3-7 步
6. `negative_pattern` 必须明确排除至少一种相似但不同的场景
7. `severity` 与 `defect_type` 必须是枚举值之一
8. `affected_state` 必须引用具体的状态名称或状态转移路径

---

## 与现有 JSONL 文件的兼容说明

现有 `defects_by_type/` 和 `defects_by_domain/` 目录下的 `.txt` 文件为历史数据，后续新增缺陷条目应遵循本 schema。历史数据迁移计划：

1. 第一阶段：新增条目强制遵循 schema
2. 第二阶段：逐步补充历史条目的 `root_cause`、`trigger_condition`、`affected_state`、`negative_pattern` 字段
3. 第三阶段：全量数据符合 schema 后，启用字段完整性校验门禁

---

## 使用场景

- 测试用例生成引擎：根据 `trigger_condition` + `test_hint` 自动生成回归测试用例
- 缺陷预测：根据 `module_path` + `tags` 预测高风险模块
- 知识召回：根据 `symptom` + `root_cause` 进行语义匹配，辅助缺陷定位
- 反例排除：根据 `negative_pattern` 避免误报
