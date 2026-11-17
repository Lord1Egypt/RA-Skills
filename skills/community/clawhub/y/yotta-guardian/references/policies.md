
# 策略 / 退出码 / 使用姿势（yotta-guardian）

## 一、三档策略

| 策略 | 行为 | 适用场景 |
|---|---|---|
| default（默认） | critical / high 拒绝；medium 警告（exit 1）；low 允许 | 通用默认，安全与可用平衡 |
| strict | critical / high / medium 一律拒绝；low 提示 | 高风险环境、不可逆操作前置检查 |
| loose | 仅 critical 拒绝；high 警告；medium / low 允许 | 需要高可用、仅拦最危险动作 |

放行规则（--allow / --allow-path / ALLOW_PATTERNS / 配置文件 allow）可把 high 降级为警告、medium 降级为允许；**critical 不受放行规则影响**。

## 二、退出码

| 退出码 | 含义 | 对应 |
|---|---|---|
| 0 | 允许（无 finding 或仅 low） | allowed |
| 1 | 允许但带警告 / 严格策略下拒绝 medium | 需人工复核 |
| 2 | 拒绝（high） | denied |
| 3 | 拒绝（critical） | denied |
| 4 | 用法错误 / 致命异常 | error |

AI 智能体判断：退出码非 0 时不要直接执行；2 / 3 一律停下并向用户报告原因。

## 三、判定优先级

1. 确定性规则引擎先跑（文本 + argv + 路径 + 内容）。
2. 放行规则判定（allow 命中可降级，critical 除外）。
3. 策略裁决（default / strict / loose）。
4. 若配置了意图验证器且当前结论为「允许」，再跑验证器（外部或内置启发式），可把允许升级为复核 / 拒绝；已拒绝的调用不跑验证器。

## 四、使用姿势（AI 智能体）

### 执行前 gate

```bash
python3 scripts/yotta_guardian.py check exec --cmd "<待执行命令>" --json
```

- exit 0：执行。
- exit 1：执行但提示用户「护栏给出中危警告」。
- exit 2 / 3：不执行；向用户说明命中规则（rule_ids 与原因）。
- exit 4：命令用法错误，检查参数。

### 批量预检

```bash
python3 scripts/yotta_guardian.py check --batch calls.json --json
```

calls.json 为数组或 {"calls": [...]}，每项含 tool / cmd / path / content / old / new / target。任一被拒时整体退出码取最严重值。

### 授权放行

确有授权的操作（如正规重启、备份清理）用显式放行，而不是绕过检查：

```bash
python3 scripts/yotta_guardian.py check exec --cmd "<命令>" --allow "<模式>"
python3 scripts/yotta_guardian.py check write --path "<路径>" --allow-path "<前缀>"
```

### 审计

```bash
# 检查时落审计
python3 scripts/yotta_guardian.py check exec --cmd "<命令>" --audit-log .yotta-guardian/audit.jsonl

# 查询
python3 scripts/yotta_guardian.py audit --file .yotta-guardian/audit.jsonl --tail 20
python3 scripts/yotta_guardian.py audit --file .yotta-guardian/audit.jsonl --denied --json
```

## 五、JSON 输出结构（check --json）

```json
{
  "tool": "yotta-guardian",
  "version": "0.1.0",
  "policy": "default",
  "summary": { "calls": 1, "allowed": 0, "denied": 1, "exit": 3 },
  "results": [
    {
      "call": { "tool": "exec", "cmd": "..." },
      "verdict": "deny",
      "allowed": false,
      "severity": "critical",
      "reason": "拒绝：...",
      "rule_ids": ["ARG-RM-SYSTEM"],
      "findings": [ { "rule_id": "...", "severity": "critical", "category": "command", "reason": "...", "confidence": 95 } ],
      "verifier": null,
      "exit": 3
    }
  ]
}
```
