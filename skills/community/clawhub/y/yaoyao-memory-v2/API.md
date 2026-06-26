# API 路由文档

> yaoyao-memory API 服务器路由说明

---

## 路由列表

### 统计接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stats` | 获取记忆统计 |
| GET | `/api/activity` | 获取活动数据 |
| GET | `/api/daily` | 获取每日数据 |
| GET | `/api/system` | 获取系统信息 |

### 告警接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/alerts` | 获取告警列表 |

### 性能接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/performance` | 获取性能指标 |

### 数据接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/backups` | 获取备份列表 |
| GET | `/api/memory_trends` | 获取记忆趋势 |
| GET | `/api/memory_insights` | 获取记忆洞察 |
| GET | `/api/memory_quality` | 获取记忆质量 |

### 智能接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/smart_query` | 智能查询 |
| GET | `/api/query_predictor` | 查询预测 |
| GET | `/api/snapshot_list` | 快照列表 |

### 配置接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/features` | 获取功能开关 |
| GET | `/api/config` | 获取配置 |
| GET | `/api/get_password_status` | 获取密码状态 |

---

## 使用示例

```bash
# 获取统计
curl http://localhost:PORT/api/stats

# 获取系统信息
curl http://localhost:PORT/api/system
```

---

## 启动方式

```bash
python3 scripts/api_server.py
```

默认端口：查看 `api_server.py` 中的 `PORT` 常量
