# truetime-cn

跨平台的中文时间精确处理 skill，支持 Claude.ai 沙箱、Claude Code、OpenClaw 及任意 Python ≥ 3.9 本地环境，零外部依赖。

## 它解决什么问题

LLM 处理中文时间场景时容易出三类错误：
1. **静态注入日期陈旧化**：长会话进行 30 分钟后，LLM 还按对话开始时的日期算，结果跨日错误。
2. **跨时区与日历月心算不可靠**：1.5 个月、月末钳位、DST 转换 LLM 自己算经常错。
3. **不知道中国节假日和调休补班**：把春节 2 月 14 日补班那天当成普通周六。

本 skill 提供一个 Python 引擎 + 强制工作流，让 LLM 在每次时间敏感决策前调脚本拿真实数据，避免上述错误。

## 与 cccat6/truetime 的关系

- 参考来自 cccat6/truetime（OpenClaw 生态），独立实现，**未复制其 .mjs 代码**。
- 引擎从 Node 改 Python（Claude.ai 沙箱 Python 优先）。
- 增加：中国法定节假日 + 调休补班识别、农历干支显示、24 节气、长会话漂移检测、纯对话降级方案。
- 默认时区改 `Asia/Shanghai`。

## 安装

### Claude.ai

1. 打包：`zip -r truetime-cn.zip truetime-cn/`（或下载 .skill 包）
2. Claude.ai → Settings → Skills → Upload skill
3. 在对话里启用本 skill

### Claude Code

```bash
cp -r truetime-cn ~/.claude/skills/
```

### OpenClaw / ClawHub

```bash
clawhub install <your-slug>/truetime-cn
```
（发布后可用）

### 依赖

**零外部依赖。** 农历库 [cnlunar](https://github.com/OPN48/cnLunar) 0.2.4（MIT，作者 cuba3@OPN48）已 vendor 到 `vendor/cnlunar/`。这样做的目的：

1. 消除供应链风险（无需 `pip install`，无版本漂移）
2. 装完即用，不污染用户系统 Python
3. 离线/沙箱/受限环境同样工作

升级 cnlunar 时手工同步 `vendor/cnlunar/`，并更新 `vendor/README.md` 的 bundled 日期。

## 命令速查

```bash
# 当前时间，带中文摘要
python3 scripts/truetime_cn.py --human

# 1.5 个月后的时间和农历
python3 scripts/truetime_cn.py --plus 1.5month

# 北京 9:00 的会议在纽约几点
python3 scripts/truetime_cn.py \
  --target 2026-09-25T09:00:00 \
  --target-tz Asia/Shanghai \
  --user-tz America/New_York

# 列出所有 IANA 时区
python3 scripts/truetime_cn.py --list-timezones | head
```

## 输出示例

```json
{
  "now_user_tz": "2026-05-08T18:18:13+08:00",
  "now_lunar": {
    "display": "丙午年三月廿二",
    "zodiac": "马",
    "next_solar_term": "小满",
    "next_solar_term_date": "2026-05-21"
  },
  "now_is_workday": true,
  "target_user_tz": "2026-02-17T10:00:00+08:00",
  "target_zh_holiday": "春节",
  "target_is_workday": false,
  "target_holiday_source": "statutory_holiday",
  "delta_human_zh": "约 -2 个月零 19 天"
}
```

## 节假日数据维护

`data/cn_holidays.json` 内置 2026 年法定节假日和调休补班日，来源国务院办公厅 [国办发明电〔2025〕7号](http://politics.people.com.cn/n1/2025/1104/c1001-40596715.html)。

每年 10-11 月国务院办公厅发布次年安排后，需手动追加。脚本会在数据缺失时返回 `holiday_data_year_available: false`，提示降级。

欢迎 PR 添加新年度数据。

## 测试

```bash
cd truetime-cn
python3 -m pytest tests/ -v
```

## License

MIT-0 (本项目代码)。本项目包含的 vendored 第三方库各自保留原许可：

- `vendor/cnlunar/` —— [cnlunar](https://github.com/OPN48/cnLunar) v0.2.4，MIT，Copyright (c) 2025 OPN48 (cuba3)

详见 `vendor/cnlunar/LICENSE` 和 `vendor/README.md`。

## Acknowledgements

- 设计契约（输出字段、日历单位、DST 严格策略）灵感来自 [cccat6/truetime](https://github.com/openclaw/skills/tree/main/skills/cccat6/truetime)，独立用 Python 实现，未复制其 .mjs 代码。
- 农历计算依赖 [OPN48/cnLunar](https://github.com/OPN48/cnLunar)，已 vendor 进本项目。
- 节假日数据源自国务院办公厅 [国办发明电〔2025〕7号](http://politics.people.com.cn/n1/2025/1104/c1001-40596715.html)。
