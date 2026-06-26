# Pattern 6.1: Post-Edit Diagnostics（编辑后即时诊断）

## 问题

Agent 修改文件后，错误在后续工具调用中才暴露。此时 agent 可能已经在错误基础上修改了更多文件，导致错误级联放大。

来源：`parcadei/Continuous-Claude-v3` — PostToolUse hook 实现

## 原理

PostToolUse hook 在每次文件编辑（Write/Edit）后立即运行诊断工具（linter、type checker），在秒级提供反馈。这是"shift-left"策略——在错误扩散前捕获。

## 实现

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash scripts/post-edit-check.sh"
      }]
    }]
  }
}
```

```bash
# post-edit-check.sh
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
[ -z "$FILE" ] && exit 0

case "$FILE" in
  *.py)  pyright "$FILE" 2>&1 | head -5; ruff check "$FILE" 2>&1 | head -5 ;;
  *.ts)  npx tsc --noEmit "$FILE" 2>&1 | head -5 ;;
  *.rs)  cargo check 2>&1 | head -5 ;;
esac
```

## 与 Pattern 2.1（工具错误升级）的关系

Pattern 2.1 处理工具本身执行失败（`cargo build` 找不到命令）。Post-Edit Diagnostics 处理工具执行成功但产出有问题（文件写入成功但引入了类型错误）。

Pattern 2.1 是反应式（错误发生后升级），Pattern 6.1 是预防式（错误扩散前捕获）。

## Tradeoff

- 每次编辑都跑诊断会拖慢执行速度（特别是大项目的 type check）
- 可以只在指定文件类型上启用，或用 `async: true` 异步运行不阻塞
- 诊断工具需要提前安装，否则 hook 本身会失败
