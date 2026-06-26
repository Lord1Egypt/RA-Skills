# 友盟+ App 分析 — 命令参考

## 全部应用

```bash
python3 umeng.py get-all-app-data
python3 umeng.py get-app-count
python3 umeng.py get-app-list [--page 1] [--per-page 20] [--access-token TOKEN]
```

## 单个应用

所有命令均需 `--appkey <appkey>`（数字，非字符串）。

### 今日/昨日快速数据

```bash
python3 umeng.py get-today-data --appkey 123456
python3 umeng.py get-yesterday-data --appkey 123456
python3 umeng.py get-today-yesterday-data --appkey 123456
```

### 时间范围统计（--start-date / --end-date 格式 YYYY-MM-DD）

```bash
# 基础指标（可选 --period-type daily/weekly/monthly）
python3 umeng.py get-new-users --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31
python3 umeng.py get-active-users --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31
python3 umeng.py get-launches --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31

# 留存率（可选 --period-type --channel --version --type）
python3 umeng.py get-retentions --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31

# 游戏账号（仅游戏类 App）
python3 umeng.py get-new-accounts --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31
python3 umeng.py get-active-accounts --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31
```

### 指定日期统计（--date 格式 YYYY-MM-DD）

```bash
# App 每日统计（可选 --version --channel）
python3 umeng.py get-daily-data --appkey 123456 --date 2024-01-31

# 渠道/版本维度（可选 --page --per-page）
python3 umeng.py get-channel-data --appkey 123456 --date 2024-01-31
python3 umeng.py get-version-data --appkey 123456 --date 2024-01-31

# 使用时长（可选 --stat-type --channel --version）
python3 umeng.py get-durations --appkey 123456 --date 2024-01-31
```

### 按渠道或版本过滤（--period-type 必填）

```bash
python3 umeng.py get-launches-by-channel-or-version \
  --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31 \
  --period-type daily --channels "渠道A,渠道B"

python3 umeng.py get-active-users-by-channel-or-version \
  --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31 \
  --period-type daily --versions "1.0,2.0"

python3 umeng.py get-new-users-by-channel-or-version \
  --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31 \
  --period-type daily
```

### 自定义事件

```bash
# 创建事件（--event-type 可选）
python3 umeng.py create-event --appkey 123456 \
  --event-name "btn_click" --event-display-name "按钮点击"

# 事件列表（可选 --page --per-page --version）
python3 umeng.py get-event-list --appkey 123456 \
  --start-date 2024-01-01 --end-date 2024-01-31

# 事件统计数据
python3 umeng.py get-event-data --appkey 123456 \
  --start-date 2024-01-01 --end-date 2024-01-31 --event-name "btn_click"

# 事件独立用户数
python3 umeng.py get-event-unique-users --appkey 123456 \
  --start-date 2024-01-01 --end-date 2024-01-31 --event-name "btn_click"

# 事件参数列表（需要 --event-id，是数字 ID，不是 event-name）
python3 umeng.py get-event-param-list --appkey 123456 \
  --start-date 2024-01-01 --end-date 2024-01-31 --event-id 789

# 事件参数值列表
python3 umeng.py get-event-param-value-list --appkey 123456 \
  --start-date 2024-01-01 --end-date 2024-01-31 \
  --event-name "btn_click" --event-param-name "page"

# 事件参数值统计数据
python3 umeng.py get-event-param-data --appkey 123456 \
  --start-date 2024-01-01 --end-date 2024-01-31 \
  --event-name "btn_click" --event-param-name "page" --param-value-name "home"

# 事件参数值时长列表
python3 umeng.py get-event-param-value-duration-list --appkey 123456 \
  --start-date 2024-01-01 --end-date 2024-01-31 \
  --event-name "btn_click" --event-param-name "page"
```

## 参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `--appkey` | App 的 appkey（**整数**） | `123456` |
| `--start-date` | 开始日期 | `2024-01-01` |
| `--end-date` | 结束日期 | `2024-01-31` |
| `--date` | 指定日期 | `2024-01-31` |
| `--period-type` | 统计周期 | `daily` / `weekly` / `monthly` |
| `--channel` | 单渠道过滤 | `华为应用市场` |
| `--channels` | 多渠道（逗号分隔） | `渠道A,渠道B` |
| `--version` | 单版本过滤 | `1.0.0` |
| `--versions` | 多版本（逗号分隔） | `1.0,2.0` |
| `--event-name` | 事件标识名 | `btn_click` |
| `--event-id` | 事件 ID（**整数**，与 event-name 不同） | `789` |
| `--event-param-name` | 事件参数名 | `page` |
| `--param-value-name` | 参数值名称 | `home` |
| `--page` | 页码 | `1` |
| `--per-page` | 每页条数 | `20` |
