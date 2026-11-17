# 加固扫描报告模板（report template）

> 元安全 yotta-agent-hardening 的 `scan` 输出三种形式：终端文本（默认）、JSON（`--json`）、
> Markdown 报告（`--report out.md`）。本文档给出结构与字段说明，便于对接 CI 与二次处理。

## 退出码（与安全家族一致）

| 退出码 | 含义 | 触发条件 |
|---|---|---|
| 0 | 通过 | 无 low 及以上发现（最高 info 或无发现） |
| 1 | 有加固建议 | 最高严重级为 low 或 medium |
| 2 | 高危需处理 | 最高严重级为 high 或 critical |
| 4 | 用法错误 / 致命异常 | 目标不存在、非法域、文件不可读、用法错误 |

`--severity` 只影响报告内容（过滤低严重级条目），**不影响退出码**；CI 请以退出码为准。

## JSON 结构（`--json`）

顶层字段：`tool` / `cn_name` / `version` / `target` / `time` / `domains` /
`files_scanned` / `exit_code` / `result` / `max_severity` / `summary` / `findings` / `threat`。

```json
{
  "tool": "yotta-agent-hardening",
  "cn_name": "元安全",
  "version": "0.2.6",
  "target": "./agent-runtime",
  "time": "2026-08-29T08:10:33+08:00",
  "domains": ["pi", "tools", "isolation"],
  "files_scanned": 3,
  "exit_code": 2,
  "result": "high",
  "max_severity": "high",
  "summary": { "info": 0, "low": 2, "medium": 4, "high": 1, "critical": 0 },
  "findings": [
    {
      "rule_id": "HTO-005",
      "detector": "McpRemoteSource",
      "severity": "high",
      "domain": "tools",
      "file": "config/mcp.json",
      "line": 0,
      "description": "MCP 服务器来源为远程 http(s) 地址（不可信源，无哈希/签名锁定，需先过元信/元审）",
      "confidence": 75
    }
  ],
  "threat": {
    "health_score": 35,
    "taxonomy": [
      { "name": "供应链风险", "verdict": "danger", "count": 1 },
      { "name": "其他安全风险", "verdict": "suspicious", "count": 2 }
    ],
    "behaviors": [
      { "behavior": "调用远端 API", "observed": 1 },
      { "behavior": "修改 AI 配置", "observed": 1 }
    ]
  }
}
```

字段说明：

- `result`：`pass`（0）/ `suggest`（1）/ `high`（2）。
- `max_severity`：本次扫描最高严重级；`summary` 为各严重级计数。
- `findings[].file`：相对扫描目标的路径；`line` 为命中行号（MCP 配置分析类为 0，表示配置级）。
- `description`：固定「类」表述，**不含可复制注入串 / 命中原文**。
- `threat`：双视角视图 —— `health_score`（0-100 安全健康度评分）+ `taxonomy`（8 检测点逐类 verdict）+ `behaviors`（13 行为项）。

## Markdown 报告结构（`--report out.md`）

```
# 加固扫描报告（元安全 yotta-agent-hardening）

- 目标 / 时间 / 扫描文件数 / 扫描域 / 结果（critical=… exit N）

## 汇总            ← 严重级计数表 + 安全健康度评分（0-100）
## 威胁捕获模型视图（8 类）  ← 8 检测点逐类 verdict 表
## 行为项（13 项）          ← 观察到 / 未观察到的行为项
## 域 1 / 2 / 3    ← 每个有发现的域一张表：规则 | 严重级 | 文件 | 行 | 说明
## 说明            ← 行为锚点声明（只读 / 敏感读取默认开启 / 类表述 / 守则入口）
```

域表列：`规则`（规则号）、`严重级`、`文件`、`行`、`说明`（「类」表述，不回显命中原文）。
无发现的域不出现；全绿时只保留汇总与说明。

## 扫描留痕（audit log）

- 位置：`~/.yotta-hardening/audit.log`（可用 `--config-dir` 或 `$YOTTA_HARDENING_DIR` 覆盖）。
- 格式：JSONL，每次 `scan` 追加一条，字段：
  `ts` / `tool` / `version` / `action=scan` / `target` / `domains` / `result` /
  `exit_code` / `max_severity` / `files_scanned` / `summary`。
- 行为锚点④：**每次扫描默认留痕，无 `--no-audit`**。
- 查看 / 过滤 / 导出：

```bash
python3 scripts/yotta_agent_hardening.py audit log
python3 scripts/yotta_agent_hardening.py audit log --result high
python3 scripts/yotta_agent_hardening.py audit log --severity high
python3 scripts/yotta_agent_hardening.py audit log --since 2026-08-01 --until 2026-08-29
python3 scripts/yotta_agent_hardening.py audit log --limit 20
python3 scripts/yotta_agent_hardening.py audit log --json
python3 scripts/yotta_agent_hardening.py audit log --export audit-high.jsonl
```

## 脱敏纪律

- 报告与留痕一律「类」表述，**不回显命中原文**（不输出可复制注入串 / 凭据值 / 命中行内容）。
- 发现硬编码凭据只报告文件位置与风险等级；发现敏感读取只报告路径类别与风险等级。
- 需要对外提交报告时，先过一遍 `audit log --export` 产物，确认无敏感片段。
