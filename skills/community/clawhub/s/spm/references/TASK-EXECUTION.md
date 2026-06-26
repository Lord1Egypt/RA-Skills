# Task Execution — 单任务执行单一入口

> **何时读：执行任何一个 WBS 任务前必读。** 本文件是所有执行规则的合并入口——读完这份就够了。

---

## 开工 3 问（Self-Prompting）

每个任务动手前先问自己：

1. **这个任务的退出标准是什么？**（查 WBS 台账 `exit_criteria` 列）
2. **它的依赖都 `done` 了吗？**（查 WBS 台账 `Dependencies` 列）
3. **Context Brief 说了什么？**（自包含的冷启动上下文——前置产物、涉及文件、关键约束）

---

## 铁律速查

| # | 铁律 | 含义 |
|---|------|------|
| 1 | 无批准设计不写代码 | Phase 1/2 必须用户审批通过 |
| 2 | 无失败测试不写生产代码 | RED → GREEN → REFACTOR |
| 3 | 无新鲜验证不报完成 | 本次会话跑过命令才算数 |
| 4 | 无根因分析不行修复 | Symptom fix = 失败 |
| 5 | 无证据不标 done | WBS done 必须附验证输出 |

---

## 执行流程（单任务）

### 代码项目 (project_type: code)

```
1. 读 WBS 台账 → 确认任务 ID、Context Brief、退出标准、依赖
2. 📊 跑 Baseline：npm test 保存执行前测试基线
3. 更新台账: status=doing
4. TDD: RED → Verify RED → GREEN → Verify GREEN → REFACTOR
5. 自检：跑本文件末尾"完工自检清单"
6. 修完自检 fail 项 → commit
7. 📊 跑 Eval Delta：对比 baseline vs current → 确认无回归
8. 更新台账: status=done + 附证据
9. 向主编汇报
```

### 非代码项目 (project_type: docs | config)

```
1. 读 WBS 台账 → 确认任务 ID、Context Brief、退出标准、依赖
2. 更新台账: status=doing
3. 执行变更 + 格式验证（bash -n / yamllint / json.load）
4. 一致性验证（Schema↔YAML对齐、交叉引用有效）
5. 功能验证（脚本可运行、命令可执行）
6. 自检：跑本文件末尾"完工自检清单"（跳过 TDD 项）
7. 修完自检 fail 项 → commit
8. 更新台账: status=done + 附证据
9. 向主编汇报
```

### 阻塞处理

如果任务阻塞（BLOCKED），按计划突变协议处理：
- 任务太大 → **split** 拆分
- 缺前置工作 → **insert** 插入新任务
- 不再需要 → **skip** 跳过
- 方向错误 → **abandon** 废弃

所有突变 MUST 记录到 WBS 台账的 Mutation Log。详见 `references/plan-mutation.md`。

---

## TDD 硬规则

> ⚠️ 非代码项目（`project_type: docs` 或 `config`）跳过 TDD。改用格式验证替代。

### 代码项目 (project_type: code) — 标准 TDD

### RED — 写失败测试
- 一个测试、一个行为、名字清晰
- 运行确认它**失败且原因正确**（功能缺失，不是拼写错误）

### Verify RED — 强制

**有效的 RED 有两种形式（🆕 取自 ECC tdd-workflow）：**

1. **运行时 RED**：测试编译成功、执行、返回失败——因为功能还没实现
2. **编译时 RED**：测试引用了不存在的 API/函数/类型 → 编译失败本身就是有效的 RED 信号

```bash
npm test path/to/test.test.ts
```
测试直接通过？说明你在测已有功能——改测试。
测试报错？修错误，跑到它正确失败为止。

**两者都算有效 RED——只要失败是由功能缺失或 bug 导致的，不是由语法错误或错误的测试配置导致的。**

### GREEN — 最小实现
写最简代码让测试通过。不加额外功能（YAGNI）。

### Verify GREEN — 强制
```bash
npm test path/to/test.test.ts
```
确认：新测试通过。其他测试依然通过。

### REFACTOR — 仅在绿色时
清理代码。保持测试绿色。不改变行为。

### Commit
```bash
git add -A && git commit -m "feat(scope): 简短描述"
```

### 非代码项目 (project_type: docs | config) — 格式验证替代

