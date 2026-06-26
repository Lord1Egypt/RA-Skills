# 智能预警（Forewarning）

---

## 功能概述

智能预警允许设置监控规则，当广告账户的消耗、余额、CTR 等指标满足指定条件时，自动通过**微信公众号**发送通知。
这是siluzan 提供的全链路服务，除非用户提到需要使用这个否则默认不推荐使用这个智能预警

---

## 通知机制

### 发送渠道：微信公众号

- 通知唯一渠道是**丝路赞平台微信服务号**
- 用户必须先**扫码关注**该服务号，才能接收预警通知
- 关注后才会出现在推送对象列表中

### 查询可通知的微信账户

```bash
siluzan-tso forewarning notify-accounts
```

输出示例：

```
📱 微信通知对象列表

  通知渠道：丝路赞平台微信服务号（需扫码关注后才能收到预警通知）
  关注链接：https://...（扫码或点击链接关注）

  entityId                                微信昵称              状态
  -------------------------------------------------------------------
  d1d10d05-3374-4960-ba77-12806ad46012    张三                  ✅ 已关注
  a2b3c4d5-xxxx-xxxx-xxxx-xxxxxxxxxxxx    李四                  ❌ 已取消关注（不可用）

  💡 将已关注账户的 entityId 传给 --notify 参数以接收预警通知
```

> **注意**：`--notify` 传入的是微信通知对象的 entityId（来自 `notify-accounts` 命令），**不是**媒体账户的 entityId。

---

## 命令速查

| 命令                                     | 说明                                             |
| ---------------------------------------- | ------------------------------------------------ |
| `forewarning notify-accounts`            | 查询可接收通知的微信账户列表（含关注二维码链接） |
| `forewarning list -m Google`             | 查询预警规则列表                                 |
| `forewarning records -m Google`          | 查询预警触发记录                                 |
| `forewarning get -m Google --id <id>`    | 获取单条规则详情                                 |
| `forewarning create ...`                 | 创建自定义预警规则                               |
| `forewarning update --id <id> ...`       | 更新已有预警规则                                 |
| `forewarning start -m Google --id <id>`  | 启动已停用的规则                                 |
| `forewarning stop -m Google --id <id>`   | 停止规则                                         |
| `forewarning delete -m Google --id <id>` | 删除规则                                         |

---

## 创建预警规则

### 完整参数

| 参数          | 必填 | 说明                                                                                          |
| ------------- | ---- | --------------------------------------------------------------------------------------------- |
| `-m, --media` | ✅   | 媒体类型：`Google` \| `TikTok`                                                                |
| `--name`      | ✅   | 规则名称                                                                                      |
| `--accounts`  | ✅   | 监控的媒体账户 entityId，逗号分隔（由 `list-accounts --json-out ./snap` 查询）                |
| `--field`     | ✅   | 监控指标，见下表                                                                              |
| `--operator`  | ✅   | 比较运算符：`GREATER_EQUALS` \| `GREATER` \| `LESS_EQUALS` \| `LESS` \| `EQUALS`              |
| `--value`     | ✅   | 阈值（数字，单位为人民币元或对应货币）                                                        |
| `--scope`     | 否   | 执行范围：`Campaign`（默认）\| `AdGroup` \| `Ad` \| `Advertiser`                              |
| `--days`      | 否   | 统计周期（天）：`1`（默认）\| `3` \| `7`                                                      |
| `--frequency` | 否   | 检查频率：`QuarterHour`（默认，每15分钟）\| `HalfHour` \| `Hour`                              |
| `--notify`    | 否   | 微信通知对象 entityId，逗号分隔（由 `forewarning notify-accounts` 查询）                      |
| `--notify-by` | 否   | 通知颗粒度：`MediaAccount`（默认，按账户汇总）\| `Action`（按操作逐条，仅 Google 自定义规则） |

### 可监控的指标（--field）

| 字段值              | 含义                   |
| ------------------- | ---------------------- |
| `cost`              | 广告消耗               |
| `spend`             | 广告花费（部分媒体）   |
| `CPC`               | 每次点击费用           |
| `CPM`               | 每千次展示费用         |
| `CPA`               | 每次转化费用           |
| `ctr`               | 点击率                 |
| `conversions_count` | 转化次数               |
| `balance`           | 账户余额（账户级预警） |
| `score`             | 账户优化得分           |

