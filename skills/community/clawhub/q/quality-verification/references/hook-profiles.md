# Pattern 6.2: Hook Runtime Profiles（环境级 hook 强度控制）

## 问题

所有 hook 以相同强度在所有场景下运行。快速实验需要最小 overhead，生产部署需要最大保障，但 hook 配置只有一套。

来源：`affaan-m/everything-claude-code` — ECC_HOOK_PROFILE 环境变量

## 原理

通过环境变量控制 hook 行为强度，无需修改 settings.json。同一套 hook 配置在不同环境下表现不同。

### 三个 Profile

| Profile | 启用的 Pattern | 适用场景 |
|---------|---------------|---------|
| `minimal` | 仅 Pattern 6.5（原子写入）| 快速实验、探索性编码 |
| `standard` | Pattern 1.1/2.1/3.5/6.5 | 日常开发 |
| `strict` | 全部 Pattern | 生产变更、安全修复、正式 review |

### 细粒度控制

```bash
# Profile 级别
export HARNESS_PROFILE=strict

# 单个 hook 级别
export HARNESS_DISABLED_HOOKS=doubt-gate,post-edit-diagnostics
```

## 实现

每个 hook 脚本的入口处检查 profile：

```bash
#!/usr/bin/env bash
PROFILE="${HARNESS_PROFILE:-standard}"

# 此 hook 需要 strict 或更高
case "$PROFILE" in
  strict) ;; # 继续执行
  *) echo '{"continue":true}'; exit 0 ;; # 跳过
esac

# 检查是否被单独禁用
DISABLED="${HARNESS_DISABLED_HOOKS:-}"
if echo ",$DISABLED," | grep -q ",$(basename "$0" .sh),"; then
  echo '{"continue":true}'; exit 0
fi

# ... hook 的实际逻辑 ...
```

## 与 Pattern 1.3（Adaptive Complexity）的关系

Pattern 1.3 根据任务复杂度自动选择 pattern 组合。Pattern 6.2 根据环境/意图手动选择 hook 强度。两者可以组合：`HARNESS_PROFILE=strict` + adaptive complexity = "strict 模式下，仍然根据任务复杂度微调具体启用哪些 pattern"。

## Tradeoff

- 增加了一层间接性——debug 时需要知道当前 profile 是什么
- 需要每个 hook 脚本都加入 profile 检查代码
- Profile 语义需要团队达成共识——"standard"对不同人可能意味着不同的东西
