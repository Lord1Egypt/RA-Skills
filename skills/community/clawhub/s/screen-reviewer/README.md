# Screen Reviewer — 电脑行为复盘助手

自动截图 → 结构化日志 → AI 每日复盘报告，帮你回顾一天的时间都花在了哪里。

## 它能做什么

- **每 5 秒自动截屏**，智能跳过没变化的画面（省空间）
- **记录活跃窗口** + **OCR 提取屏幕文字**，生成结构化日志
- **每天早上自动生成复盘报告**，包含时间分配、ROI 分析、行动建议
- **自动清理** 3 天前的截图，日志和报告永久保留
- **隐私保护**：支持暂停 + 应用黑名单（银行、密码管理器等自动跳过）

## 跨 Agent 兼容

一次安装，多个 AI Agent 自动发现：

| Agent | 发现方式 |
|-------|---------|
| Cursor | `~/.cursor/skills/screen-reviewer/` |
| Claude Code / Codex | `~/.codex/skills/screen-reviewer/` |
| 任意 Agent | 项目内 `CLAUDE.md` / `AGENTS.md` |

## 快速开始

### 1. 安装

```bash
git clone https://github.com/DRPris/screen-reviewer.git
cd screen-reviewer
bash install.sh
```

安装脚本会自动完成：
- 创建 Python 虚拟环境和依赖
- 编译 macOS OCR 工具（需要 Xcode Command Line Tools）
- 生成默认配置文件
- 注册到 Cursor 和 Codex 的 Skill 目录

### 2. 授权 macOS 权限

首次运行前需要授予两个权限：

- **屏幕录制**：系统设置 → 隐私与安全性 → 屏幕录制 → 勾选 Terminal
- **辅助功能**：系统设置 → 隐私与安全性 → 辅助功能 → 勾选 Terminal

### 3. 启动

```bash
# 手动启动
~/.screen-reviewer/venv/bin/python scripts/service_manager.py start

# 或设为开机自启（推荐）
~/.screen-reviewer/venv/bin/python scripts/service_manager.py install
```

### 4. 配置 AI（用于生成报告）

在 `~/.zshrc` 中添加 API Key：

```bash
# OpenAI（默认）
export OPENAI_API_KEY="sk-your-key"

# 或 Claude
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

如果用 Claude 或 Ollama，编辑 `~/.screen-reviewer/config.yaml` 修改 `report.ai_provider`。

## 命令参考

```bash
VENV=~/.screen-reviewer/venv/bin/python
SM=scripts/service_manager.py

$VENV $SM start              # 启动截图守护进程
$VENV $SM stop               # 停止
$VENV $SM status             # 查看状态 + 今日统计
$VENV $SM pause              # 暂停截图（进程保留）
$VENV $SM resume             # 恢复截图
$VENV $SM report             # 生成昨天的复盘报告
$VENV $SM report 2026-03-22  # 生成指定日期报告
$VENV $SM cleanup            # 清理过期截图
$VENV $SM install            # 安装 macOS 开机自启
$VENV $SM uninstall          # 卸载开机自启
```

## 配置说明

配置文件位置：`~/.screen-reviewer/config.yaml`

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `capture.interval_seconds` | 5 | 截图间隔（秒） |
| `capture.smart_detect` | true | 屏幕无变化时跳过 |
| `capture.jpeg_quality` | 60 | JPEG 质量（越低越省空间） |
| `privacy.blacklist_apps` | [1Password, ...] | 不截图的应用 |
| `ocr.enabled` | true | 是否启用文字提取 |
| `report.ai_provider` | openai | AI 提供商：openai / claude / ollama |
| `report.ai_model` | gpt-4o-mini | 模型名称 |
| `cleanup.keep_days` | 3 | 截图保留天数 |
| `categories.*` | 见配置文件 | 应用→价值分类（影响 ROI 分析） |

## 复盘报告示例

```markdown
# 每日复盘报告 — 2026-03-22

## 一、今日概览
- 总活跃时间：8h 32min
- 有效截图：1,680 张

## 二、时间分配
| 类别 | 应用 | 时长 | 占比 | ROI |
|------|------|------|------|-----|
| 编程开发 | Cursor | 4h 10min | 49% | ★★★★★ |
| 文档阅读 | Chrome | 1h 20min | 16% | ★★★★ |
| 社交媒体 | 微信 | 45min | 9% | ★★ |

## 四、ROI 分析
- 高价值时间占比：65%
- 时间黑洞：社交媒体 45min

## 六、明日行动建议
1. 上午集中处理编码任务
2. 社交媒体控制在 20min 以内
```

## 数据存储

```
~/.screen-reviewer/
├── config.yaml              # 配置
├── screenshots/             # 截图（按日期分文件夹，自动清理）
│   └── 2026-03-22/
├── logs/                    # 结构化日志（永久保留）
│   └── 2026-03-22.jsonl
└── reports/                 # 复盘报告（永久保留）
    └── 2026-03-22-review.md
```

## 系统要求

- macOS 12+（Monterey 及以上）
- Python 3.9+
- Xcode Command Line Tools（用于编译 OCR 工具）

## 卸载

```bash
bash uninstall.sh
# 如需彻底删除数据：rm -rf ~/.screen-reviewer
```

## License

MIT
