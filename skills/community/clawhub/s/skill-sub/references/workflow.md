# skill-sub 详细工作流程

> 本文档是 SKILL.md 的渐进式补充，详细描述执行流程、里程碑判断规则、三层回退策略。

---

## 完整执行流程

### 创建调用链（create）

AI 执行 7 步流程：

1. **分析意图**：理解用户想串联哪些技能、达成什么目的
2. **读取技能信息**：对每个涉及技能，运行 `skill_extractor.py scan` 提取关键步骤和指令
3. **规划步骤**：确定步骤顺序、依赖关系、并行机会
4. **流程缺口分析**：检查技能衔接处是否存在真实缺口，按以下三条规则判断（**禁止为了打粘连点而主动制造缺口**）

   ### 缺口规则

   | 缺口类型 | 说明 | 示例 | 是否打粘连点 |
   |---------|------|------|------------|
   | **语义缺口** | Skill A 的输出不是 Skill B 需要的输入格式/内容，需要转换 | 代码分析 skill 输出 JSON → 报告生成 skill 需要 Markdown | ✅ 需转换步骤 |
   | **流程缺口** | 用户任务流程中缺少某个环节，且无 skill 覆盖 | 编码→部署之间缺测试阶段，且无测试 skill | ✅ 需补充步骤 |
   | **决策缺口** | 需要人工判断/审批的节点 | 发布审批、PR Merge、方案决策 | ✅ 需人工节点 |
   | **自然衔接** | 两个 skill 输出输入天然匹配，无需额外转换 | 编译→运行测试、生成报告→发送通知 | ❌ 不需要 |

   ### 禁止行为

   - **不要为了有粘连点而故意制造缺口** — 自然衔接的 skill 步骤之间不打
   - **不要用粘连点替代 skill** — 如果一个 skill 能完成，直接用 skill 步骤
   - **不要过度粘连** — 一条调用链中粘连点数量应远少于 skill 步骤数

5. **配置策略**：根据里程碑规则自动判断 + 用户确认调整
6. **流程+结构校验**：自动调用 `chain_flow_validator` 和 `chain_structure_checker` 双重校验，不通过则拒绝保存
7. **展示确认**：展示完整调用链供用户确认（包括里程碑标记、判断依据、粘连点信息）
8. **命名保存**：根据配置决定自动命名或询问用户
5. **展示确认**：展示完整调用链供用户确认（包括里程碑标记和判断依据）
6. **命名保存**：根据配置决定自动命名或询问用户

> **记忆参考（配置启用时）**：在步骤2后，读取 MEMORY.md 和近期日志，提取用户偏好和习惯，用于增强步骤描述的个性化。

### 预生成（suggest）

扫描已安装技能，推荐常用或相关的技能组合：

```bash
python {SKILL_DIR}/scripts/skill_extractor.py scan
```

### 查询（list / show）

```bash
# 列出所有调用链
python {SKILL_DIR}/scripts/chain_manager.py list
python {SKILL_DIR}/scripts/chain_manager.py list --tag "发布"

# 查看详情（含里程碑判断依据）
python {SKILL_DIR}/scripts/chain_manager.py show --name "发布流水线"

# 查看当前配置
python {SKILL_DIR}/scripts/chain_manager.py config
```

### 执行（run）

三步执行流程：

1. **生成执行计划**：`chain_executor.py plan --name <名称>`
2. **按计划执行**：AI 读取执行计划，逐步执行
3. **汇报结果**：每步执行后汇报 ✅/❌，里程碑步骤失败则中止

### 调整（edit）

```bash
# 添加步骤
python {SKILL_DIR}/scripts/chain_manager.py add-step --name "链名" --after 1 --skill "技能名" --step-name "步骤名" --action "动作"

# 删除步骤
python {SKILL_DIR}/scripts/chain_manager.py remove-step --name "链名" --step 3

# 更新步骤
python {SKILL_DIR}/scripts/chain_manager.py update-step --name "链名" --step 2 --action "新动作"
python {SKILL_DIR}/scripts/chain_manager.py update-step --name "链名" --step 1 --milestone
python {SKILL_DIR}/scripts/chain_manager.py update-step --name "链名" --step 3 --no-milestone
python {SKILL_DIR}/scripts/chain_manager.py update-step --name "链名" --step 1 --retry-max 5
python {SKILL_DIR}/scripts/chain_manager.py update-step --name "链名" --step 2 --on-exhaust abort

# 重命名
python {SKILL_DIR}/scripts/chain_manager.py rename --name "旧名" --new-name "新名"
```

### 删除（delete）

```bash
python {SKILL_DIR}/scripts/chain_manager.py delete --name "链名" --force
```

---

## 循环与分支编排（v1.20.0 新增）

### for-each 循环

`type: "loop"` + `"mode": "for_each"`：遍历数组，对每个元素执行循环体。

```json
{
  "type": "loop",
  "step_name": "批量处理",
  "loop": {
    "mode": "for_each",
    "items": "{{file_list}}",
    "loop_variable": "f",
    "max_iterations": 10,
    "steps": [
      {"type": "skill", "skill_name": "file-ops", "action": "处理 {{f}}"}
    ]
  }
}
```

### while 循环

`type: "loop"` + `"mode": "while"`：按条件重复执行，直到条件为假或达到最大次数。

```json
{
  "type": "loop",
  "step_name": "重试直到成功",
  "loop": {
    "mode": "while",
    "while_condition": "{{retry_count}} < 3 and {{last_success}} == false",
    "max_iterations": 3,
    "steps": [
      {"type": "skill", "skill_name": "api-call", "action": "重试"}
    ]
  }
}
```

### if-else 分支

`type: "branch"`：根据条件选择执行 `if_steps` 或 `else_steps`。

