---
name: update-stock-mcp
description: >
  UpdateStock MCP 服务技能 v1.1 —— 通过 stdio 模式调用 UpdateStock 脚本，
  提供 A 股 DuckDB 数据库管理功能：创建数据库、全量/增量更新股票数据、查询股票行情。
  触发条件：用户提到"UpdateStock"、"创建股票数据库"、"更新股票数据"、"获取股票数据"、"ping 股票服务"等。
agent_created: true
---

# UpdateStock MCP 技能 v1.1

通过 stdio MCP 工具调用 UpdateStock 脚本，管理 A 股 DuckDB 数据库。

## 安装前准备

### 1. 填写 tushare API token

技能目录下已包含 `API_tushare.txt`（空白文件），**请先填入你自己的 tushare API token**，否则无法获取 tushare 数据。

获取方式：访问 https://tushare.pro/register 注册，登录后在个人中心复制 token，粘贴到 `API_tushare.txt` 中保存。

> 即使不填 token，脚本仍可通过 baostock（免费，无需注册）获取部分数据。

### 2. 安装 Python 依赖

在技能目录下运行：

```bash
pip install -r requirements.txt
```

所需依赖：
- `pandas` — 数据处理
- `numpy` — 数值计算
- `duckdb` — DuckDB 数据库引擎
- `tushare` — A 股数据接口（需注册获取 API token）
- `baostock` — 备用数据源（免费，无需 token）
- `mcp` — MCP Python SDK（提供 FastMCP）
- `pydantic` — 参数校验

### 3. 配置 MCP（stdio 模式）

在 `~/.workbuddy/mcp.json` 的 `mcpServers` 中添加：

```json
"UpdateStock": {
  "command": "python",
  "args": ["<skill-dir>/scripts/UpdateStock_skill.py"],
  "disabled": false
}
```

> `<skill-dir>` 替换为技能实际路径，如 `C:/Users/CMF/.workbuddy/skills/update-stock-mcp/scripts/UpdateStock_skill.py`
> 若系统 `python` 命令指向不正确，可替换为完整路径，如 `C:/Python312/python.exe`

配置完成后需重启 WorkBuddy 使 MCP 服务生效。

## 可用工具

### mcp__UpdateStock__ping — 连接检测

无参数。返回 `Pong` 表示服务正常。

调用方式：
```
DeferExecuteTool(toolName="mcp__UpdateStock__ping", params={})
```

### mcp__UpdateStock__Creat_DB — 创建数据库

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| DB_path | string | `""` | 数据库路径，留空则使用同目录下 `Test.duckdb` |

创建的表：stock、stock_index、stock_basic、stock_factor、stock_forecast、stock_dividend、stock_report

调用方式：
```
DeferExecuteTool(toolName="mcp__UpdateStock__Creat_DB", params={"DB_path": ""})
```

### mcp__UpdateStock__Update_Stock_Data — 全量更新

> ⚠️ **首次从 0 开始更新数据库耗时非常长（可能需数小时）**，请在空闲时运行，避免中途中断。
> 需要 tushare 积分 2000+。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| DB_path | string | `""` | 留空自动查找 `Test.duckdb` |
| API | string | `""` | tushare token，留空读取同目录 `API_tushare.txt` |
| ignore_check | boolean | `false` | 是否跳过部分检查 |

调用方式：
```
DeferExecuteTool(toolName="mcp__UpdateStock__Update_Stock_Data", params={
  "DB_path": "",
  "API": "",
  "ignore_check": false
})
```

### mcp__UpdateStock__Update_Stock_Data_easy — 增量更新

> 适合 tushare 积分 120 的用户，仅更新指数行情和股票行情两张表。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| DB_path | string | `""` | 留空自动查找 `Test.duckdb` |
| API | string | `""` | tushare token，留空读取同目录 `API_tushare.txt` |

调用方式：
```
DeferExecuteTool(toolName="mcp__UpdateStock__Update_Stock_Data_easy", params={
  "DB_path": "",
  "API": ""
})
```

### mcp__UpdateStock__get_stock — 获取非复权股票行情

从数据库查询指定股票、指定时间范围的非复权行情数据。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| symbol | string | `"000001"` | 股票代码（6位数字） |
| DB_path | string | `""` | 数据库路径，留空自动查找 `Test.duckdb` |
| start_date | string | `""` | 开始日期，格式 `YYYY-MM-DD` |
| end_date | string | `""` | 截止日期，格式 `YYYY-MM-DD` |

返回字段：trade_date, symbol, open, high, low, close, pre_close, vol, voe

调用方式：
```
DeferExecuteTool(toolName="mcp__UpdateStock__get_stock", params={
  "symbol": "000001",
  "DB_path": "",
  "start_date": "2026-05-01",
  "end_date": "2026-05-19"
})
```

### mcp__UpdateStock__get_adj_stock — 获取前复权股票行情

从数据库查询指定股票、指定时间范围的前复权行情数据（已自动处理分红送股除权）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| symbol | string | `"000001"` | 股票代码（6位数字） |
| DB_path | string | `""` | 数据库路径，留空自动查找 `Test.duckdb` |
| start_date | string | `""` | 开始日期，格式 `YYYY-MM-DD` |
| end_date | string | `""` | 截止日期，格式 `YYYY-MM-DD` |

返回字段：trade_date, symbol, open, high, low, close, vol, voe

调用方式：
```
DeferExecuteTool(toolName="mcp__UpdateStock__get_adj_stock", params={
  "symbol": "000001",
  "DB_path": "",
  "start_date": "2026-05-01",
  "end_date": "2026-05-19"
})
```

## 工作流程

### 数据更新流程
1. 调用 `ping` 确认 MCP 服务已连接
2. 首次使用先调用 `Creat_DB` 创建数据库
3. 根据 tushare 积分选择 `Update_Stock_Data`（2000+）或 `Update_Stock_Data_easy`（120）
   - **首次全量更新耗时极长，请在空闲时段运行，避免中途中断**
4. 检查返回信息确认操作结果

### 数据查询流程
1. 调用 `get_stock`（非复权）或 `get_adj_stock`（前复权）获取行情数据
2. 指定股票代码和时间范围
3. AI 可直接使用返回的 JSON 数据进行绘图、分析等操作

## 注意事项

- 脚本优先使用【全A解析】的数据库，缺失时才使用 `DB_path` 指定的路径
- tushare API token 可放入脚本同目录 `API_tushare.txt`，避免每次输入
- 查询无结果时返回友好提示字符串，而非报错
- 返回的 trade_date 格式为 `YYYY-MM-DD` 字符串，方便 AI 直接解析

## 版本历史

- **v1.1** - 新增 `get_stock` 和 `get_adj_stock` 工具，支持查询股票行情数据（支持时间范围过滤）
- **v1.0** - 初始版本，支持数据库创建和全量/增量更新
