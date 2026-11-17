# 测试报告与风险汇总（Reporting & Risk Summary）

> 把测试结果整理成可读的交付物：测试计划、测试矩阵、覆盖率汇总、风险报告。让非技术的干系人也能看懂质量状态。

## 何时使用

- 用户说「生成测试报告」「出个测试计划」「汇总风险」「给个质量门禁结论」
- 测试执行完，需要沉淀文档或向上汇报

## 产出类型

| 产出 | 用途 | 来源 |
|------|------|------|
| 测试计划 | 规划测什么、怎么测 | [scripts/gen_test_plan.py](../scripts/gen_test_plan.py) + [assets/test-plan-template.md](../assets/test-plan-template.md) |
| 测试矩阵 | 接口用例清单 | [scripts/test_matrix.py](../scripts/test_matrix.py) |
| 覆盖率汇总 | 哪些没测到 | [scripts/run_coverage.py](../scripts/run_coverage.py) |
| 风险报告 | 安全/性能/功能风险分级 | 各专项 references 的结果 |

## 测试计划模板

参考 [assets/test-plan-template.md](../assets/test-plan-template.md)，包含：范围、策略（金字塔比例）、环境、用例清单、准入准出标准、风险。

```bash
python3 scripts/gen_test_plan.py --name 支付模块 --features 创建订单,退款,对账
```

## 风险报告格式

按严重级分级，每条含「证据 + 影响 + 建议」：

```markdown
## 风险报告：用户服务 API

### 🔴 高危
- **BOLA 越权**：用用户 A 的 token 可读取用户 B 的订单（GET /orders/{id}）。
  证据：返回 200 且含他人数据。建议：服务端校验资源归属。

### 🟡 中危
- **无速率限制**：/login 高频请求未触发 429。建议：加限流。

### 🟢 低危
- **错误体泄露版本号**：500 响应暴露框架版本。建议：统一错误包装。
```

## 质量门禁结论模板

```markdown
## 质量门禁
- 单元测试覆盖率：核心模块 92% ✅ / 一般 81% ✅
- 关键 E2E：8/8 通过 ✅
- 性能：p95 420ms < 500ms 阈值 ✅
- 安全：1 高危（见风险报告） ❌ → 阻断合并
结论：存在高危安全风险，建议修复后重新评估。
```

## 原则

- 报告面向人：结论先行，证据支撑，不堆原始日志。
- 风险分级用高/中/低，附可复现证据，避免「可能有问题」式模糊表述。
- 与 [references/test-strategy.md](test-strategy.md) 的准入准出标准对齐。

## 相关子技能（L3）

- 测试报告与质量门禁结论的产出动作 → [skills/test-coverage/SKILL.md](../skills/test-coverage/SKILL.md)（质量门禁由测试策略的 CI 门禁消费）
