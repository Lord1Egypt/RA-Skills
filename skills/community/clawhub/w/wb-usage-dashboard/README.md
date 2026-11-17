# WorkBuddy 用量看板

WorkBuddy 官方客户端（含国际版）没有暴露 Token 用量和额度面板，但本机数据库里存着真实的会话消耗。
这个 Skill 直接读取本地数据，生成一份离线 HTML 看板——不联网、不上传、不写库。

## 能看什么

- **累计 Token / 积分消耗**，以及今日、近 7 天用量
- **每日消耗柱状图**，一眼看出哪天烧得最凶
- **按模型分布**，对比不同模型的实际开销
- **会话明细**：每个会话的 Token、上下文窗口占用率、积分、请求数

## 安装

把 `SKILL.md` 和 `scripts/` 放到 WorkBuddy 的技能目录：

```
~/.workbuddy-ai/skills/wb-usage/     # 国际版
~/.workbuddy/skills/wb-usage/        # 国内版
```

或者直接在客户端里用「导入技能」选择 `SKILL.md`。

## 使用

对 AI 说「查一下我的用量」即可触发。也可以手动运行：

```bash
python scripts/usage_report.py                      # 摘要 + 生成看板到当前目录
python scripts/usage_report.py -o report.html       # 指定输出路径
python scripts/usage_report.py --json               # 机器可读输出
```

Windows 下如果 `python` 不在 PATH，用 WorkBuddy 自带的托管 Python：

```bash
"C:/Users/<用户名>/.workbuddy-ai/binaries/python/versions/3.13.12/python.exe" scripts/usage_report.py
```

## 数据来源

读取 `~/.workbuddy-ai/workbuddy.db`（国内版为 `~/.workbuddy/workbuddy.db`）：

| 表 | 字段 | 含义 |
| --- | --- | --- |
| `sessions` | `id` `title` `model` `created_at` `context_window` | 会话元信息 |
| `session_usage` | `used` `size` `credit_json` | 会话累计 Token、上下文窗口、逐请求积分 |

- `used / size` = 上下文窗口占用率
- `credit_json` 是 `{请求ID: 积分}` 映射，求和即该会话积分消耗
- 免费模型（如 `deepseek-v4.1-flash`）该字段为空，表示**确实不扣积分**，属正常现象

数据目录不在默认位置时，用环境变量 `WB_DATA_DIR` 指定。

## 设计取舍

- **零依赖**：只用 Python 标准库，不需要 pip 装任何东西
- **只读**：把 `workbuddy.db` 及 `-wal` / `-shm` 复制到临时目录再打开，不锁库、不改数据，客户端运行时也能安全执行
- **离线**：看板是单文件 HTML，无外部 CDN，断网可看

## 已知限制

- 数字来自本地记录，**不是官方账单**，可能与实际计费口径有差异
- 看不到「剩余额度」——本地只有消耗记录，没有总额
- 当前会话的用量会随对话继续增长，需要最新数字就重跑一次

## License

MIT
