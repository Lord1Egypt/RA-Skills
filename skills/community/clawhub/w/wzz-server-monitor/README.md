# wzz-server-monitor — 服务器资源监控通知 Skill

监控 CPU / 内存 / 磁盘使用率，超过阈值时通过 SMTP 发送邮件告警。支持可配置阈值、发送时间窗口、通知频率（防刷屏）和邮件文案模板。核心脚本由 cron 独立运行，**不依赖任何 AI Agent**。

## 特性

- ✅ CPU / 内存 / 多路径磁盘监控，阈值可配置
- ✅ SMTP 直连发送（SSL / TLS），支持国内邮箱（QQ / 163 授权码）
- ✅ 通知频率控制：状态变化去重 + cooldown 节流 + 单日上限
- ✅ 可配置发送时间窗口（窗口外静默、状态照记、开窗补发）
- ✅ Jinja2 邮件模板（可自定义文案；缺失时回退标准库）
- ✅ 跨 Agent 通用（遵循 Agent Skills 开放标准，Claude Code / Codex 可用）
- ✅ cron 独立运行，Agent 掉线不影响监控

## 快速开始

```sh
# 1. 初始化（检查依赖、生成配置模板）
python3 scripts/monitor.py setup

# 2. 编辑 ~/.config/resource-monitor/config.yaml，填入 SMTP 与阈值
#    SMTP 密码写入 ~/.config/resource-monitor/.smtp_secret（chmod 600）

# 3. 校验 + 测试 + 安装定时任务
python3 scripts/monitor.py validate-config
python3 scripts/monitor.py send-test
bash assets/install.sh
```

## 命令一览

| 命令 | 说明 |
|------|------|
| `monitor.py setup` | 首次初始化（依赖检查、生成目录与配置模板） |
| `monitor.py check` | 单次检查（cron 入口）；`--now` 绕过窗口；`--dry-run` 只打印决策 |
| `monitor.py status` | 查看当前指标快照与状态 |
| `monitor.py send-test` | 发送测试邮件 |
| `monitor.py validate-config` | 校验配置；`--smtp-connect` 额外做 SMTP 握手 |
| `monitor.py reset-state` | 重置告警状态 |

## 目录结构

```
wzz-server-monitor/
├── SKILL.md                  # 使用文档 + Agent 交互入口
├── LICENSE                   # MIT
├── README.md
├── scripts/
│   └── monitor.py            # 核心监控脚本
└── assets/
    ├── config.example.yaml   # 配置模板
    ├── install.sh            # 一键安装辅助
    └── templates/            # 邮件文案模板（jinja2）
```

运行时数据位于用户本地（不受 skill 更新影响）：`~/.config/resource-monitor/`（配置 + 密码）与 `~/.local/state/resource-monitor/`（状态 + 日志）。

## 依赖

- Python ≥ 3.9
- `psutil`、`pyyaml`、`jinja2`

```sh
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil pyyaml jinja2
```

## 配置

完整字段说明见 `assets/config.example.yaml` 与 [SKILL.md](SKILL.md#5-配置参考)。核心概念：

- **通知频率**：`cooldown_minutes`（两次实际发送最小间隔）+ 状态变化去重 + `daily_cap`（单日上限）
- **时间窗口**：`window.rules`，如 `09:00-22:00`；窗口外静默但状态照记，开窗后补发
- **模板**：`templates.alarm` / `templates.recovery`，Jinja2，变量白名单见 SKILL.md

## 在其他 Agent 中使用（Codex 等）

本 skill 遵循 Agent Skills 开放标准，Claude Code 与 Codex 均识别。将目录软链到目标 Agent 的 skills 路径：

```sh
mkdir -p ~/.codex/skills        # 或 .agents/skills
ln -s /path/to/wzz-server-monitor ~/.codex/skills/wzz-server-monitor
```

监控本身由 cron 驱动，即使不经任何 Agent 也可独立工作。

## 许可

ClawHub 发布统一采用 [MIT-0](https://opensource.org/license/mit-0) 许可。
