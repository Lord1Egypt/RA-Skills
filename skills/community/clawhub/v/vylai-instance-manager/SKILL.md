---
name: vylai-instance-manager
description: 管理无阶未来GPU云平台实例的创建、查询与删除操作；当用户需要创建GPU容器、查询实例状态、获取应用app_id或清理资源时使用
---

# Vylai 实例管理

管理无阶未来（Vylai）GPU云平台的实例生命周期，包括创建容器、查询状态和删除实例。

## 任务目标
- 管理无阶未来平台的GPU实例
- 支持创建、查询、删除实例操作
- 获取可用GPU资源列表
- 查询平台应用列表（获取app_id）

## 前置准备
- 需要在环境变量中设置 Vylai API Token
- Token 获取方式：登录 https://vylai.com 后进入「控制台」→「API」页面（https://vylai.com/console/api）获取

## GPU资源ID映射

| GPU ID | GPU型号 | 说明 |
|--------|---------|------|
| 1 | Geforce 4090 | 24GB显存 |
| 2 | Geforce 3090 | 24GB显存 |
| 3 | Tesla A100-SXM | 80GB显存 |
| 4 | Tesla A100-PCIE | 80GB显存 |
| 12 | Geforce 4090-48G | 48GB显存 |
| 13 | Geforce 5090 | 显存待确认 |
| 14 | CPU | 仅CPU计算 |

## 操作步骤

### 创建实例

1. 确定要使用的应用ID（app_id）和GPU类型
2. 生成唯一的task_id（建议使用业务相关标识符）
3. 调用创建脚本

```
python scripts/create_instance.py --app-id <应用ID> --gpu-id <GPU类型ID> --task-id <任务标识>
```

**参数说明:**
- `--app-id`: 应用ID，在平台主页点击"立即启动"获取
- `--gpu-id`: GPU资源ID（见上方映射表），默认为1（4090）
- `--task-id`: 唯一任务标识符，用于幂等控制，支持256字符
- `--gpu-num`: GPU数量（0-8），默认0表示使用应用默认值

**返回值:** container_id、container_status、create_time

### 查询实例状态

1. 获取所有实例列表
```
python scripts/query_instances.py
```

2. 查询指定实例（通过task_id）
```
python scripts/query_instances.py --task-id <任务ID>
```

**返回值:** 实例列表，包含task_id、container_id、status、deploy_name等

### 删除实例

1. 通过task_id删除
```
python scripts/delete_instance.py --task-id <任务ID>
```

2. 通过deploy_name删除
```
python scripts/delete_instance.py --deploy-name <实例名>
```

**说明:** 运行中的实例需先关机才能删除

### 获取GPU资源列表

```
python scripts/list_gpus.py
```

**返回值:** 平台所有可用GPU资源，包含价格、配置等信息

### 查询应用列表

获取平台公开应用和用户的私有应用，快速获取app_id用于创建实例。

```
python scripts/list_apps.py
```

**参数说明:**
- `--page`: 页码，默认1
- `--limit`: 每页数量，默认20
- `--search`: 搜索关键词
- `--no-token`: 不使用token，仅获取公开应用

**返回值:** 应用列表，包含id、name、description、owner、price等

**说明:**
- 带Token：返回公开应用 + 用户的私有应用
- 不带Token：仅返回公开应用

## 使用示例

### 示例1：创建4090 GPU实例
- 场景: 创建一个使用Geforce 4090的AI训练容器
- 输入: app-id=123, gpu-id=1, task-id=my-training-001
- 预期产出: 返回container_id和状态

### 示例2：查询并清理闲置实例
- 场景: 查看当前所有实例，找出闲置容器
- 输入: 无参数调用query_instances.py
- 预期产出: 实例列表，筛选status非running的实例

### 示例3：删除指定任务
- 场景: 清理已完成训练的任务容器
- 输入: task-id=my-training-001
- 预期产出: 删除成功确认

## 资源索引

- 脚本-创建实例: 见 [scripts/create_instance.py](scripts/create_instance.py)(用途: 创建GPU容器实例)
- 脚本-查询实例: 见 [scripts/query_instances.py](scripts/query_instances.py)(用途: 查询实例状态)
- 脚本-删除实例: 见 [scripts/delete_instance.py](scripts/delete_instance.py)(用途: 删除GPU容器实例)
- 脚本-GPU列表: 见 [scripts/list_gpus.py](scripts/list_gpus.py)(用途: 获取可用GPU资源)
- 脚本-应用列表: 见 [scripts/list_apps.py](scripts/list_apps.py)(用途: 获取应用列表和app_id)
- 参考-API文档: 见 [references/api-reference.md](references/api-reference.md)(何时读取: 需要详细API说明时)

## 注意事项

- task_id 具有幂等性：相同task_id不会重复创建容器
- 运行中实例删除前需先关机
- 包月计费实例不能通过API删除
- API调用限流：创建接口每1秒最多1次，删除接口每1秒最多5次
- 创建接口返回waiting状态表示容器正在创建中，需后续轮询查询状态
