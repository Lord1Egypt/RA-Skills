# 仙宫云API参考文档

## 目录
- [通用说明](#通用说明)
- [实例API](#实例api)
- [私有镜像API](#私有镜像api)
- [账号API](#账号api)
- [公共镜像列表](#公共镜像列表)
- [实例状态说明](#实例状态说明)

## 通用说明

### 基础信息
- **基础域名**: `https://api.xiangongyun.com`
- **认证方式**: 所有请求需在Header中携带 `Authorization` 字段，值为`Bearer <仙宫云访问令牌>`

### 通用响应格式
所有接口响应均为JSON格式，包含以下通用字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 响应代码，0表示成功 |
| msg | string | 消息文本 |
| success | bool | 操作是否成功 |

## 实例API

### 1. 获取实例列表

**请求**: `GET /open/instances`

**请求参数**: 无

**响应参数**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| list | []Instance | 实例列表 |
| total | int | 实例总数 |

**Instance字段说明**:

| 字段名称 | 类型 | 说明 |
|----------|------|------|
| id | string | 实例ID |
| create_timestamp | int64 | 创建时间戳 |
| data_center_name | string | 数据中心名称 |
| name | string | 实例名称 |
| public_image | string | 公共镜像名称 |
| gpu_model | string | GPU型号 |
| gpu_used | int | 已使用的GPU数量 |
| cpu_model | string | CPU型号 |
| cpu_core_count | int | CPU核心数 |
| memory_size | int64 | 内存大小(字节) |
| system_disk_size | int64 | 系统盘大小(字节) |
| data_disk_size | int64 | 数据盘大小(字节) |
| expandable_data_disk_size | int64 | 可扩展的数据盘大小(字节) |
| data_disk_mount_path | string | 数据盘挂载路径 |
| storage_mount_path | string | 存储挂载路径 |
| price_per_hour | float64 | 每小时价格 |
| ssh_key | string | SSH密钥 |
| ssh_port | string | SSH端口 |
| ssh_user | string | SSH用户 |
| password | string | 密码 |
| jupyter_token | string | Jupyter令牌 |
| jupyter_url | string | Jupyter URL |
| xgcos_token | string | XG COS令牌 |
| xgcos_url | string | XG COS URL |
| start_timestamp | int64 | 启动时间戳 |
| stop_timestamp | int64 | 停止时间戳 |
| status | string | 实例状态 |
| ssh_domain | string | SSH域名 |
| web_url | string | Web URL |
| progress | int | 进度 |
| image_id | string | 镜像ID |
| image_type | string | 镜像类型 |
| image_price | float64 | 镜像价格 |
| image_save | bool | 是否保存镜像 |
| base_price | float64 | 基础价格 |

---

### 2. 获取单个实例信息

**请求**: `GET /open/instance/{id}`

**路径参数**:

| 参数名 | 位置 | 类型 | 说明 | 是否必须 |
|--------|------|------|------|----------|
| id | 路径 | string | 实例ID | 是 |

**响应参数**: 与获取实例列表的Instance字段完全一致，额外包含实例状态说明

---

### 3. 获取实例储存的镜像

**请求**: `GET /open/instance/{id}/images`

**路径参数**:

| 参数名 | 位置 | 类型 | 说明 | 是否必须 |
|--------|------|------|------|----------|
| id | 路径 | string | 实例ID | 是 |

**响应参数**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| list | []Image | 储存的镜像列表 |
| total | int | 镜像总数 |

---

### 4. 部署实例

**请求**: `POST /open/instance/deploy`

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| name | string | 实例名称 | 是 |
| gpu_count | int | GPU数量 | 是 |
| image | string | 公共镜像名称 | 是 |
| data_center | string | 数据中心 | 否 |
| ssh_key | string | SSH密钥 | 否 |
| password | string | 密码 | 否 |
| image_id | string | 私有镜像ID(使用私有镜像时需要) | 否 |
| image_type | string | 镜像类型(使用私有镜像时需要) | 否 |

**响应参数**:

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | string | 实例ID |
| code | int | 响应代码 |
| msg | string | 消息文本 |
| success | bool | 操作是否成功 |

---

### 5. 销毁实例

**请求**: `POST /open/instance/destroy`

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| id | string | 实例ID | 是 |

**响应参数**:

| 参数名 | 类型 | 描述 |
|--------|------|------|
| code | int | 响应代码 |
| msg | string | 消息文本 |
| success | bool | 操作是否成功 |

---

### 6. 关机保留GPU

**请求**: `POST /open/instance/shutdown`

**说明**: 该操作为仅关机，关机后GPU会继续保留，期间实例照常收费。

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| id | string | 实例ID | 是 |

**响应参数**: 标准响应格式

---

### 7. 关机释放GPU

**请求**: `POST /open/instance/shutdown_release_gpu`

**说明**: 关机后GPU会被释放并不再计费。系统磁盘已使用空间以¥0.00003/GB/小时继续计费。

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| id | string | 实例ID | 是 |

**响应参数**: 标准响应格式

---

### 8. 关机并销毁

**请求**: `POST /open/instance/shutdown_destroy`

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| id | string | 实例ID | 是 |

**响应参数**: 标准响应格式

---

### 9. 开机

**请求**: `POST /open/instance/boot`

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| id | string | 实例ID | 是 |

**响应参数**: 标准响应格式

---

### 10. 储存镜像

**请求**: `POST /open/instance/saveimage`

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| id | string | 实例ID | 是 |
| image_name | string | 镜像名称 | 是 |

**响应参数**: 标准响应格式

---

### 11. 储存镜像并销毁

**请求**: `POST /open/instance/saveimage_destroy`

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| id | string | 实例ID | 是 |
| image_name | string | 镜像名称 | 是 |

**响应参数**: 标准响应格式

---

## 私有镜像API

### 1. 获取镜像列表

**请求**: `GET /open/images`

**请求参数**: 无

**响应参数**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| list | []Image | 镜像列表 |
| total | int | 镜像总数 |

**Image字段说明**:

| 字段名称 | 类型 | 说明 |
|----------|------|------|
| id | string | 镜像的唯一标识符 |
| create_timestamp | int64 | 镜像创建的时间戳 |
| name | string | 镜像的名称 |
| introduction | string | 镜像的简介 |
| size | int64 | 镜像的大小(字节) |
| visibility | int | 镜像的可见性 |
| status | string | 镜像的状态 |
| price | float64 | 镜像的价格 |
| save_image | int | 是否保存镜像(1为保存,0为不保存) |
| original_image_name | string | 原始镜像名 |
| original_image_id | string | 原始镜像ID |
| original_image_price | float64 | 原始镜像价格 |
| original_owner | bool | 当前用户是否为镜像的原始拥有者 |
| file_timestamp | int64 | 镜像文件最后更新时间 |

---

### 2. 获取镜像信息

**请求**: `GET /open/image/{id}`

**路径参数**:

| 参数名 | 位置 | 类型 | 说明 | 是否必须 |
|--------|------|------|------|----------|
| id | 路径 | string | 镜像ID | 是 |

**响应参数**: 与Image字段完全一致

---

### 3. 销毁镜像

**请求**: `POST /open/image/destroy`

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| id | string | 镜像ID | 是 |

**响应参数**: 标准响应格式

---

## 账号API

### 1. 获取用户信息

**请求**: `GET /open/whoami`

**请求参数**: 无

**响应参数**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| nickname | string | 用户昵称 |
| phone | string | 账户脱敏手机号码 |
| uuid | string | 用户唯一标识 |

---

### 2. 获取账户余额

**请求**: `GET /open/balance`

**请求参数**: 无

**响应参数**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| balance | float64 | 账户余额 |

---

### 3. 创建充值订单

**请求**: `POST /open/recharge/order`

**Body参数**:

| 参数名 | 类型 | 描述 | 是否必须 |
|--------|------|------|----------|
| amount | float64 | 金额 | 是 |
| payment | string | 支付方式：alipay或wechat | 是 |

**响应参数**:

| 字段名 | 类型 | 描述 |
|--------|------|------|
| url | string | 充值URL |
| amount | string | 金额 |
| trade_no | string | 交易订单号 |
| payment | string | 支付方式 |

**注意**: 充值URL中，alipay链接可在浏览器直接打开，wechat链接请转换为二维码使用微信APP扫码

---

### 4. 查询充值订单

**请求**: `GET /open/recharge/order/{trade_no}`

**路径参数**:

| 参数名 | 位置 | 类型 | 说明 | 是否必须 |
|--------|------|------|------|----------|
| trade_no | 路径 | string | 交易订单号 | 是 |

**响应参数**: 标准响应格式(含订单状态信息)

---

## 公共镜像列表

以下是部署实例时可使用的公共镜像名称：

| 镜像名称 | 说明 |
|----------|------|
| PyTorch 2.0.0 | PyTorch深度学习框架 |
| TensorFlow 2.x | TensorFlow深度学习框架 |
| CUDA 12.0 | NVIDIA CUDA开发环境 |
| Ubuntu 22.04 | Ubuntu操作系统 |
| 其他镜像 | 请参考仙宫云控制台查看最新镜像列表 |

**使用说明**: 在部署实例时，通过 `--image` 参数指定公共镜像名称。

---

## 实例状态说明

| 状态 | 说明 |
|------|------|
| running | 运行中 |
| stopped | 已停止 |
| deploying | 部署中 |
| destroying | 销毁中 |
| saving | 保存镜像中 |
| error | 错误状态 |

**注意**: 所有异步操作(部署、销毁、启停等)请求成功后会立即返回，实际执行状态需通过查询实例信息确认进度和结果。