```json
{
  "type": "branch",
  "step_name": "按环境部署",
  "branch": {
    "condition": "{{env}} == 'prod'",
    "if_steps": [
      {"type": "skill", "skill_name": "deploy", "action": "部署到生产"}
    ],
    "else_steps": [
      {"type": "skill", "skill_name": "deploy", "action": "部署到预发"}
    ]
  }
}
```

> 📚 完整 schema 参见 `chain_schema.md`

---

## 里程碑通用判断规则

> **设计原则**：不完全依赖 AI 自觉判断，基于步骤的**结构特征**自动确定里程碑。

### 判断规则（优先级从高到低）

| 优先级 | 规则 | 说明 | 示例 |
|--------|------|------|------|
| 1 | 用户显式标记 | `is_milestone=true` | 用户手动指定 |
| 2 | 显式取消 | `is_milestone=false` | 用户明确不需要 |
| 3 | 短链全部标记 | 总步骤数 ≤ 2 → 全部里程碑 | 链太短，每步都关键 |
| 4 | 关键词匹配 | 步骤名包含特定关键词 → 里程碑 | "安全审计"、"部署上线" |
| 5 | 瓶颈点 | 被 ≥2 个后续步骤依赖 → 里程碑 | 多个步骤依赖该步骤的输出 |
| 6 | 最终交付 | 是最后一步 → 里程碑 | 最终产出物 |
| 7 | 默认非里程碑 | 以上均不满足 | 辅助/中间步骤 |

### 里程碑关键词

中英文关键词（步骤名包含任一即匹配）：

```
审计、安全、部署、发布、上线、打包、测试、验证、校验、审批、审核、
付款、支付、下单、提交、推送、导入、导出、迁移、备份、恢复、
audit、deploy、release、publish、push、test、verify、validate、
approve、review、payment、submit、import、export、migrate、
backup、restore、build、compile、install
```

### 里程碑行为

- **里程碑步骤失败** → 无论 `on_exhaust` 配置如何，**强制中止整条链**
- **里程碑步骤的 on_exhaust** → 建议设为 `abort`（validate 时会发出警告）
- **非里程碑步骤失败** → 按 `on_exhaust` 配置处理（ask/skip/abort）

---

## 三层回退执行策略

| 层次 | 策略 | 上下文占用 | 触发条件 |
|------|------|-----------|---------|
| **第一层** | 仅用 action 精炼描述直接执行 | 最低 | 默认，action 足够明确 |
| **第二层** | 按需读取 SKILL.md 对应指令片段 | 中等 | action 不明确或执行失败 |
| **第三层** | 加载完整 SKILL.md | 最高 | 前两层均无法完成 |

---

## 分级重试策略

| 错误类型 | 重试间隔 | 说明 |
|---------|---------|------|
| file_locked | 0 秒 | 文件占用/锁定，立即重试 |
| network_error | 5 秒 | 网络不通/超时 |
| timeout | 5 秒 | 执行超时 |
| auth_error | - | 认证/权限错误，直接询问用户 |
| other | 2 秒 | 其他错误 |

重试次数从配置读取（默认3次），耗尽后按 `on_exhaust` 处理。

---

## AI 执行指令（必读原则）

1. **执行前通读调用链**：读取整条链的所有步骤，理解全局依赖关系
2. **三层回退**：每个步骤优先用 action 执行，不充分时再读取 SKILL.md
3. **里程碑步骤失败立即中止**：不继续后续步骤
4. **非里程碑步骤失败按 on_exhaust 处理**：ask（询问）/ skip（跳过）/ abort（中止）
5. **记录变量传递**：步骤输出变量作为后续步骤输入
6. **命名遵循配置**：`naming_mode=auto` 时 AI 自动命名，`manual` 时询问用户

---

## 配置界面

### 配置项说明

| 配置项 | 选项 | 说明 |
|--------|------|------|
| **记忆参考** | 是 / 否 | 创建/执行调用链时，是否读取用户记忆文件增强步骤描述 |
| **命名方式** | 自动 / 人工 | 创建调用链时，由 AI 自动命名还是询问用户 |
| **默认重试次数** | 1-10（默认3） | 所有步骤的默认最大重试次数 |

### 当前配置

> **配置路径**：`~/.workbuddy/skills/.standardization/skill-sub/config.json`
> **默认配置**：`{skill_dir}/scripts/default_config.json`

**方式 1：HTML 配置界面（推荐）**

Agent 执行：
1. 运行 `python {SKILL_DIR}/scripts/settings.py --serve-only`
2. 解析输出中的 `SERVER_STARTED:<port>`
3. 打开浏览器 `http://localhost:{port}/`
4. 轮询 `{SKILL_DIR}/.settings_done` 标志文件
5. 检测到标志文件后关闭服务器

**方式 2：命令行查看**

```bash
python {SKILL_DIR}/scripts/settings.py --get-config
```

**方式 3：命令行保存**

```bash
python {SKILL_DIR}/scripts/settings.py --save-config '{"use_memory_reference": true, "naming_mode": "auto", "default_max_retries": 5}'
```

**方式 4：对话式配置（回退方案）**

当 HTML 配置界面无法打开时，通过对话方式收集配置：

```
步骤 1：记忆参考
是否在创建调用链时参考用户记忆文件？（输入 y/n）:

步骤 2：命名方式
调用链命名方式（输入 1/2 选择）：
1. 自动 — AI 根据意图和目的自动生成名称
2. 人工 — 每次创建时询问用户
请输入：

步骤 3：默认重试次数
请输入默认最大重试次数（1-10，默认3）:

步骤 4：保存
Agent 执行: python settings.py --save-config '<json>'
```
