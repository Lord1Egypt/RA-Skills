# Tushare 股票数据技能

本技能封装了 **Tushare Pro 数据接口**，基于用户提供的详细接口文档，明确了所支持的**全部23个接口**。与通用调用器不同，本技能有明确的接口边界，方便用户了解其完整能力。

## 特性
- ✅ **接口明确**: 支持 23 个具体接口，涵盖行情、基础信息、基本面、特色数据。
- 📋 **列表可查**: 通过 `api_name: list` 可获取完整的支持接口列表。
- 🎯 **分类清晰**: 接口按“行情数据”和“基础信息”分类。
- 🔧 **即装即用**: 包含完整依赖和配置。

## 快速开始

### 1. 列出所有支持的接口
调用本技能，并将 `api_name` 参数设为 `list`：
json
{
"api_name": "list"
}
返回结果将包含所有支持的接口名称、中文名、描述和分类。

### 2. 调用具体接口
例如，获取平安银行日线数据：
json
{
"api_name": "daily",
"ts_code": "000001.SZ",
"start_date": "20240101",
"end_date": "20240110"
}
### 3. 配置Token (必做)
**本技能不自带有效Token，您必须使用自己在[Tushare Pro官网](https://tushare.pro)注册获取的Token。**

有两种方式设置Tushare Token（按优先级）：
1.  **调用参数传入**: 在每次调用的JSON参数中传入 `"token": "你的token"`。
2.  **环境变量**: 设置系统环境变量 `TUSHARE_TOKEN` 为你的token。

如果以上均未提供，技能将初始化失败并返回错误。

## 完整接口支持表
| 分类 | 接口数量 | 接口名称 (api_name) |
|------|----------|-------------------|
| 行情数据 | 13 | `daily`, `rt_k`, `stk_mins`, `rt_min`, `weekly`, `monthly`, `stk_weekly_monthly`, `stk_week_month_adj`, `adj_factor`, `daily_basic`, `stk_limit`, `suspend_d`, `hsgt_top10` |
| 基础信息 | 10 | `stock_basic`, `trade_cal`, `stock_st`, `stock_hsgt`, `namechange`, `stock_company`, `stk_managers`, `stk_rewards`, `bse_mapping`, `new_share`, `bak_basic` |

## 核心参数说明
调用本技能时，可传递以下参数。其中 `api_name` 为必填项，其他参数是否必需取决于具体接口。

| 参数名 | 必填 | 类型 | 说明与示例 |
| :--- | :--- | :--- | :--- |
| `api_name` | 是 | String | 要调用的接口名称。例如：`"daily"`, `"stock_basic"`。特殊值`"list"`用于查询接口列表。 |
| `token` | 否 | String | 您的Tushare Token。若不在此传入，则必须设置`TUSHARE_TOKEN`环境变量。 |
| `ts_code` | 否 | String | 股票代码。格式：`代码.交易所`。单/多个：`"000001.SZ"` 或 `"000001.SZ,600000.SH"`。 |
| `trade_date` | 否 | String | 指定交易日。格式：`YYYYMMDD`。示例：`"20240115"`。 |
| `start_date` | 否 | String | 开始日期。日线：`YYYYMMDD`；分钟线：`YYYY-MM-DD HH:MM:SS`。需与`end_date`配对使用。 |
| `end_date` | 否 | String | 结束日期。格式同 `start_date`。 |
| `fields` | 否 | String | 指定返回字段，英文逗号分隔，无空格。示例：`"ts_code,trade_date,open,close,vol"`。 |
| `extra_params` | 否 | String | 其他接口特定参数，需为**合法的JSON字符串**。示例：`"{\"freq\": \"5min\"}"`。 |

## 典型调用示例

### 获取实时日K线（支持通配符）
json
{
"api_name": "rt_k",
"ts_code": "6*.SH"
}
### 获取5分钟K线数据
json
{
"api_name": "stk_mins",
"ts_code": "600000.SH",
"freq": "5min",
"start_date": "2024-01-15 09:00:00",
"end_date": "2024-01-15 15:00:00"
}
### 获取股票列表
json
{
"api_name": "stock_basic",
"list_status": "L",
"fields": "ts_code,symbol,name,area,industry,list_date"
}
### 使用额外参数
json
{
"api_name": "stock_hsgt",
"trade_date": "20240115",
"extra_params": "{"type": "HK_SZ"}"
}
## 安装依赖
bash
pip install tushare pandas
## 重要注意事项
1.  **积分与权限**: 不同接口需要不同的Tushare积分。基础行情接口通常需2000积分，实时数据等高级接口需要更高积分或单独申请权限。
2.  **数据延迟**: 免费账号获取的数据可能有**15分钟**的延迟。
3.  **股票代码**: 格式为 `代码.交易所`，如 `000001.SZ` (深交所), `600000.SH` (上交所)。
4.  **日期格式**: 请严格区分**日线接口** (`YYYYMMDD`) 和**分钟线接口** (`YYYY-MM-DD HH:MM:SS`) 的日期时间格式。
5.  **官方文档**: 完整参数和字段说明，请参考 [Tushare官方文档](https://tushare.pro/document/2)。
6.  **错误排查**: 如调用失败，请按序检查：① Token是否有效且已配置；② 参数名称和格式是否正确；③ 账号积分是否支持该接口。
