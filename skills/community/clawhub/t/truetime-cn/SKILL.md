---
name: truetime-cn
description: 中文优先的精确时间处理：当前时间、相对/绝对偏移、跨时区、夏令时、农历干支、中国法定节假日（含调休补班）、24 节气。长会话规划必备——任何涉及"现在""明天""X 天后""截止日""会议时间""农历某节"的请求都应该用这个 skill，因为系统注入的日期没有时分秒、不会随对话推进而更新、不知道中国节假日和调休、不会做日历月运算、容易在 DST 上算错。LLM的内置时间常识在跨时区与日历月计算上不可靠；遇到任何时间敏感的决策（订机票、安排会议、设定截止、长任务进度核对）都先调本 skill 拿事实，再做判断。
license: MIT-0
---

# truetime-cn

中文优先、跨平台的时间精确处理。支持 Claude.ai 沙箱、Claude Code、OpenClaw 及任意 Python ≥ 3.9 环境，零外部依赖。

## 何时触发本 skill

只要请求里出现以下任意信号，**先调脚本，后回答**：

- "现在""今天""明天""昨天""刚才""一会儿""稍后"等时间词
- 相对时间："X 分钟/小时/天/周/月/年后"、"X 个月零 X 天后"、"半年后"
- 绝对时间："2026 年 9 月 25 日 9 点"、"中秋节那天"
- 跨时区："北京 X 点在纽约几点"、"我们和欧洲同事开会"
- 中国节假日："春节""国庆""调休""补班""下周一是不是工作日"
- 农历："农历几号""中秋是几号""春节倒计时"、"今年闰几月"
- 节气："立春""夏至"
- 长任务规划检查点："这个 deadline 还有多久""按目前进度能赶上吗"

**不必触发**：纯历史问题（"1949 年发生了什么"）、已知绝对日期且无需运算（"圣诞节是 12 月 25 日"）。

## 不可妥协的规矩

1. **用户给的数值原样保留**——"1.5 个月"就是 1.5，不要替换成"约 45 天"再做计算。
2. **必须用脚本读真实时间**——绝不基于系统注入日期"估算"。系统日期没有时分秒，且对话进行中会越来越陈旧。
3. **UTC 优先**——脚本输出的 `target_utc` 是规范值；本地时区只用于显示。
4. **DST 不猜**——脚本会硬错，把错误信息原样转给用户并要求显式 offset。
5. **农历仅作显示**——执行调度仍用公历 UTC。用户只给农历日期时，反问要求公历对应。
6. **节假日数据缺失要明示**——脚本返回 `holiday_data_year_available: false` 时，告诉用户"我没有该年节假日数据，仅按周末规则判断"。
7. **不要在没跑脚本前就回答时间**——这是最常见的错误。

## 如何调用脚本

**Claude.ai（用户上传 skill 后）**：
```bash
python3 /mnt/skills/user/truetime-cn/scripts/truetime_cn.py [选项]
```

**Claude Code / OpenClaw / 本地**：在 SKILL.md 所在目录运行
```bash
python3 ./scripts/truetime_cn.py [选项]
```

**零依赖**：脚本仅需 Python ≥ 3.9 标准库。农历库 `cnlunar`（MIT，OPN48 作）已 vendor 到 `vendor/cnlunar/`，运行时自动加载，无需 `pip install` 任何东西。

## 核心命令

| 用途 | 命令 |
|---|---|
| 当前时间（默认北京） | `python3 ...truetime_cn.py` |
| 当前 + 中文摘要 | `python3 ...truetime_cn.py --human` |
| 1.5 个月后 | `python3 ...truetime_cn.py --plus 1.5month` |
| 1 小时 30 分后 | `python3 ...truetime_cn.py --plus 1h30m` |
| 250.5 毫秒后 | `python3 ...truetime_cn.py --plus 250.5ms` |
| 北京 X 点在纽约 | `python3 ...truetime_cn.py --target 2026-09-25T09:00:00 --target-tz Asia/Shanghai --user-tz America/New_York` |
| 用户在洛杉矶时区 | 加 `--user-tz America/Los_Angeles` |
| 列所有时区 | `python3 ...truetime_cn.py --list-timezones` |

## 单位约定

- **固定单位**：`ms`、`s`、`m`、`h`、`d`、`w`（含全拼 milliseconds、seconds…）
- **日历单位**：`mo`（month）、`y`（year）、`decade`、`century`
- 全部支持小数：`1.5month`、`0.1year`、`0.01century`
- 复合 token：`1h30m`、`1month2weeks`
- 月末钳位：1/31 + 1mo = 2/28 或 2/29
- 不识别的单位会硬错，不猜