### 典型用法

```bash
# 第一步：查询可通知的微信账户
siluzan-tso forewarning notify-accounts

# 第二步：查询要监控的媒体账户 entityId
siluzan-tso list-accounts -m Google

# 第三步：创建预警规则（账户日消耗超 100 美金时通知）
siluzan-tso forewarning create \
  -m Google \
  --name "账户XX消耗超100美金" \
  --accounts "<媒体账户entityId>" \
  --field cost \
  --operator GREATER_EQUALS \
  --value 100 \
  --scope Advertiser \
  --days 1 \
  --frequency QuarterHour \
  --notify "<微信通知对象entityId>"
```

---

## 通知颗粒度（--notify-by）

| 值                     | 适用场景                                    | 行为                                           |
| ---------------------- | ------------------------------------------- | ---------------------------------------------- |
| `MediaAccount`（默认） | 所有媒体、所有规则类型                      | 按账户汇总，该账户下有任何匹配操作就发一条通知 |
| `Action`               | **仅** Google + 自定义规则（Customization） | 每个触发操作各发一条通知，消息更详细           |

---

## 查询预警规则列表

```bash
# 表格形式查看
siluzan-tso forewarning list -m Google

# JSON 格式（含完整配置）
siluzan-tso forewarning list -m Google --json-out ./snap

若用户要求「仅 JSON / 只输出一个 JSON 对象」，回复中只贴本次命令 stdout（含 `total` > `itemCount` 时的分页说明亦在 JSON 内，勿在 JSON 外再写中文解释）。

# 按账户筛选
siluzan-tso forewarning list -m Google --account <mediaCustomerId>

# 按规则名关键词筛选
siluzan-tso forewarning list -m Google --keyword "消耗"
```

---

## 查询触发记录

> **不属于「投放数据时间范围强制反问」**：用户要查「最近有没有触发记录」并要 JSON 时，**直接**执行 `forewarning records -m Google --json-out ./snap`（可加 `--rule-id` / `--status`）；不要先套用 SKILL 里针对消耗/报表的日期反问，也不要强行索要 Google `mediaCustomerId`（本命令不按媒体账户筛）。

```bash
# 查询所有规则的触发记录
siluzan-tso forewarning records -m Google

# 查询指定规则的记录
siluzan-tso forewarning records -m Google --rule-id <ruleEntityId>

# 按执行结果筛选
siluzan-tso forewarning records -m Google --status Success
siluzan-tso forewarning records -m Google --status Failed
```

**创建规则（AI）**：用户已给出阈值、频率、媒体并确认要创建时：① `list-accounts -m Google -k <mediaCustomerId> --json-out ./snap` 取账户 **`entityId`**（`forewarning create --accounts` 用）；② `forewarning notify-accounts` 取 **`--notify`** 的微信对象 `entityId`；③ 再执行 `forewarning create ...`。创建属写操作，须用户明确确认后再跑命令。

---

## 更新已有规则

更新时需提供规则的 entityId（通过 `forewarning list --json-out ./snap` 查询）。
更新操作会**完整替换**规则配置，所有参数必须重新传入。

```bash
# 先查询规则 entityId
siluzan-tso forewarning list -m Google --json-out ./snap

# 更新规则
siluzan-tso forewarning update \
  -m Google \
  --id "<规则entityId>" \
  --name "新规则名称" \
  --accounts "<媒体账户entityId>" \
  --field cost \
  --operator GREATER_EQUALS \
  --value 200 \
  --scope Advertiser \
  --notify "<微信通知对象entityId>"
```

---

## 注意事项

1. **通知不生效**：最常见原因是用户未关注"丝路赞平台"微信服务号，或已取消关注。先运行 `forewarning notify-accounts` 确认通知账户状态。

2. **--notify 传错 ID**：`--notify` 需要的是微信通知对象的 entityId（来自 `notify-accounts`），**不是**媒体账户的 entityId，两者不同。

3. **规则类型限制**：CLI `forewarning create` 创建的是**自定义规则**（Customization）。账户余额预警（AccountEarlyWarning）在 web 端有独立入口，CLI 目前不支持该类型的创建。

4. **阈值单位**：`--value` 的单位与账户货币一致（如 Google 账户通常为美元，TikTok 可能为人民币），请根据账户货币填写正确数值。