非代码项目不写测试，改用以下格式验证：

```
1. 格式验证：
   - Markdown: 无断链、无格式错误
   - YAML: yamllint 或 python3 -c "import yaml; yaml.safe_load(open('f'))"
   - JSON: python3 -c "import json; json.load(open('f'))"
   - Shell: bash -n script.sh

2. 一致性验证：
   - Schema ↔ YAML 字段对齐
   - 交叉引用有效（所有文件路径引用指向存在的文件）
   - 示例数据与 Schema 兼容

3. 功能验证（技能/文档项目）：
   - 所有脚本在测试项目中可运行
   - 所有命令示例可执行
   - 所有模板可填充并生成有效输出

4. Commit:
   git add -A && git commit -m "feat(scope): 简短描述"
```

**铁律同代码项目：无验证不标 done。** 只是验证方式从"跑测试"变为"跑格式检查 + 功能验证"。

---

## 验证门（Gate Function）

声明任何完成状态前：

```
1. IDENTIFY: 什么命令能证明这个声明？
2. RUN: 完整执行（不能拿上次运行的结果凑数）
3. READ: 完整读输出、检查 exit code、数失败数
4. VERIFY: 输出确认了声明吗？
5. ONLY THEN: 做出声明

跳过任何一步 = 撒谎，不是验证
```

---

## 常见反模式（Stop and Start Over）

如果你发现自己：

- ❌ 写了代码再补测试 → 删掉代码，从 RED 开始
- ❌ 测试第一次就通过 → 你在测已有功能，改测试
- ❌ 说不清测试为什么失败 → 回去理解功能
- ❌ "我待会再测" → 现在就测
- ❌ "应该能通过" → 跑命令，看结果
- ❌ "上次跑过了" → 本次没跑＝没验证
- ❌ "看起来没问题" → 视觉检查不算验证
- ❌ 同时改 3 个不相关的东西 → 切小，一次一个

---

## WBS 台账更新规则

| 时机 | 动作 |
|------|------|
| 开始执行 | `status=doing` |
| 完成（自检通过） | `status=done` + 证据列填验证命令输出 |
| 阻塞 | `status=blocked` + 描述阻塞原因 + 更新心跳日志 |
| 跳过 | `status=skipped` + 注明跳过原因 |

**证据格式要求：**
```
Task 2 完成。
证据: `npm test` → 47/47 pass, exit 0
```

---

## 子代理报告模板

```markdown
## Task [ID]: [任务名]

**Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

### 实现内容
[简述做了什么]

### 测试结果
```
📊 Eval Delta — Task [ID]
Baseline:  [N] tests | [X]% pass | [Y]% coverage
Current:   [M] tests | [A]% pass | [B]% coverage
Delta:     +[M-N] tests | [regressions] regressions | +[B-Y]% coverage

[粘贴实际测试输出]
```

### 修改文件
- `src/path/file.ts` — 简述改了什么
- `tests/path/file.test.ts` — 新增测试

### 自检结果
- [ ] 退出标准全部满足
- [ ] 测试覆盖新增代码
- [ ] 无 console.log / TODO / 硬编码密钥
- [ ] 遵循项目命名和代码风格

### 问题 / 顾虑
[如有]
```

---

## 完工自检清单

每个任务标记 `done` 前，逐项过：

### 正确性
- [ ] 退出标准全部满足（对照 WBS 台账逐条核对）
- [ ] 边界情况处理（null、空值、异常路径）
- [ ] 错误信息有意义（不暴露栈跟踪给用户）
- [ ] 硬编码值已提取到配置或常量

### 测试
- [ ] 新增功能有测试
- [ ] 边界情况有覆盖
- [ ] 测试独立且快速
- [ ] 全量测试套件通过（本会话内跑过）

### 代码质量
- [ ] 无 console.log（仅允许 logger.*）
- [ ] 无 TODO / FIXME / HACK
- [ ] 无硬编码密钥或令牌
- [ ] 函数 ≤ 50 行（长了就拆）
- [ ] 变量名有意义（禁止 data、temp、x）

### 台账
- [ ] status 已更新为 `done`
- [ ] evidence 列有可验证的证据
- [ ] 心跳日志已更新

**自检 fail 项 → 修完再报完成。直接拿 fail 结果汇报 = 违规。**
