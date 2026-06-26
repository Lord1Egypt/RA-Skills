# XLink IoT CLI 命令参考

详细的命令行接口参考文档。

---

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `XLINK_BASE_URL` | 否 | 网关基础 URL (默认：`https://api-gw.xlink.cn`) |
| `XLINK_APP_ID` | 是 | 网关应用 ID |
| `XLINK_APP_SECRET` | 是 | 网关应用密钥 |
| `XLINK_API_GROUP` | 是 | 网关组 ID |

---

## CLI 命令详解

### `overview` - 设备概览

获取设备数量和状态分布。

```bash
python scripts/xlink_api.py overview [--json]
```

**选项：**
- `--product-id ID` - 按产品 ID 过滤
- `--project-id ID` - 按项目 ID 过滤
- `--json` - 输出 JSON 格式

**示例：**
```bash
# 总体概览
python scripts/xlink_api.py overview

# 按产品过滤
python scripts/xlink_api.py overview --product-id 160593ec01

# JSON 输出
python scripts/xlink_api.py overview --json
```

**输出示例：**
```
==================================================
📊 XLINK 设备概览
==================================================

   📱 设备总数：      120034
   🟢 在线：          87433 (72.0%)
   ✅ 已激活：        110223 (91.0%)
   ⚫ 离线：          32601
   ⏸️  未激活：        9811
```

---

### `device-list` - 设备列表

查询设备列表，支持分页和高级过滤。

```bash
python scripts/xlink_api.py device-list [options]
```

**选项：**
- `--offset N` - 分页偏移量 (默认：0)
- `--limit N` - 每页数量 1-100 (默认：20)
- `--filter JSON` - 过滤配置 JSON 字符串
- `--query JSON` - 查询条件 JSON 字符串
- `--order JSON` - 排序配置 JSON 字符串
- `--json` - 输出 JSON 格式

**过滤配置示例：**
```json
{
  "device": ["mac", "id", "name", "project_id"],
  "online": ["is_online"],
  "vdevice": ["last_login"]
}
```

**查询配置示例：**
```json
{
  "logic": "AND",
  "device": {
    "project_id": {"$eq": "XJA1JJAJA"},
    "$or": [
      {"tags_map": {"$elemMatch": {"key": {"$eq": "Project"}, "value": {"$eq": "青创汇"}}}}
    ]
  }
}
```

**示例：**
```bash
# 基本列表
python scripts/xlink_api.py device-list --limit 20

# 带过滤
python scripts/xlink_api.py device-list --filter '{"device":["id","name","mac"],"online":["is_online"]}'

# 复杂查询
python scripts/xlink_api.py device-list --query '{"logic":"AND","device":{"project_id":{"$eq":"XJA1JJAJA"}}}'

# 带排序
python scripts/xlink_api.py device-list --order '{"device":{"create_time":"desc"}}'
```

---

### `device-trend` - 设备统计趋势

按时间粒度获取设备统计趋势数据。

```bash
python scripts/xlink_api.py device-trend --start-time <iso> --end-time <iso> [options]
```

**选项：**
- `--start-time ISO` - 开始时间 ISO 8601 (必需)
- `--end-time ISO` - 结束时间 ISO 8601 (必需)
- `--granularity {hour,day,week,month}` - 时间粒度 (默认：day)
- `--json` - 输出 JSON 格式

**示例：**
```bash
# 最近 7 天，按天
python scripts/xlink_api.py device-trend --start-time "2026-03-19T09:40" --end-time "2026-03-26T09:40"

# 最近 24 小时，按小时
python scripts/xlink_api.py device-trend --start-time "2026-03-23T09:40" --end-time "2026-03-24T09:40" --granularity hour
```

---

### `device-history` - 设备属性历史

获取多个设备的历史属性快照数据。

```bash
python scripts/xlink_api.py device-history --device-ids <ids> [options]
```

