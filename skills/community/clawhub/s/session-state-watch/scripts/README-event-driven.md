# 实时事件驱动模式（可选增强）

> 使用 Linux inotify 实现实时文件变更检测。

## 前提条件

```bash
# Debian/Ubuntu
apt install inotify-tools

# CentOS/RHEL
yum install inotify-tools

# Arch
pacman -S inotify-tools
```

## 使用方式

```bash
# 启动实时监控（前台）
bash scripts/check_session_state.sh --watch

# 启动实时监控（后台守护）
nohup bash scripts/check_session_state.sh --watch --daemon > /tmp/session-state-watch.log 2>&1 &

# 停止守护
bash scripts/check_session_state.sh --stop-daemon
```

## 工作原理

`--watch` 模式使用 `inotifywait -m -e close_write` 监控 `SESSION-STATE.md`，
在文件被关闭写入时立即检查。与 mtime 轮询完全兼容，可同时使用。

## 注意

- inotify 需要 inotify-tools 包
- 守护进程需要手动管理（systemd 或 nohup）
- 系统重启后需要重新启动守护
