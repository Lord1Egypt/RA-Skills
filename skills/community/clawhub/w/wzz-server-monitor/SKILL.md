---
# 通用字段（Agent Skills 开放标准；name 与父目录名一致）
name: wzz-server-monitor
description: 监控服务器 CPU/内存/磁盘使用率，超过配置阈值时通过 SMTP 发送邮件告警。支持可配置阈值、通知时间窗口、发送频率（防刷屏）和邮件文案模板。当用户询问服务器资源、负载、告警、监控通知、设置或查看资源监控时使用。Make sure to use whenever the user asks about server resource monitoring, load, or email alerts.
version: 1.0.0

# ClawHub 运行时元数据
metadata:
  openclaw:
    os: ["linux"]
    requires:
      bins: [python3]
      config: [~/.config/resource-monitor/config.yaml]
    emoji: "📊"

# Claude Code 增强字段（其他 agent / ClawHub 忽略，不影响可移植性）
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash(monitor.py *)
  - Bash(crontab *)
---

# wzz-server-monitor — 服务器资源监控通知

监控 CPU / 内存 / 磁盘使用率，超过阈值时通过 SMTP 发送邮件告警。**核心脚本由 cron 独立定时运行，与任何 AI Agent 无关**；本 SKILL.md 是配置文档和交互入口。

## 1. 快速开始

新用户三步完成：

1. **初始化**（检查依赖、生成配置目录与模板）：

   ```sh
   python3 <skill-dir>/scripts/monitor.py setup
   ```

2. **编辑配置** `~/.config/resource-monitor/config.yaml`，填入：
   - `smtp`：SMTP 服务器、账号、授权码（国内邮箱 QQ/163 均可；QQ 用「授权码」而非登录密码）
   - `metrics`：CPU/内存/磁盘阈值
   - `window`：允许发送的时间窗口（可选）
   - `cooldown_minutes`：通知频率（可选）

   SMTP 密码建议写入独立文件 `~/.config/resource-monitor/.smtp_secret`（`chmod 600`），配置文件只引用路径。

3. **校验 + 安装定时任务**：

   ```sh
   python3 <skill-dir>/scripts/monitor.py validate-config
   python3 <skill-dir>/scripts/monitor.py send-test       # 收一封测试邮件
   bash <skill-dir>/assets/install.sh                     # 自动写入 crontab
   ```

> **Claude 交互**：用户说「看下服务器负载」→ 运行 `status`；「测一下告警邮件」→ `send-test`；「帮我配置监控」→ 引导用户完成 `setup` + 编辑 `config.yaml` + `validate-config` + `send-test`。

## 2. 依赖

- Python ≥ 3.9
- `psutil`、`pyyaml`、`jinja2`（第三方，安装时可用国内镜像加速）

```sh
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil pyyaml jinja2
```

模板渲染优先 jinja2；缺失时脚本自动回退到 Python 标准库 `string.Template`，功能不中断。

## 3. 文件布局

**skill 目录**（随版本更新，只读）：

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 本文档 |
| `scripts/monitor.py` | 核心监控脚本（cron 直接调用） |
| `assets/config.example.yaml` | 配置模板 |
| `assets/install.sh` | 一键安装辅助 |
| `assets/templates/*.html` | 邮件文案模板 |

**运行时数据**（用户环境，不受 skill 更新影响）：

| 路径 | 说明 |
|------|------|
| `~/.config/resource-monitor/config.yaml` | 用户配置 |
| `~/.config/resource-monitor/.smtp_secret` | SMTP 密码（chmod 600） |
| `~/.local/state/resource-monitor/state.json` | 运行状态（告警去重/节流） |
| `~/.local/state/resource-monitor/monitor.log` | 运行日志 |

## 4. 发送决策模型

一份邮件聚合列出所有超限指标（不是每项一封）。状态机基于 `state.json`：

- **状态变化去重**：只有指标从「正常 → 超限」才进入告警状态；恢复后重置，下次超限重新计时。
- **cooldown 节流**：同一告警两次实际发送之间强制最小间隔 `cooldown_minutes`，防止刷屏。
- **单日上限**：`daily_cap` 限制当日发送总数，防止异常失控。
- **时间窗口**：`window.rules` 之外即使超限也静默不发，但**状态照常记录、不推进上次发送时间**——窗口一打开的第一轮检查就会补发（夜间超限、早上准时收到）。
- **恢复通知**：`recovery: true` 时，恢复正常会发一封恢复邮件（受 cooldown 与窗口约束）。

决策优先级：冷却期内 → 当日已达上限 → 窗口外静默 → 发送。

## 5. 配置参考