## 输出契约

脚本输出 JSON，必含以下字段：

| 字段 | 含义 |
|---|---|
| `now_utc` / `target_utc` | 规范 UTC 时间（ISO 8601） |
| `now_user_tz` / `target_user_tz` | 用户时区下的时间 |
| `target_server_tz` | 服务器时区下的时间 |
| `now_lunar` / `target_lunar` | 农历对象，含 `display`（"丙午年三月廿二"）、`year_ganzhi`、`month`、`day`、`zodiac`、`is_leap_month`、`next_solar_term`、`next_solar_term_date` |
| `now_zh_holiday` / `target_zh_holiday` | 中国法定节假日名（如"春节"），无则 `null` |
| `now_is_workday` / `target_is_workday` | 是否工作日（已考虑调休补班） |
| `target_holiday_source` | 判定来源：`statutory_holiday` / `compensatory_workday` / `weekend_rule` / `fallback_weekend_only`（无该年数据时） |
| `delta_milliseconds` / `delta_seconds` | 与 now 的差 |
| `delta_human_zh` | 中文摘要："约 4 个月零 22 天" |
| `holiday_data_year_available` | 是否有目标年的节假日数据 |
| `assumptions` | 脚本做的隐含假设（如"无时区按 UTC 解释"） |

## 长会话时间漂移检测

Claude 在长会话里特别容易踩坑：第一次问时调了脚本拿到准确时间，后续基于这个值聊很久之后还按这个旧值算。**遇到下面任意一种情况，必须重新调脚本：**

- 距上次调脚本超过 **15 分钟**（按对话内 timestamp 估算，或宁可错杀）
- 用户消息里出现"现在""此刻""当前"等词，**且**当前是时间敏感任务（订票、约会、deadline）
- 任何"还有多久""倒计时""到点没"类问题
- 用户表达不确定："是吗？""真的？""我感觉时间不对"
- 跨午夜：上次调用后用户讨论了 30+ 分钟，可能跨日

不要节省调用次数。脚本本地运行，无成本。

## DST 错误处理

脚本对模糊或不存在的本地时间硬错。原文转给用户：

> 用户："2026年11月1日凌晨1点半的航班，洛杉矶起飞"
> 脚本错误："DST 模糊时间: 2026-11-01T01:30:00 在 America/Los_Angeles 存在两次..."
> 你应回复："洛杉矶 11月1日凌晨1:30在夏令时回拨当晚出现两次。请确认航班是回拨前 (PDT, -07:00) 还是回拨后 (PST, -08:00)。"

## 纯对话兜底（无任何工具时）

若环境中**没有 bash/code execution**（罕见情况，如纯网页对话且未开代码工具），按以下降级：

1. 明确告诉用户："我此刻没有工具能取真实时间，只能基于系统注入的日期 `<注入值>`。"
2. 时分秒未知，故**不要**编造："现在大概是下午"。
3. 若任务对精度敏感（订票、deadline），**反问用户当前精确时间**，再做计算。
4. 不做跨时区运算（Claude 心算时区不可靠）；让用户提供本地时间。
5. 提示用户："启用 Code Execution 后，本 skill 可提供精确时间、农历、中国节假日。"

## 节假日数据维护

`data/cn_holidays.json` 来自国务院办公厅每年 11 月发布的次年通知。当前内置 2026 年。**脚本检测到 `holiday_data_year_available: false` 时，主动告知用户**：

> "2027 年节假日表尚未内置（国务院办公厅一般在 2026 年 10-11 月发布），目前仅按周末规则判断。"

## 完整工作流

1. **意图提取**：从用户文本里抓时间词、单位、时区线索、目标日。
2. **调脚本**：用上面命令拿 JSON。
3. **优先用 UTC 推理**：所有比较、排序、调度逻辑都基于 `target_utc`。
4. **回复用本地表达**：给用户看 `target_user_tz` 和 `target_lunar.display`。
5. **节假日要点提示**：若 `target_zh_holiday` 非空或 `target_is_workday: false`，明确指出。
6. **DST 失败要透传**：把错误原文给用户，要求显式 offset。
7. **跨长对话主动重测**：详见上面的"漂移检测"。

## 触发短语示例（提高自动激活率）

verify time accuracy、calculate utc target、set precise reminder、convert to utc、handle timezones、中文时间、农历日期、中国节假日、调休、春节倒计时、跨时区会议、deadline 还有多久、现在几点
