# Pattern 6.5: 原子文件写入

## 问题

Ralph stop hook 和外部监控可能同时读写同一个状态文件。直接写入可能导致读到半写的 JSON。

## 原理

先写到临时文件，再原子 rename。`rename` 在 POSIX 文件系统上是原子操作。来自 Claude Code 内部所有状态文件的写入模式。

## 实现

```bash
write_atomic() {
  local target="$1" content="$2"
  local tmp="${target}.${$}.$(date +%s).tmp"
  echo "$content" > "$tmp"
  mv "$tmp" "$target"
}
```

`${$}` 是当前进程 PID，`$(date +%s)` 是时间戳，两者组合确保临时文件名唯一。即使多个进程同时写入，每个进程写自己的临时文件，最终 `mv` 是原子的——读者要么看到旧版本，要么看到新版本，不会看到半写的内容。

## 在本 skill 中的使用

所有状态文件（ralph.json、cancel.json、tool-errors.json、denials.json）都通过这个函数写入。`scripts/ralph-stop-hook.sh` 和 `scripts/ralph-init.sh` 中均使用此模式。