见 `assets/config.example.yaml`（带注释的完整示例）。校验命令：

```sh
python3 <skill-dir>/scripts/monitor.py validate-config --smtp-connect
```

`--smtp-connect` 会额外执行 SMTP 连接与认证握手（不发信）。

## 6. 模板编写

模板文件在 `assets/templates/`，使用 Jinja2 语法。可在 `config.yaml → templates` 修改主题与正文文件名。

**暴露给模板的变量白名单**（SMTP 凭据绝不会进入模板上下文）：

| 变量 | 说明 |
|------|------|
| `hostname` | 服务器名（`hostname_label` 或系统主机名） |
| `timestamp` | 本地时间 `YYYY-MM-DD HH:MM:SS` |
| `status` | `alarm` / `recovery` / `test` |
| `alarm_count` | 超限指标个数 |
| `alarms` | `[{metric, current, threshold, path}]` 超限指标列表 |
| `metrics` | 全量指标 `{key: {percent, threshold, path}}` |
| `uptime` | 运行时长（timedelta） |
| `load_avg` | `psutil.getloadavg()` 三元组 |

subject 同样支持模板变量，如 `[{{ hostname }}] 资源告警 ({{ alarm_count }}项)`。

## 7. cron

脚本由 cron 定时运行，**每 5 分钟一次全天运行**；时间窗口在脚本内过滤（二者正交，改窗口不影响 cron）。

```
*/5 * * * * /usr/bin/python3 ~/.claude/skills/wzz-server-monitor/scripts/monitor.py check --config ~/.config/resource-monitor/config.yaml >> ~/.local/state/resource-monitor/monitor.log 2>&1
```

- 使用绝对路径 `python3`，不依赖 cron 的 PATH。
- 检查频率决定「多久看一次」，通知频率由 `cooldown_minutes` 控制。
- `bash assets/install.sh` 可自动写入并去重 crontab。

### WSL2 / 容器 cron 自启

WSL2 与多数容器默认不启动 cron 服务。手动启动：

```sh
sudo service cron start
```

开机自启（WSL2）：编辑 `/etc/wsl.conf`：

```ini
[boot]
command = service cron start
```

## 8. 日常维护

| 需求 | 命令 |
|------|------|
| 查看当前指标与状态 | `monitor.py status` |
| 手动触发一次检查 | `monitor.py check --dry-run`（只打印决策） |
| 绕过窗口测试 | `monitor.py check --now` |
| 重置告警状态 | `monitor.py reset-state` |
| 修改配置后校验 | `monitor.py validate-config` |

日志位置 `~/.local/state/resource-monitor/monitor.log`，长跑后手动截断（`> log`）。

## 9. 故障排查

| 现象 | 排查 |
|------|------|
| SMTP 认证失败 | QQ/163 邮箱必须用「授权码」（设置里生成）而非登录密码；检查 `security`/`port` 是否匹配（ssl=465, tls=587） |
| 日志为空 | 检查 cron 服务是否运行（WSL2 见上）；`crontab -l` 确认条目 |
| CPU 恒为 0% | cron 每轮是全新进程，`cpu_interval` 必须 > 0（默认 0.5） |
| 窗口内仍没收到 | `validate-config` 确认时间格式；`status` 查看 `window: 开/关` |
| 不想收到重复告警 | 调大 `cooldown_minutes` 或开启 `recovery` 恢复通知 |

## 10. 在其他 Agent 中使用（Claude / Codex 等）

本 skill 遵循 **Agent Skills 开放标准**，核心格式（SKILL.md + YAML frontmatter + Markdown）在 Claude Code、OpenAI Codex、Cursor 等主流 Agent 间通用：

- 本文件的 `name`/`description`/`version` 是通用字段；`user-invocable`、`allowed-tools` 是 Claude Code 增强，其他 Agent 会忽略。
- **监控功能本身与 Agent 无关**：即使不经过任何 Agent，`cron` 直接运行 `scripts/monitor.py check` 即可工作。

在 Codex 等其他 Agent 中使用时，把本 skill 目录软链到它的 skills 发现路径：

```sh
mkdir -p ~/.codex/skills   # 或 .agents/skills
ln -s <skill-dir> ~/.codex/skills/wzz-server-monitor
```

## 11. 安全说明

- SMTP 密码存 `~/.config/resource-monitor/.smtp_secret`（`chmod 600`），不写入配置文件。
- 模板上下文只注入白名单变量，凭据与完整配置不进模板。
- 脚本只读取系统指标与发送邮件，不做任何删除/修改系统操作。
- 发布版本不包含任何用户数据；`config.yaml`、`state.json`、`.smtp_secret` 均生成于用户本地目录。