**选项：**
- `--device-ids IDS` - 逗号分隔的设备 ID (必需)
- `--offset N` - 分页偏移量 (默认：0)
- `--limit N` - 每页数量 1-100 (默认：20)
- `--start-time TS` - 开始时间戳 (毫秒)
- `--end-time TS` - 结束时间戳 (毫秒)
- `--rule-id ID` - 快照规则 ID
- `--sort-by-date {asc,desc}` - 排序 (默认：desc)
- `--json` - 输出 JSON 格式

**示例：**
```bash
# 获取多个设备历史
python scripts/xlink_api.py device-history --device-ids 1000,1002,1005

# 带时间范围
python scripts/xlink_api.py device-history --device-ids 1000,1002 --start-time 1711008000000 --end-time 1711612800000

# 升序排序
python scripts/xlink_api.py device-history --device-ids 1000 --limit 50 --sort-by-date asc
```

---

### `device-latest` - 设备最新属性

批量获取多个设备的最新属性信息。

```bash
python scripts/xlink_api.py device-latest [options]
```

**选项：**
- `--device-ids IDS` - 逗号分隔的设备 ID
- `--product-ids IDS` - 逗号分隔的产品 ID
- `--offset N` - 分页偏移量 (默认：0)
- `--limit N` - 每页数量 1-10000 (默认：10)
- `--load-exception` - 加载异常信息
- `--json` - 输出 JSON 格式

**示例：**
```bash
# 按设备 ID 查询
python scripts/xlink_api.py device-latest --device-ids 228546143,1839137554

# 按产品 ID 查询
python scripts/xlink_api.py device-latest --product-ids 16a8b0d3133f000116a8b0d3133fc801

# 带异常信息
python scripts/xlink_api.py device-latest --device-ids 1000 --load-exception
```

---

### `device-control` - 设备控制

通过调用物模型服务控制设备。

```bash
python scripts/xlink_api.py device-control --thing-id <id> --service <name> --input <json> [options]
```

**选项：**
- `--thing-id ID` - 设备 ID (必需)
- `--service NAME` - 服务名称 (必需)
- `--input JSON` - 输入参数 JSON (必需)
- `--ttl SEC` - 命令缓存时长 秒 (1-864000)
- `--json` - 输出 JSON 格式

**服务名称：**
- `device_attribute_set_service` - 设置设备属性 (最常用)
- 其他产品物模型中定义的服务

**示例：**
```bash
# 设置色温
python scripts/xlink_api.py device-control \
  --thing-id 10299402 \
  --service device_attribute_set_service \
  --input '{"ColorTemperature": 8}'

# 开启设备
python scripts/xlink_api.py device-control \
  --thing-id 10299402 \
  --service device_attribute_set_service \
  --input '{"Power": 1}'

# 带命令缓存 (10 分钟)
python scripts/xlink_api.py device-control \
  --thing-id 10299402 \
  --service device_attribute_set_service \
  --input '{"Brightness": 100}' \
  --ttl 600
```

**响应码：**
| 码 | 说明 |
|------|-------------|
| `200` | 成功 - 设备已响应 |
| `202` | 设备离线 - 命令未下发 |
| `408` | 连接关闭 - 设备休眠 |
| `503` | 控制失败 - 无响应或无效服务 |

---

### `alert-overview` - 告警概览

获取告警统计（新增、历史、设备告警、告警率）。

```bash
python scripts/xlink_api.py alert-overview [options]
```

**选项：**
- `--product-id ID` - 按产品 ID 过滤
- `--project-id ID` - 按项目 ID 过滤
- `--json` - 输出 JSON 格式

**输出示例：**
```
==================================================
⚠️  XLINK 告警概览
==================================================

   🆕 新增告警：        0
   📚 历史告警：        143
   📱 设备告警：        112
   📊 告警率：          1.43%
```

---

### `alert-statistics` - 告警时间序列统计

