# 无阶未来 API 参考文档

## 目录

- [基础信息](#基础信息)
- [认证方式](#认证方式)
- [API端点](#api端点)
- [GPU资源ID映射](#gpu资源id映射)
- [错误码说明](#错误码说明)

## 基础信息

- **API基础URL**: `https://api.vylai.com`
- **协议**: HTTPS
- **数据格式**: JSON

## 认证方式

所有API请求需要在Header中携带认证Token：

```
X-Auth-Token: <your-api-token>
```

Token获取方式：登录无阶未来平台（https://vylai.com），进入「控制台」→「API」页面（https://vylai.com/console/api）获取。

## API端点

### 0. 获取应用列表

**接口**: `GET /app/app`

获取平台公开应用列表，带Token可同时获取用户的私有应用。

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 页码，默认1 |
| limit | integer | 否 | 每页数量，默认20 |
| search_string | string | 否 | 搜索关键词 |

**请求头**:
```
X-Auth-Token: <token>  // 可选，不带则仅获取公开应用
```

**响应示例**:
```json
{
    "v": "0.0.2",
    "code": 200,
    "msg": "success",
    "data": {
        "total": 69,
        "list": [
            {
                "id": "b390",
                "name": "ComfyUI 适配5090 推荐",
                "image_description": "已安装常用节点和模型，推荐使用",
                "owner_name": "无阶未来",
                "gpu_num": 1,
                "price": 0.0
            }
        ]
    }
}
```

**说明**: 不传Token只返回公开应用，传Token可同时返回用户的私有应用。

### 1. 获取GPU资源列表

**接口**: `GET /market/allgpus`

获取平台所有可用的GPU资源信息。

**请求头**:
```
X-Auth-Token: <token>
```

**响应示例**:
```json
{
    "v": "0.0.2",
    "code": 200,
    "msg": "success",
    "data": {
        "gpu_dict": {
            "1": [1, 2, 3, 4, 12, 13, 14],
            "2": [1, 2, 3, 4, 12, 13, 14],
            "4": [1, 2, 3, 4, 12, 13, 14],
            "8": [2, 12, 4, 14]
        },
        "toptype_dict": {
            "1": {
                "name": "Geforce 4090",
                "tflops": 330,
                "mem": 24,
                "price_per_hour": 1.88,
                "price_per_day": 40,
                "availableGpu": [1, 2, 4]
            }
        },
        "total": 12
    }
}
```

### 2. 创建容器实例

**接口**: `POST /api/v1/app/create`

使用应用ID创建GPU容器。

**请求头**:
```
X-Auth-Token: <token>
Content-Type: application/json
```

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| task_id | string | 是 | 任务唯一标识符，用于幂等控制 |
| app_id | string | 是 | 应用ID |
| gpu_id | integer | 是 | GPU资源ID |
| gpu_num | integer | 否 | GPU数量，默认0使用应用默认值 |
| accessory | object | 否 | 自定义附加信息 |

**请求示例**:
```json
{
    "task_id": "my-training-task-001",
    "app_id": "123",
    "gpu_id": 1,
    "gpu_num": 0,
    "accessory": {"note": "训练任务"}
}
```

**响应示例**:
```json
{
    "v": "0.0.2",
    "code": 200,
    "msg": "任务创建成功",
    "data": {
        "task_id": "my-training-task-001",
        "container_id": 12345,
        "container_status": "waiting",
        "create_time": "2024-01-15 10:30:00",
        "update_time": "2024-01-15 10:30:00"
    }
}
```

### 3. 查询所有实例状态

**接口**: `GET /api/v1/app/status`

查询当前用户所有实例的状态。

**请求头**:
```
X-Auth-Token: <token>
```

**响应示例**:
```json
{
    "v": "0.0.2",
    "code": 200,
    "msg": "success",
    "data": {
        "tasks": [
            {
                "task_id": "my-training-task-001",
                "container_id": 12345,
                "container_info": {
                    "deploy_name": "abc123def456",
                    "status": "running",
                    "gpu_type": "Geforce 4090",
                    "gpu_num": 1
                },
                "create_time": "2024-01-15 10:30:00",
                "update_time": "2024-01-15 10:35:00"
            }
        ]
    }
}
```

### 4. 查询指定实例状态

**接口**: `POST /api/v1/app/status`

通过task_id数组查询指定实例。

**请求头**:
```
X-Auth-Token: <token>
Content-Type: application/json
```

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| task_ids | array[string] | 是 | task_id数组 |

**请求示例**:
```json
{
    "task_ids": ["task-001", "task-002"]
}
```

### 5. 删除实例（通过task_id）

**接口**: `DELETE /api/v1/app/delete/{task_id}`

通过任务ID删除实例。

**路径参数**:
- `task_id`: 任务唯一标识符

**请求头**:
```
X-Auth-Token: <token>
```

**响应示例**:
```json
{
    "v": "0.0.2",
    "code": 200,
    "msg": "删除成功",
    "data": null
}
```

### 6. 删除实例（通过实例ID）

**接口**: `DELETE /api/v1/deploy/delete/{deploy_name}`

通过容器部署名称删除实例。

**路径参数**:
- `deploy_name`: 容器部署名称（实例ID）

**请求头**:
```
X-Auth-Token: <token>
```

**deploy_name获取方式**:
- 从查询接口返回的 `container_info.deploy_name` 获取
- 从容器内部的hostname提取（格式: `{deploy_name}-{pod_suffix}`）

## GPU资源ID映射

| GPU ID | 型号名称 | 显存 | 说明 |
|--------|----------|------|------|
| 1 | Geforce 4090 | 24GB | 性价比之选 |
| 2 | Geforce 3090 | 24GB | 上代旗舰 |
| 3 | Tesla A100-SXM | 80GB | 大显存高性能 |
| 4 | Tesla A100-PCIE | 80GB | 大显存高性能 |
| 12 | Geforce 4090-48G | 48GB | 大显存版4090 |
| 13 | Geforce 5090 | - | 新一代显卡 |
| 14 | CPU | - | 仅CPU计算 |
| 15 | 4080 Super 32G | 32GB | 中高端选择 |

## 错误码说明

### HTTP状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误或业务逻辑错误 |
| 401 | Token验证失败 |
| 404 | 资源不存在 |
| 422 | 参数验证错误 |
| 500 | 服务器内部错误 |

### 业务错误码

| code | 说明 |
|------|------|
| 200 | 操作成功 |
| 234 | 任务已存在（幂等性返回） |
| 400 | 业务逻辑错误（如包月容器不能删除） |
| 401 | Token验证失败 |
| 444 | 资源不存在或参数错误 |
| 422 | 参数验证错误 |

### 常见错误消息

- `Token验证失败`: API Token无效或过期
- `GPU不存在`: 指定的GPU资源ID不存在
- `App不存在`: 指定的应用ID不存在
- `余额不足`: 账户余额不足以创建实例
- `包月容器不能删除`: 包月计费容器不支持API删除
- `任务不存在`: 指定的task_id不存在
- `任务已删除`: 任务已处于删除状态
- `请先关机`: 运行中的容器需先关机才能删除
