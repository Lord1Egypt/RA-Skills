# 任务管理

**⚠️ task_id 由系统自动生成，无需用户输入。**

## 创建任务

### 接口

```
POST /biyi.srv/user/use.cash.task
```

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_name` | string | ✅ | 任务名称（任意字符串） |
| `timestamp` | int | ✅ | 毫秒时间戳 |
| `tpl_code` | string | ✅ | 模板代码，固定 `hook` |
| `num` | int | ✅ | 任务数量，通常 `1` |
| `timbre_id` | int | ❌ | 音色ID（后续指定音色时传） |

### 请求示例

```json
{
  "file_name": "我的影视解说",
  "timestamp": 1742371200000,
  "tpl_code": "hook",
  "num": 1
}
```

### 响应示例（成功）

```json
{
  "err_code": -1,
  "msg": "success",
  "data": {
    "task_id": 123456,
    "record_id": "rec_xxx"
  }
}
```

### 响应示例（失败）

```json
{
  "err_code": 1001,
  "msg": "余额不足",
  "data": null
}
```

### 关键字段说明

- `task_id`（即 `server_task_id`）：**贯穿全流程的核心ID**，后续所有接口都需要传此值
- `record_id`：任务记录ID，用于关联查询

### 错误码

| err_code | 说明 |
|----------|------|
| `-1` | 成功 |
| 其他 | 失败（余额不足/参数错误等） |

### 注意事项

- 创建任务会消耗积分/余额，执行前需确认余额充足
- `server_task_id` 是后续所有步骤的必传参数，**创建任务失败则无法继续**
- `tpl_code` 必须传 `hook`，否则可能返回参数错误
