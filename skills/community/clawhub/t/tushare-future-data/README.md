# Tushare 期货数据技能

本技能封装了 **Tushare Pro 期货数据接口**，提供国内期货市场的全面数据查询功能。技能明确支持 **14 个核心接口**，涵盖行情、基础信息、仓单、结算、持仓、指数等。

## 特性
- 📈 **全面覆盖**：14个明确接口，覆盖期货数据全链条。
- 📋 **清晰透明**：通过 `api_name=list` 可查看所有支持接口，功能无黑盒。
- 🔧 **开箱即用**：完整配置，依赖清晰。
- 🛡 **安全可靠**：Token由用户自行配置，技能不内置任何有效凭证。

## 快速开始

### 1. 安装依赖
bash
pip install tushare pandas
### 2. 配置Token (必做！)
**本技能不自带Token，您必须使用自己在[Tushare Pro官网](https://tushare.pro)注册获取的Token。**

**方式一 (推荐，通过环境变量)**：
bash
Linux/Mac/WSL
export TUSHARE_TOKEN="你的token字符串"
Windows (PowerShell)
$env:TUSHARE_TOKEN="你的token字符串"
**方式二 (调用时传入)**：
在每次调用的JSON参数中添加 `"token": "你的_token_字符串"`。

### 3. 查看全部功能
调用本技能，传入以下参数，可列出所有支持的接口：
json
{
"api_name": "list"
}
### 4. 调用示例
**获取期货合约列表**：
json
{
"api_name": "fut_basic",
"exchange": "DCE",
"fields": "ts_code,symbol,name,list_date,delist_date"
}
**获取期货日线行情**：
json
{
"api_name": "fut_daily",
"ts_code": "CU2501.SHF",
"start_date": "20240101",
"end_date": "20240110"
}
## 支持的接口列表 (14个)
### 基础信息 (3个)
- `fut_basic` - 期货合约列表
- `trade_cal` - 期货交易日历
- `fut_mapping` - 主力合约映射

### 行情数据 (4个)
- `fut_daily` - 期货日线行情
- `fut_weekly_monthly` - 期货周/月线行情
- `ft_mins` - 期货分钟行情(历史)
- `rt_fut_min` - 期货实时分钟行情 **(需单独权限)**

### 仓单、结算与持仓排名 (3个)
- `fut_wsr` - 仓单日报
- `fut_settle` - 每日结算参数
- `fut_holding` - 成交持仓排名

### 指数数据 (1个)
- `index_daily` - 南华指数行情

### 统计与风险指标 (2个)
- `fut_weekly_detail` - 周期交易统计
- `ft_limit` - 涨跌停价格及保证金率

## 核心参数说明
| 参数名 | 必填 | 说明 | 常见值 |
|--------|------|------|--------|
| `api_name` | 是 | 要调用的期货接口名称 | 如 `fut_daily` |
| `token` | 否* | Tushare Token，不填则用环境变量 | 您的Token字符串 |
| `ts_code` | 否 | 合约代码 | `CU1811.SHF`, `A2503.DCE` |
| `trade_date` | 否 | 交易日期，`YYYYMMDD` | `20240115` |
| `exchange` | 否 | 交易所代码 | `DCE`(大商所), `SHFE`(上期所)等 |
| `symbol` | 否 | 品种代码 | `CU`(铜), `ZN`(锌) |
| `freq` | 否 | 数据频率 | 分钟:`1min`/`1MIN`；周月:`week`/`month` |
| `start_date` / `end_date`| 否 | 起止日期 | `YYYYMMDD` 或 `YYYY-MM-DD HH:MM:SS` |

\*：`token` 参数和环境变量 `TUSHARE_TOKEN` 必须至少提供一个。

## 典型示例
### 获取某交易所所有期货合约列表
json
{
"api_name": "fut_basic",
"exchange": "DCE",
"fields": "ts_code,symbol,name,list_date,delist_date,multiplier"
}
### 获取某日期全部期货合约日行情
json
{
"api_name": "fut_daily",
"trade_date": "20240115",
"exchange": "SHFE",
"fields": "ts_code,trade_date,open,high,low,close,settle,vol,oi"
}
### 获取铜期货5分钟历史数据
json
{
"api_name": "ft_mins",
"ts_code": "CU2501.SHF",
"freq": "5min",
"start_date": "2024-01-15 09:00:00",
"end_date": "2024-01-15 15:00:00"
}
## 重要提示
1.  **积分与权限**：不同接口需要不同的Tushare积分（通常2000积分起）。实时行情(`rt_fut_min`)等需要单独申请权限。
2.  **合约代码**：格式为 `品种+合约月份.交易所`，如 `CU2501.SHF`。
3.  **主力合约**：可通过 `fut_mapping` 接口查询连续/主力合约与具体月合约的映射。
4.  **时间格式**：注意区分日线(`YYYYMMDD`)和分钟线(`YYYY-MM-DD HH:MM:SS`)的时间格式。
5.  **官方文档**：完整参数和字段说明，请参考 [Tushare官方文档](https://tushare.pro/document/2)。

## 技能信息
- **版本**：1.0.1
- **接口数量**：14个
- **数据源**：Tushare Pro (期货板块)
- **最后更新**：2024年1月
- **依赖**：tushare>=1.2.89, pandas>=1.5.0