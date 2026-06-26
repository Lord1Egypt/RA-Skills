# HEARTBEAT.md - 任务恢复自动检查

## 定期检查
- 扫描未完成任务（每2-4小时）
- 提醒用户恢复
- 静默通过无任务时

## 执行脚本
```powershell
# 使用Python版本（编码兼容性更好）
$skillBase = if (Test-Path "$env:APPDATA\winclaw\.openclaw\skills\workspace-organizer") {
    "$env:APPDATA\winclaw\.openclaw\skills\workspace-organizer"
} else {
    "$HOME\.openclaw\skills\workspace-organizer"
}

$checkScript = Join-Path $skillBase "scripts\task-recovery-check.py"
py $checkScript notify
```

## 配置说明
复制到 workspace 根目录（`~/.openclaw/workspace/HEARTBEAT.md`）。
系统在heartbeat时自动执行检查。