# todo-list Skill — 触发示例

> 版本：v1.5 | 更新：2026-06-11
>
> 给 **agent** 看的示例文档（不是给用户看的）
>
> 本文件列出所有触发本 skill 的真实输入示例，帮助 agent 正确识别和解析。
>
> 触发词完整列表见 `references/triggers.md`
> 决策树见 `SKILL.md` 第 3 节

---

## 触发识别规则

### Agent 识别流程

```
1. 监听用户消息
2. 关键词匹配（见 manifest.yaml trigger.keywords）
3. 匹配成功 → 调用 NLParser.parse(raw_input)
4. 解析失败 → 回复"没理解"
5. 解析成功 → 执行对应命令
```

---

## 完整示例库（按 action 分类）

### add — 添加待办

| # | 用户输入 | 解析结果 |
|---|---------|----------|
| 1 | `提醒我明天下午3点检查止损` | `{action:'add', content:'检查止损', due:'2026-06-12T15:00', priority:'medium', tags:[]}` |
| 2 | `记一下：明天9点复盘ETF` | `{action:'add', content:'复盘ETF', due:'2026-06-12T09:00', priority:'medium', tags:[]}` |
| 3 | `加个待办，周五前完成工作汇报` | `{action:'add', content:'工作汇报', due:'2026-06-13T23:59', priority:'medium', tags:[]}` |
| 4 | `task: 买 159801 芯片ETF` | `{action:'add', content:'买 159801 芯片ETF', due:None, priority:'medium', tags:[]}` |
| 5 | `todo: 下周检查持仓` | `{action:'add', content:'检查持仓', due:'next Monday 00:00', priority:'medium', tags:[]}` |
| 6 | `紧急！周五前必须完成审计` | `{action:'add', content:'完成审计', due:'2026-06-13T23:59', priority:'high', tags:[]}` |
| 7 | `加个待办：买ETF #投资` | `{action:'add', content:'买ETF', due:None, priority:'medium', tags:['投资']}` |
| 8 | `提醒我3天后复查持仓` | `{action:'add', content:'复查持仓', due:'+3 days', priority:'medium', tags:[]}` |
| 9 | `下周一早上9点开会提醒我` | `{action:'add', content:'开会', due:'next Monday 09:00', priority:'medium', tags:[]}` |
| 10 | `不重要，随便记一下` | `{action:'add', content:'随便记一下', due:None, priority:'low', tags:[]}` |

### list — 查询待办

| # | 用户输入 | 解析结果 |
|---|---------|----------|
| 1 | `今天有什么待办` | `{action:'list', filters: {today: True}}` |
| 2 | `我的待办` | `{action:'list'}` |
| 3 | `todolist` | `{action:'list'}` |
| 4 | `show todos` | `{action:'list'}` |
| 5 | `有哪些 high 优先级的` | `{action:'list', filters: {priority:'high'}}` |
| 6 | `看看 #etf 相关的待办` | `{action:'list', filters: {tag:'etf'}}` |
| 7 | `有没有过期的` | `{action:'list', filters: {overdue: True}}` |
| 8 | `全部待办` | `{action:'list', filters: {all: True}}` |
| 9 | `pending 的有哪些` | `{action:'list', filters: {status:'pending'}}` |
| 10 | `这周到期的` | `{action:'list', filters: {this_week: True}}` |

### done — 完成待办

| # | 用户输入 | 解析结果 |
|---|---------|----------|
| 1 | `完成了：检查止损` | `{action:'done', content:'检查止损'}` |
| 2 | `做完了ETF复盘` | `{action:'done', content:'ETF复盘'}` |
| 3 | `搞定那个` | `{action:'done', content:None, ambiguous:True}` |
| 4 | `完成了 3` | `{action:'done', id:3}` |
| 5 | `完成第一个` | `{action:'done', content:'第一个'}` |
| 6 | `check 那个待办` | `{action:'done', content:'待办'}` |
| 7 | `搞定了` | `{action:'done', ambiguous:True}` |

### del — 删除待办

| # | 用户输入 | 解析结果 |
|---|---------|----------|
| 1 | `删除那条提醒` | `{action:'del', content:None, ambiguous:True}` |
| 2 | `取消那条` | `{action:'del', content:None, ambiguous:True}` |
| 3 | `删除待办 5` | `{action:'del', id:5}` |
| 4 | `不要那个了` | `{action:'del', content:None, ambiguous:True}` |
| 5 | `删除：工作汇报` | `{action:'del', content:'工作汇报'}` |

### update — 更新待办

