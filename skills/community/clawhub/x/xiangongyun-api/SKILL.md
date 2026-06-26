---
name: xiangongyun-api
description: 仙宫云GPU云服务平台API集成工具，支持实例管理、私有镜像管理、账号管理等全量操作；当用户需要查询或管理仙宫云GPU实例、操作私有镜像、查询账户余额或充值时使用
dependency:
  python:
    - requests>=2.28.0
---

# 仙宫云API技能

## 任务目标
- 本技能用于：集成仙宫云开放平台API，实现对GPU云服务实例的完整生命周期管理
- 能力包含：实例管理（创建/启停/销毁）、私有镜像管理、账户信息查询与充值
- 触发条件：用户需要管理仙宫云GPU实例、操作镜像、查询账户信息时

## 前置准备
依赖说明：脚本依赖 requests 库
  ```
  requests>=2.28.0
  ```
- 依赖说明：脚本使用Python标准库和requests包，无需额外安装依赖
- 凭证配置：需要仙宫云API访问令牌，已在技能配置中完成授权

## 操作步骤

### 一、实例管理

#### 1. 查询实例
- **获取实例列表**：调用 `scripts/xiangongyun_api.py --action list_instances`
- **获取单个实例详情**：调用 `scripts/xiangongyun_api.py --action get_instance --instance-id <实例ID>`
- **获取实例储存的镜像**：调用 `scripts/xiangongyun_api.py --action list_instance_images --instance-id <实例ID>`

#### 2. 部署实例
- **部署新实例**：调用 `scripts/xiangongyun_api.py --action deploy_instance --name <实例名称> --gpu-count <GPU数量> --image <镜像名称> [--data-center <数据中心>] [--ssh-key <SSH密钥>] [--password <密码>]`
- 参数说明详见 [references/api_reference.md](references/api_reference.md)

#### 3. 实例生命周期操作
- **开机**：`--action boot_instance --instance-id <实例ID>`
- **关机保留GPU**：`--action shutdown_instance --instance-id <实例ID>`
- **关机释放GPU**：`--action shutdown_release_gpu --instance-id <实例ID>`
- **关机并销毁**：`--action shutdown_destroy --instance-id <实例ID>`
- **销毁实例**：`--action destroy_instance --instance-id <实例ID>`

#### 4. 镜像保存
- **储存镜像**：`--action save_image --instance-id <实例ID> --image-name <镜像名称>`
- **储存镜像并销毁**：`--action save_image_destroy --instance-id <实例ID> --image-name <镜像名称>`

### 二、私有镜像管理

- **获取镜像列表**：`--action list_images`
- **获取镜像详情**：`--action get_image --image-id <镜像ID>`
- **销毁镜像**：`--action destroy_image --image-id <镜像ID>`

### 三、账号管理

- **获取用户信息**：`--action get_user_info`
- **获取账户余额**：`--action get_balance`
- **创建充值订单**：`--action create_recharge_order --amount <金额> --payment <alipay|wechat>`
- **查询充值订单**：`--action query_recharge_order --trade-no <订单号>`

## 资源索引
- API脚本：见 [scripts/xiangongyun_api.py](scripts/xiangongyun_api.py)（封装所有API调用）
- API参考：见 [references/api_reference.md](references/api_reference.md)（完整的接口参数与响应说明）

## 注意事项
- 所有异步操作（部署、销毁、启停等）请求成功后会立即返回，实际执行状态需通过查询实例信息确认
- 关机释放GPU后，系统盘按已使用空间计费（¥0.00003/GB/小时）
- 充值订单的微信支付链接需转换为二维码扫码使用
- 公共镜像列表、实例状态说明详见API参考文档

### 示例1：查询账户信息
```bash
# 查看用户信息
python scripts/xiangongyun_api.py --action get_user_info

# 查看账户余额
python scripts/xiangongyun_api.py --action get_balance
```

### 示例2：管理GPU实例
```bash
# 获取所有实例列表
python scripts/xiangongyun_api.py --action list_instances

# 部署新实例（使用PyTorch镜像，2块GPU）
python scripts/xiangongyun_api.py --action deploy_instance --name "my-training" --gpu-count 2 --image "PyTorch 2.0.0"

# 查看实例详情
python scripts/xiangongyun_api.py --action get_instance --instance-id "abc123"

# 关机释放GPU（节省费用）
python scripts/xiangongyun_api.py --action shutdown_release_gpu --instance-id "abc123"

# 开机继续使用
python scripts/xiangongyun_api.py --action boot_instance --instance-id "abc123"
```

### 示例3：管理私有镜像
```bash
# 保存实例为镜像
python scripts/xiangongyun_api.py --action save_image --instance-id "abc123" --image-name "my-custom-image"

# 查看所有私有镜像
python scripts/xiangongyun_api.py --action list_images

# 删除镜像
python scripts/xiangongyun_api.py --action destroy_image --image-id "img456"
```

### 示例4：账户充值
```bash
# 创建充值订单（支付宝）
python scripts/xiangongyun_api.py --action create_recharge_order --amount 100 --payment alipay

# 查询订单状态
python scripts/xiangongyun_api.py --action query_recharge_order --trade-no "ORDER123456"
```
