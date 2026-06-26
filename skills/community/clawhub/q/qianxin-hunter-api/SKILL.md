---
name: qianxin-hunter-api
description: 奇安信 Hunter API 调用技能。支持查询接口和导出任务（批量查询）。需配置 QIANXIN_HUNTER_API_KEY 环境变量。
compatibility: Python 3.10+
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": [ "python3" ], "env": [ "QIANXIN_HUNTER_API_KEY" ] }, "primaryEnv": "QIANXIN_HUNTER_API_KEY" } }
---

# 🔍 Qianxin Hunter Api

本工具集成奇安信 Hunter 平台的**查询接口**和**导出任务**（**批量查询**），可通过命令行处理：语法查询、提交导出（批量查询）任务、查询导出进度、下载导出文件。

## 📦 依赖

- Python 3.10+
- Python Package `requests`
- 需配置环境变量

```bash
QIANXIN_HUNTER_API_KEY="XXXXX"
```

## 🚀 核心功能用例

### 1. 查询接口

适用于快速检索小批量数据分页获取，直接在终端查看结果。

```bash
# 仅指定查询语法，其他参数默认（默认获取第1页数据）
python3 scripts/query.py --search 'web.title="login"'

# 指定查询语法，其他可选参数：分页参数、时间范围、返回字段、资产类型（is_web）
python3 scripts/query.py --search 'app="OpenClaw"' --page 1 --page_size 10 --start '2026-01-01' --end '2026-03-01' --fields 'ip,port,domain' --is_web 1
```

### 2. 导出任务（批量查询）

适用于大规模资产导出，也适用于批量ip/domain/company目标查询导出，导出结果通过csv文件形式下载。

#### 第一步：提交任务 (`submit`)

支持通过**语法**或**本地 CSV 文件**提交。

* **语法方式**：

    ```bash
    # 仅指定查询语法进行导出，其他参数默认（默认返回可导出的全部数据）
    python3 scripts/query.py submit --search 'ip="1.1.1.1/24" && ip.port="80"' 
    
    # 指定查询语法进行导出，其他可选参数：最大返回的资产数、时间范围、返回字段、资产类型（is_web）
    python3 scripts/query.py submit --search 'ip="1.1.1.1/24" && ip.port="80"' --limit 500 --start '2026-01-01' --end '2026-03-01' --fields 'ip,port,domain' --is_web 1
    ```
* **文件方式**（需符合官方模板）：

    ```bash
    # 指定本地csv文件进行导出，文件类型默认为all（可以是ip、domain和company混合的文件）
    python3 scripts/query.py submit --file targets.csv
    
    # 指定本地csv文件进行导出，文件类型为ip
    python3 scripts/query.py submit --file targets.csv --type ip
    
    # 指定本地csv文件进行导出，文件类型为domain，其他可选参数：最大返回的资产数、时间范围、返回字段、资产类型（is_web）
    python3 scripts/query.py submit --file targets.csv --type domain --limit 500 --start '2026-01-01' --end '2026-03-01' --fields 'ip,port,domain' --is_web 1
    ```

#### 第二步：查看进度 (`status`)

使用提交任务返回的 `task_id` 追踪状态。

```bash
python3 scripts/query.py batch status --task_id 1234
```

#### 第三步：下载结果 (`download`)

当状态显示为“已完成”时，下载导出的 CSV 文件。

```bash
# 仅指定task_id，不指定保存文件名，默认保存文件名为 results_{task_id}.csv
python3 scripts/query.py batch download --task_id 1234

# 指定task_id，指定保存文件名
python3 scripts/query.py batch download --task_id 1234 --output results.csv
```

---

## 📋 参数速查表

### 全局子命令

- `search`: 查询模式。
- `batch`: 批量导出模式（含 `submit`, `status`, `download` 动作）。

### 查询参数

| 长参数           | 说明                                                                                              |
|:--------------|:------------------------------------------------------------------------------------------------|
| `--search`    | Hunter 查询语法（原始字符串），用于即时查询或批量查询/导出任务                                                             |
| `--page`      | 页码，默认 `1`                                                                                       |
| `--page_size` | 每页条数，默认 `10`                                                                                    |
| `--start`     | 开始时间 (格式: `2021-01-01`)                                                                         |
| `--end`       | 结束时间 (格式: `2021-03-01`)                                                                         |
| `--is_web`    | 资产类型：`1` (Web), `2` (非Web), `3` (全部)，默认为全部。                                                     |
| `--fields`    | 返回字段，以逗号分隔（如 `ip,port,domain`），默认返回权限内所有可导出字段。                                                  |
| `--file`      | 上传的CSV文件路径，用于批量查询                                                                               |
| `--type`      | 上传文件的类型，即检索类型：`all` (混合ip/domain/company), `ip`(批量ip), `domain`(批量域名), `company`(批量企业名称)，用于批量查询 |
| `--limit`     | 最大导出资产数                                                                                         |
| `--task_id`   | 任务 ID，用于查看进度或下载文件                                                                               |
| `--output`    | 下载的输出文件名，用于下载文件命名                                                                               |

## 🛠️ 脚本工具

- `scripts/query.py`

## 📚 参考文档

- `reference/api.md`: Hunter 查询接口文档
- `reference/api_batch.md`: Hunter 批量查询相关接口文档
- `reference/batch_file_template.csv`: 批量查询时使用的上传文件模板