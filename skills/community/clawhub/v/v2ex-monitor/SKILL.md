# V2EX Monitor Skill

## Skill 概述

这是一个适合通用 AI Agent / OpenClaw 风格接入的 skill，用于：

- 监控指定 V2EX 节点的新帖子
- 拉取当前账号的提醒通知
- 生成 Markdown 总结报告
- 提供 MCP 服务，供支持 MCP 的 Agent 进一步调用

该 skill 采用“说明文档 + 可执行脚本 + 配置说明”的通用结构，便于直接集成或二次封装。

## 目录结构

```text
skills/
├─ SKILL.md                    # Skill 说明文档
├─ run_skill.py                # 推荐给 Agent 调用的统一入口
├─ v2ex_monitor.py             # 核心监控逻辑
├─ v2ex_mcp.py                 # MCP 服务入口
├─ v2ex-monitor.md             # 原始功能说明
├─ v2ex_monitor_config.example.json
├─ requirements.txt            # 推荐依赖清单
├─ v2ex_hourly_report.md       # 运行后生成的报告
└─ v2ex_monitor_data/
   ├─ seen_topics.json         # 已处理主题记录
   └─ seen_notifications.json  # 已处理提醒记录
```

## 适用场景

当用户提出以下需求时可调用本 skill：

- “帮我监控 V2EX 某几个节点的新帖子”
- “每小时汇总 V2EX 的新主题和提醒”
- “生成 V2EX 热门帖子摘要”
- “通过 MCP 查询 V2EX 节点主题 / 主题详情 / 提醒通知”

## 输入

### 方式 1：统一入口脚本

```bash
python skills/run_skill.py config --nodes python,linux,programmer --apikey <你的_api_key>
python skills/run_skill.py run
python skills/run_skill.py report
```

### 方式 2：直接调用核心脚本

```bash
python skills/v2ex_monitor.py config --nodes python,linux,programmer --apikey <你的_api_key>
python skills/v2ex_monitor.py run
python skills/v2ex_monitor.py daemon --interval 1
```

### 方式 3：作为 MCP 服务

```bash
python skills/v2ex_mcp.py --stdio
```

## 输出

- `skills/v2ex_hourly_report.md`：监控报告
- `skills/v2ex_monitor_data/seen_topics.json`：已处理帖子记录
- `skills/v2ex_monitor_data/seen_notifications.json`：已处理提醒记录
- MCP 调用返回的 JSON 文本结果

## 配置说明

1. 复制示例配置：

```bash
copy skills\v2ex_monitor_config.example.json skills\v2ex_monitor_config.json
```

2. 填写你的 V2EX API Key 与监控节点。

也可以直接通过命令配置：

```bash
python skills/run_skill.py config --nodes python,linux,programmer --apikey <你的_api_key>
```

## Agent 使用建议

对于不支持 MCP 的 Agent，优先调用：

```bash
python skills/run_skill.py run
python skills/run_skill.py report
```

对于支持 MCP 的 Agent，可启动：

```bash
python skills/v2ex_mcp.py --stdio
```

然后使用以下工具：

- `v2ex_get_node_topics`
- `v2ex_get_topic`
- `v2ex_get_topic_replies`
- `v2ex_get_notifications`
- `v2ex_get_my_info`
- `v2ex_get_node_info`
- `v2ex_monitor_topics`
- `v2ex_config`

## 注意事项

- 默认不再内置真实 API Key，需由使用者自行配置。
- 生成的报告与数据文件都保存在 `skills/` 目录下，便于 skill 打包。
- 如果你是以 OpenClaw 的自定义 skill 目录方式接入，通常可将整个 `skills/` 目录作为 skill 资源目录使用。
- 当前核心监控逻辑优先使用 `urllib3`，即使未安装 `requests` 也可以显示帮助并执行大部分监控流程；若安装了 `requests`，会自动启用回退能力。

## 依赖建议

建议直接安装：

```bash
pip install -r skills/requirements.txt
```

或手动安装：

```bash
pip install urllib3 mcp pydantic requests
```

## 去重说明

- 帖子去重：基于主题 ID，已记录到 `seen_topics.json`
- 提醒去重：优先使用提醒 ID；如果接口未返回 ID，则回退到提醒内容哈希，记录到 `seen_notifications.json`
- 因此在单实例按小时执行时，同一帖子和同一提醒不会在后续运行中重复计入“新增”