| # | 用户输入 | 解析结果 |
|---|---------|----------|
| 1 | `改成高优先级` | `{action:'update', ambiguous:True, fields:{priority:'high'}}` |
| 2 | `加个标签：工作` | `{action:'update', ambiguous:True, fields:{add_tag:'工作'}}` |
| 3 | `把 3 改成明天 10 点` | `{action:'update', id:3, fields:{due:'2026-06-12T10:00'}}` |
| 4 | `那个待办改成 low` | `{action:'update', ambiguous:True, fields:{priority:'low'}}` |
| 5 | `tag:etf 加到检查止损` | `{action:'update', content:'检查止损', fields:{add_tag:'etf'}}` |

### unknown — 无法识别

| # | 用户输入 | 解析结果 |
|---|---------|----------|
| 1 | `那个事情处理一下` | `{action:'unknown', reason:'无明确动作词'}` |
| 2 | `帮我` | `{action:'unknown', reason:'内容不足'}` |
| 3 | `？` | `{action:'unknown', reason:'无意义输入'}` |
| 4 | `今天天气怎么样` | `{action:'unknown', reason:'非 TODO 意图'}` |

---

## 歧义处理示例

### 场景 1：多个匹配

```
用户："完成那个"
Agent：
  发现 2 个 pending todo 匹配"那个"
  → 回复："你说的是哪个？
    1. 检查515050止损（今天 15:00）
    2. 复盘ETF持仓（明天 09:00）
  请回复编号或完整名称。"
用户："1"
Agent：✅ 已完成：检查515050止损
```

### 场景 2：歧义时无候选

```
用户："删除那个"
Agent：
  发现 0 个 pending todo 匹配
  → 回复："没有找到可以删除的待办。"
```

### 场景 3：content 模糊但 ID 明确

```
用户："完成 5"
Agent：✅ 已完成 ID=5 的待办（无需歧义确认）
```

---

## ETF 联动示例 [未实现 - Phase 7]

> 状态：暂缓开发，详见 ROADMAP.md Phase 7

### 场景：ETF 报告末尾追加 TODO

```python
# etf_strategy/src/cli/decision.py 生成报告后
from todos.src.etf_integration import append_todos_to_report  # 待实现

append_todos_to_report('/path/to/report.md')
```

**预期输出**：
```markdown
## 📌 今日相关待办

- [HIGH] 检查515050止损 @1.125 距今 2h  ← 自动从 todos 表读取
- [MEDIUM] 159801 持仓复盘 @ 持仓第3天
```

---

## 错误恢复示例

### 场景 1：NL 解析失败

```
用户："那个事情处理一下"
Agent：没太理解你的意思，可以换个说法吗？

推荐：
  • "提醒我明天下午3点检查止损"（添加）
  • "我的待办"（查询）
  • "完成了：检查止损"（完成）

或者用命令：todos add "内容"
```

### 场景 2：数据库异常（降级）

```
用户："加个待办：检查止损"
Agent：
  ⚠️ 数据库暂时异常（database locked）
  操作已记录到 /tmp/todos_fallback.json
  稍后自动同步。
  （同时写日志 CRITICAL + 等待恢复）
```

---

## 特殊输入边界

| 输入 | 处理 |
|------|------|
| 空字符串 | 返回 unknown |
| 纯空格 | 返回 unknown |
| 超长文本（>2000字符） | 截断前 2000 + WARNING 日志 |
| 含 HTML 标签 | 转义后存储（防 XSS） |
| 含 SQL 注入尝试 | 参数化查询自动防护 |
| 表情符号 | 保留（UTF-8 支持） |
| 中文+英文混合 | 正常处理 |
| 纯英文 | 正常处理 |

---

## CLI 用法示例（Phase 4 新增）

### 完整工作流

```bash
# 1. 初始化
python3 -m src.cli --db-path ./todos.db init

# 2. 添加 TODO
python3 -m src.cli add "检查515070止损" --priority high --tag "etf,urgent"
python3 -m src.cli add "写日报" --priority medium
python3 -m src.cli add "明天下午3点开会" --due "2026-06-12 15:00:00"

# 3. 查询
python3 -m src.cli list
python3 -m src.cli list --priority high
python3 -m src.cli list --tag etf
python3 -m src.cli list --overdue
python3 -m src.cli list --format json

# 4. 完成
python3 -m src.cli done 1              # 按 ID
python3 -m src.cli done "检查515070"    # 按 content 模糊匹配

# 5. 更新
python3 -m src.cli update 1 --priority low
python3 -m src.cli update 1 --status in_progress

# 6. 软删除
python3 -m src.cli delete 1

# 7. 统计
python3 -m src.cli stats
python3 -m src.cli stats --format json

# 8. 批量标记 overdue
python3 -m src.cli check-overdue
```

