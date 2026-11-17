---
name: wb-usage
slug: wb-usage-dashboard
displayName: WorkBuddy 用量看板
version: 1.0.0
summary: 读取本机 WorkBuddy 数据库，统计 Token 用量与积分消耗，生成离线 HTML 看板
description: 统计本机 WorkBuddy 的 Token 用量与积分消耗，生成离线用量看板。当用户问"我用了多少 token""额度还剩多少""用量统计""哪个模型烧得多""这周花了多少积分"时使用。
description_zh: "查看本机 WorkBuddy Token 用量与积分消耗，生成离线看板"
description_en: "Inspect local WorkBuddy token usage and credit consumption"
license: MIT
tags:
  - usage
  - token
  - dashboard
  - cost
---

# WorkBuddy 用量看板

官方客户端（含国际版）目前没有暴露用量/额度面板，但本机数据库里存着真实的会话用量。
本技能直接读取本地数据，生成一份离线看板，不联网、不上传。

## 数据来源

`~/.workbuddy-ai/workbuddy.db`（Windows：`C:\Users\<用户名>\.workbuddy-ai\workbuddy.db`）

| 表 | 字段 | 含义 |
| --- | --- | --- |
| `sessions` | `id` `title` `model` `created_at` `context_window` | 会话元信息 |
| `session_usage` | `used` `size` `credit_json` | 该会话累计 Token 用量、上下文窗口、逐请求积分 |

- `used / size` = 上下文窗口占用率
- `credit_json` 是 `{请求ID: 积分}` 的映射，求和即该会话的积分消耗；免费模型（如 deepseek-v4.1-flash）该字段为空，表示**确实不扣积分**，属正常现象

## 使用方法

```bash
python <skill_dir>/scripts/usage_report.py                     # 摘要 + 生成看板
python <skill_dir>/scripts/usage_report.py -o <输出路径>.html   # 指定输出位置
python <skill_dir>/scripts/usage_report.py --json              # 机器可读输出
```

Windows 下用托管 Python：

```bash
"C:/Users/<用户名>/.workbuddy-ai/binaries/python/versions/3.13.12/python.exe" \
  "<skill_dir>/scripts/usage_report.py" -o "<工作区>/wb-usage-dashboard.html"
```

## 输出

1. **终端摘要**：累计 Token / 积分 / 会话数 / 今日 / 近 7 天，以及逐会话明细表
2. **HTML 看板**：指标卡 + 每日柱状图 + 按模型分布 + 会话明细（含上下文占用进度条）

生成后用 `present_files` 把 HTML 打开给用户看。

## 注意事项

- 脚本会先把 `workbuddy.db` 及 `-wal` / `-shm` 复制到临时目录再只读打开，不会锁库，可在客户端运行时安全执行
- 数字是本地记录，**不是官方账单**，可能与实际计费口径有差异
- 当前会话的用量会随对话继续增长，需要最新数字就重跑一次
- 若数据目录不在默认位置，用环境变量 `WB_DATA_DIR` 指定
- 若用户要跨账号/跨版本（国内版 `~/.workbuddy` 与国际版 `~/.workbuddy-ai`）对比或迁移，可建议社区工具 `Harvey-Will/workbuddy-tools`（第三方，需自行评估）
