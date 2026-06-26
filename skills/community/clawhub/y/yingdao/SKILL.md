---
name: yingdao
description: 影刀 RPA API 封装，支持鉴权/任务查询/执行/结果获取。需配置环境变量 YINGDAO_ACCESS_KEY_ID、YINGDAO_ACCESS_KEY_SECRET 作为 API 凭证。
meta:
  version: "2.2-python"
  provider: "yingdao"
  auth_type: "access_token"
  token_ttl: 7200
  endpoints:
    auth: "https://api.yingdao.com"
    business: "https://api.winrobot360.com"
requires:
  env:
    - YINGDAO_ACCESS_KEY_ID
    - YINGDAO_ACCESS_KEY_SECRET
primary_credential: env
publisher: "从0到1"
homepage: "https://clawhub.ai/yflmq001/yingdao"
---

# 影刀 RPA Skill

## 能力
- 🔐 鉴权：自动获取/刷新 accessToken
- 📋 任务：列表查询/详情获取/执行记录
- 🚀 执行：启动任务 + 动态传参 + 幂等控制
- 📊 结果：轮询状态 + 提取输出参数

## 安装方式

通过 ClawHub 安装：

```bash
clawhub install yingdao
```

### 依赖

本技能包依赖 Python 库 `requests`，安装技能后请确保已安装：

```bash
pip install -r requirements.txt
# 或
pip install "requests>=2.28.0"
```

安装完成并配置环境变量后即可使用（见下方「环境变量配置」）。

## 🐍 Python 模块使用

从包入口导入：`from active_skills.yingdao import YingdaoAPI, get_client, list_tasks, get_task_logs, YingdaoError, TokenExpiredError`。更多用法与参数说明见 `yingdao_api` 模块及各类、方法的 docstring。

### 最小示例

```python
from active_skills.yingdao import get_client, list_tasks, get_task_logs
client = get_client()
tasks = list_tasks(keyword="挂车")
logs = get_task_logs("挂车")
```

### API 速查

| 方法 / 函数 | 说明 |
|-------------|------|
| `YingdaoAPI` | 客户端类，支持 list_schedules、get_schedule_detail、get_task_records、get_today_records、start_task、query_task_result、find_task_by_name |
| `get_client()` | 从环境变量创建客户端 |
| `list_tasks(keyword, enabled)` | 查询任务列表 |
| `get_task_logs(task_name)` | 按任务名获取近期执行记录 |

## 接口速查（原始 API）

| 接口 | 方法 | 路径 | 关键参数 | 返回 |
|------|------|------|----------|------|
| 鉴权 | GET | `/oapi/token/v2/token/create` | accessKeyId, accessKeySecret | accessToken, expiresIn |
| 任务列表 | POST | `/oapi/dispatch/v2/schedule/list` | key, enabled, page, size | scheduleUuid, scheduleName |
| 任务详情 | POST | `/oapi/dispatch/v2/schedule/detail` | scheduleUuid | robotUuid, params, cron |
| 执行记录 | POST | `/oapi/dispatch/v2/task/list` | sourceUuid, cursorDirection, size | dataList, hasData, nextId |
| 启动任务 | POST | `/oapi/dispatch/v2/task/start` | scheduleUuid, params | taskUuid |
| 查询结果 | POST | `/oapi/dispatch/v2/task/query` | taskUuid | status, outputs |

## 参数规范

### 传参格式（task/start）
```json
{
  "scheduleUuid": "sched_xxx",
  "scheduleRelaParams": [{
    "robotUuid": "app_xxx",
    "params": [{"name": "order_id", "value": "ORD123", "type": "str"}]
  }]
}
```

## 环境变量配置

在使用前，需要设置以下环境变量：

```bash
export YINGDAO_ACCESS_KEY_ID="your_access_key_id"
export YINGDAO_ACCESS_KEY_SECRET="your_access_key_secret"
```

## 错误处理

异常类型：`YingdaoError`（通用）、`TokenExpiredError`（令牌过期）。调用时用 try-except 捕获即可，详见 `yingdao_api` 模块。

## Installation

安装与依赖见上文「安装方式」「依赖」「环境变量配置」。