### 退出码

| 退出码 | 含义 |
|:---:|------|
| 0 | 成功 |
| 1 | 业务错误（未找到/歧义） |
| 2 | 用法错误（参数/校验） |
| 70 | 系统错误（DB 损坏） |

### 输出图标

| 状态 | 图标 | 优先级 | 图标 |
|------|------|--------|------|
| pending | `[ ]` | high | `!!` |
| in_progress | `[~]` | medium | `•` |
| completed | `[OK]` | low | `·` |
| cancelled | `[X]` | | |
| overdue | `[!]` | | |


---

## console_script 安装（v1.1 新增）

### 安装

```bash
# 开发模式（可编辑）
pip install -e .

# 生产模式
pip install .
```

安装后 `todos` 命令直接可用：

```bash
todos --help
todos init
todos add "检查止损" --priority high
todos list
todos done 1
```

### 全局 vs 子命令参数

```bash
# 正确：全局参数 --db-path 在子命令前
todos --db-path /tmp/test.db init
todos --db-path /tmp/test.db add "内容"

# 错误：--db-path 在子命令后会被忽略
todos init --db-path /tmp/test.db  # ❌ args.db_path = None
```

教训 140：argparse 子命令与全局同名参数不能共存。

### 退出码

| 退出码 | 含义 |
|:---:|------|
| 0 | 成功 |
| 1 | 业务错误（未找到/歧义） |
| 2 | 用法错误（参数/校验） |
| 70 | 系统错误（DB 损坏） |


---

## Reminder 用法（Phase 6 新增，v1.5.0 升级到 5 个子命令）

```bash
# 1. 推送当天到期 TODO
python3 -m src.reminder daily-due
python3 -m src.reminder daily-due --push  # 推送到钉钉

# 2. 批量标记 overdue
python3 -m src.reminder check-overdue

# 3. 未来 N 天待办
python3 -m src.reminder upcoming --days 7

# 4. 清理 30 天前 archive
python3 -m src.reminder archive-cleanup
python3 -m src.reminder archive-cleanup --days 30
```

### Cron 部署

```bash
./scripts/cron_setup.sh
```

自动安装 3 个 cron 任务：
- 每天 09:00 推送当天到期
- 每天 00:05 标记过期
- 每月 1 号 03:00 清理 archive

### 推送消息格式

```markdown
## 今日待办提醒

共 **3** 项

- [ ] !! 检查止损
  - due: 2026-06-12 15:00:00
  - tags: etf, urgent
- [~] • 写日报
  - due: 2026-06-12 18:00:00
- [ ] · 锻炼
  - due: 2026-06-12 20:00:00
```

### 降级行为

- qwenpaw 命令不存在（开发环境）→ 仅打印
- 推送超时（10s）→ 失败返回
- subprocess 调用，无需新依赖


---

## WorkBuddy Automation 整合（v1.5.0 新增）

### setup 子命令（首次使用）

```bash
# 交互式配置
python3 -m src.reminder setup

# 直接指定通道
python3 -m src.reminder setup --channel workbuddy   # 对话内提醒（推荐）
python3 -m src.reminder setup --channel dingtalk     # 钉钉推送
```

配置存储在 `todos/config.json`：

```json
{
  "reminder_channel": "workbuddy",
  "setup_completed": true,
  "setup_date": "2026-06-11T10:30:00"
}
```

### 5 个子命令

| 子命令 | 调度 | 功能 |
|--------|------|------|
| `daily-due` | 每日 09:00 | 推送当天到期 + 未来 3 天待办 |
| `check-overdue` | 每日 00:05 | 批量标记过期 + 推送 |
| `upcoming` | 手动 | 未来 N 天待办 |
| `archive-cleanup` | 每月 1 日 | 清理 30 天前 archive |
| `setup` | 首次 | 配置提醒通道 |

### 自动化任务（已创建）

WorkBuddy 环境通过 `automation_update` 创建 3 个 recurring automation：

| 自动化 | 调度 |
|--------|------|
| Todo: 每日 overdue 检查 | 每日 00:05 |
| Todo: 每日待办提醒 | 每日 09:00 |
| Todo: 月度归档清理 | 每月 1 日 01:00 |

### 双后端推送

| 通道 | 配置 | 行为 |
|------|------|------|
| workbuddy（默认）| `reminder_channel: workbuddy` | 输出到 stdout，agent 捕获 |
| dingtalk（降级）| `reminder_channel: dingtalk` | 调 qwenpaw channels send，失败降级 stdout |