获取设备告警统计时间序列数据（最近 24 小时或自定义范围）。

```bash
python scripts/xlink_api.py alert-statistics [options]
```

**选项：**
- `--product-id ID` - 按产品 ID 过滤
- `--project-id ID` - 按项目 ID 过滤
- `--interval {hour,day}` - 时间粒度 (默认：hour)
- `--start-time ISO` - 开始时间 ISO 8601
- `--end-time ISO` - 结束时间 ISO 8601
- `--json` - 输出 JSON 格式

**示例：**
```bash
# 最近 24 小时 (默认)
python scripts/xlink_api.py alert-statistics

# 按天粒度
python scripts/xlink_api.py alert-statistics --interval day

# 自定义时间范围
python scripts/xlink_api.py alert-statistics \
  --start-time "2026-02-10T00:00:00.000Z" \
  --end-time "2026-02-10T23:59:59.999Z"

# 按项目过滤
python scripts/xlink_api.py alert-statistics --project-id ab582
```

---

### `event-instances` - 事件实例查询

查询事件实例，支持多种过滤条件。

```bash
python scripts/xlink_api.py event-instances [options]
```

**选项：**
- `--status N` - 事件状态 (逗号分隔：1/2/3 或 pending/processing/processed)
- `--start-time ISO` - 创建时间大于 (ISO 8601)
- `--end-time ISO` - 创建时间小于 (ISO 8601)
- `--device-id ID` - 设备 ID
- `--event-ids IDS` - 事件 ID 列表
- `--project-ids IDS` - 项目 ID 列表
- `--device-name NAME` - 设备名称 (模糊查询)
- `--name NAME` - 事件名称 (模糊查询)
- `--processed-ways N` - 处理方式 (逗号分隔)
- `--offset N` - 分页偏移量 (默认：0)
- `--limit N` - 每页数量 1-100 (默认：10)
- `--json` - 输出 JSON 格式
- `--debug` - 启用调试日志

**状态值：**
| 值 | 说明 |
|------|-------------|
| `1` | 🟡 待处理 |
| `2` | 🟠 处理中 |
| `3` | 🟢 已处理 |

**处理方式：**
| 值 | 说明 |
|------|-------------|
| `-1` | 未处理 |
| `1` | 设备调试 |
| `2` | 真实故障 |
| `3` | 误报 |
| `4` | 其他 |
| `5` | 转工单 |
| `6` | 抑制 |
| `7` | 自动恢复 |

**示例：**
```bash
# 最新 50 个事件
python scripts/xlink_api.py event-instances --limit 50

# 待处理事件
python scripts/xlink_api.py event-instances --status 1

# 特定设备的已处理事件
python scripts/xlink_api.py event-instances --device-id 12345 --status 3

# 时间范围内的事件
python scripts/xlink_api.py event-instances \
  --start-time "2026-03-01T00:00:00.00Z" \
  --end-time "2026-03-31T23:59:59.99Z"

# 误报事件
python scripts/xlink_api.py event-instances --processed-ways 3
```

---

## Python API 使用

使用 `XlinkIoTClient` 类进行编程访问：

```python
import sys
sys.path.insert(0, "scripts")
from xlink_api import XlinkIoTClient

# 初始化客户端 (从环境变量读取配置)
client = XlinkIoTClient()

# 设备概览
overview = client.get_device_overview(product_id="160593ec01")
print(f"Total: {overview.get('total')}, Online: {overview.get('online')}")

# 设备列表
devices = client.get_device_list(limit=50)

# 告警概览
alerts = client.get_alert_overview(project_id="ab582")

# 事件实例
events = client.get_event_instances(status="ACTIVE", limit=50)

# 设备控制
result = client.control_device(
    thing_id="10299402",
    service="device_attribute_set_service",
    input_params={"ColorTemperature": 8}
)
```

详细 API 方法请参考 `xlink_api.py` 源码。
