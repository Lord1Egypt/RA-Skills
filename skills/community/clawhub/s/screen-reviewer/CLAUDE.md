# Screen Reviewer — 电脑行为复盘助手

自动截图 + OCR + AI 每日复盘报告。安装后 Cursor / Claude Code / Codex 均可自动发现。

## 安装

```bash
bash install.sh
```

## 常用命令

```bash
VENV=~/.screen-reviewer/venv/bin/python
SM=scripts/service_manager.py

$VENV $SM start              # 启动截图守护进程
$VENV $SM stop               # 停止
$VENV $SM status             # 查看状态
$VENV $SM pause              # 暂停截图
$VENV $SM resume             # 恢复截图
$VENV $SM report             # 生成昨天的复盘报告
$VENV $SM report 2026-03-22  # 指定日期
$VENV $SM cleanup            # 清理旧截图
$VENV $SM install            # 安装开机自启
```

## 关键路径

| 文件 | 路径 |
|------|------|
| 配置 | `~/.screen-reviewer/config.yaml` |
| 日志 | `~/.screen-reviewer/logs/YYYY-MM-DD.jsonl` |
| 报告 | `~/.screen-reviewer/reports/YYYY-MM-DD-review.md` |
| 截图 | `~/.screen-reviewer/screenshots/YYYY-MM-DD/` |

## 配置

编辑 `~/.screen-reviewer/config.yaml`，可修改截图间隔、AI 提供商、应用黑名单、ROI 分类规则等。
