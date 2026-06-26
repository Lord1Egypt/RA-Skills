# TencentCloud-Manager - 腾讯云资源统一管理技能

## 📋 技能说明

**腾讯云资源统一管理入口**，提供 CVM 云服务器、Lighthouse 轻量应用服务器、COS 对象存储的创建、配置和运维管理。

### 入口组件

本技能是腾讯云管理的**统一入口**。你也可以直接使用各分支技能：

| 技能 | 说明 | 引用 |
|------|------|------|
| tencentcloud-cvm | CVM 云服务器管理 | `from tencentcloud_cvm import CVMManager` |
| tencentcloud-lighthouse | Lighthouse 轻量服务器管理 | `from tencentcloud_lighthouse import LighthouseManager` |
| tencentcloud-cos | COS 对象存储管理 | `from tencentcloud_cos import COSManager` |
| tencentcloud-ops | CVM + COS 运维工具包 | `from tencentcloud_ops import CVMManager, COSManager` |

### 核心功能

✅ **资源创建与配置**
- CVM 云服务器实例管理
- Lighthouse 轻量服务器管理
- COS 存储桶与文件管理

✅ **运维管理**
- 实例启停与重启
- 监控与状态查询
- 生命周期管理
- 批量操作

✅ **成本优化**
- 促销方案查询与对比
- 存储类型成本估算
- 资源配置建议

✅ **安全管理**
- 子用户权限配置
- 凭证外部化管理
- 操作审计日志

---

## 💰 价格参考

> ⚠️ **注意**: 以下价格为参考区间（更新于 2026-03-29），实际价格以腾讯云官网实时查询为准。

### CVM 云服务器

| 方案类型 | 2 核 4G 参考 | 特点 |
|----------|-------------|------|
| 新人特惠 | ~¥150-200/年 | 限新用户 |
| 按量付费 | ~¥120-150/月 | 灵活 |
| 竞价实例 | ~¥30-50/月 | 最高 90% OFF |

### Lighthouse 轻量服务器

| 方案类型 | 2 核 2G 参考 | 特点 |
|----------|-------------|------|
| 新人特惠 | ~¥80-120/年 | 限新用户 |
| 包年包月 | ~¥400-500/年 | 价格稳定 |

### COS 对象存储

| 存储类型 | 参考价格 | 适用 |
|----------|---------|------|
| 标准存储 | ~¥0.12-0.15/GB/月 | 频繁访问 |
| 低频存储 | ~¥0.07-0.09/GB/月 | 不常访问 |
| 归档存储 | ~¥0.02-0.04/GB/月 | 长期保存 |

### 查询实时价格

```python
from tencentcloud_manager import TencentCloudManager

tcm = TencentCloudManager()

# 查询 CVM 促销
tcm.show_promotions(service='cvm')

# 查询 Lighthouse 促销
tcm.show_promotions(service='lighthouse')
```

---

## ⚠️ 前置配置 (必须完成)

### 步骤 1: 创建腾讯云子用户

1. 访问 https://console.cloud.tencent.com/cam/capi
2. 登录腾讯云账号
3. 创建子用户（如：`resource-manager`）
4. 复制 SecretId 和 SecretKey

### 步骤 2: 配置子用户权限

**推荐策略**: 创建自定义策略，授予最小必要权限

#### CVM 管理权限

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "cvm:Describe*", "cvm:RunInstances", "cvm:StartInstances",
        "cvm:StopInstances", "cvm:RestartInstances", "cvm:ModifyInstancesAttribute",
        "cvm:RenewInstances", "vpc:DescribeSecurityGroups", "vpc:CreateSecurityGroup"
      ],
      "resource": "*"
    }
  ]
}
```

#### Lighthouse 管理权限

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "lighthouse:Describe*", "lighthouse:CreateInstance",
        "lighthouse:StartInstances", "lighthouse:StopInstances",
        "lighthouse:RestartInstances", "lighthouse:ModifyInstancesAttribute",
        "lighthouse:RenewInstance"
      ],
      "resource": "*"
    }
  ]
}
```

#### COS 管理权限

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "name/cos:GetBucket", "name/cos:PutBucket", "name/cos:ListBucket",
        "name/cos:GetObject", "name/cos:PutObject", "name/cos:DeleteObject",
        "name/cos:PutBucketLifecycle", "name/cos:GetBucketLifecycle"
      ],
      "resource": "*"
    }
  ]
}
```

### 步骤 3: 配置凭证到.env 文件

```bash
cp skills/tencentcloud-manager/config/.env.example \
   skills/tencentcloud-manager/config/.env

vim skills/tencentcloud-manager/config/.env
```

```bash
TENCENT_SECRET_ID=AKIDxxxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_REGION=ap-singapore
RESOURCE_PREFIX=resource
BUDGET_ALERT=100
```

### 步骤 4: 安装依赖

```bash
pip3 install --break-system-packages \
  tencentcloud-sdk-python \
  cos-python-sdk-v5 \
  python-dotenv
```

---

## 🚀 快速开始

### 方式 1: 使用统一入口

```python
from tencentcloud_manager import TencentCloudManager

tcm = TencentCloudManager()

# 查看所有可用服务
tcm.show_services()

# 查询促销方案
tcm.show_promotions(service='lighthouse')

# 创建资源
instance = tcm.create_resource(
    service='lighthouse',
    plan_id='new-2c4g',
    instance_name='my-server'
)
```

### 方式 2: 直接使用各服务管理器

```python
from tencentcloud_cvm import CVMManager
cvm = CVMManager()
cvm.show_promotions()

from tencentcloud_lighthouse import LighthouseManager
lh = LighthouseManager()
lh.show_blueprints()

from tencentcloud_cos import COSManager
cos = COSManager()
cos.create_bucket(bucket_name='my-bucket')
```

---

## 📚 Cookbook - 常用场景

### 场景 1: 创建个人博客服务器

```python
from tencentcloud_manager import TencentCloudManager

tcm = TencentCloudManager()

# 查看促销方案
tcm.show_promotions(service='lighthouse')

# 创建轻量服务器（使用 WordPress 镜像）
instance = tcm.create_resource(
    service='lighthouse',
    plan_id='new-1c1g',
    blueprint_id='bp-wordpress',
    instance_name='my-blog',
    period=12
)

print(f"服务器已创建：{instance['PublicAddress']}")
```

**预估成本**: ~¥60-80/年（新人特惠）

---

### 场景 2: 创建数据采集服务器

```python
tcm = TencentCloudManager()

# 创建 CVM 实例（按量付费）
instance = tcm.create_resource(
    service='cvm',
    plan_id='payg-2c4g',
    image_id='img-ubuntu-2204',
    instance_name='data-collector',
    system_disk_size=100,
    bandwidth=5
)

# 设置定时关机
tcm.schedule_shutdown(
    service='cvm',
    instance_id=instance['InstanceId'],
    shutdown_time='23:00',
    timezone='Asia/Shanghai'
)
```

**预估成本**: ~¥130-180/月（按实际使用计费）

---

### 场景 3: 配置对象存储并设置生命周期

```python
# 创建存储桶
bucket = tcm.create_cos_bucket(
    bucket_name='my-data-bucket',
    region='ap-singapore',
    storage_class='STANDARD'
)

# 上传文件
tcm.upload_to_cos(
    bucket=bucket['bucket'],
    local_path='/tmp/data.parquet',
    key='data/2024/03/29/data.parquet'
)

# 设置生命周期
tcm.set_cos_lifecycle(
    bucket=bucket['bucket'],
    rules=[
        {
            'id': 'data-lifecycle',
            'prefix': 'data/',
            'transitions': [
                {'days': 7, 'storage_class': 'STANDARD_IA'},
                {'days': 30, 'storage_class': 'ARCHIVE'}
            ]
        }
    ]
)
```

**预估成本**: ~¥35-50/月（生命周期优化后）

---

### 场景 4: 批量管理服务器

```python
# 查询所有实例
instances = tcm.list_all_instances()

# 批量开机
for inst in instances:
    if inst['state'] == 'STOPPED':
        tcm.start_resource(inst['service'], inst['id'])

# 批量关机
for inst in instances:
    if inst['state'] == 'RUNNING':
        tcm.stop_resource(inst['service'], inst['id'])
```

---

### 场景 5: 监控资源成本

```python
# 查询所有资源成本
cost_report = tcm.get_cost_report()

print(f"总月成本：¥{cost_report['total_monthly_cost']}")

# 成本优化建议
suggestions = tcm.get_cost_optimization_suggestions()
for suggestion in suggestions:
    print(f"💡 {suggestion}")
```

---

## 🔒 安全最佳实践

### 1. 使用子用户凭证

❌ **不要**使用主账号密钥：
```python
SECRET_ID = "AKID 主账号密钥"  # 危险！
```

✅ **使用子用户密钥**：
```python
from dotenv import load_dotenv
load_dotenv('config/.env')
SECRET_ID = os.getenv('TENCENT_SECRET_ID')
```

### 2. 最小权限原则

只授予必要的权限：
- 开发环境：只读权限 + 创建权限
- 生产环境：只读权限 + 启停权限
- 避免：财务权限、用户管理权限

### 3. 定期轮换密钥

每 90 天轮换一次密钥。

### 4. 启用操作审计

```python
tcm = TencentCloudManager(enable_audit=True)
```

---

## 📈 运维管理

### 日常巡检

```python
# 检查所有实例状态
instances = tcm.list_all_instances()
for inst in instances:
    status = tcm.get_resource_status(inst['service'], inst['id'])
    if status['state'] != 'RUNNING':
        print(f"⚠️  实例异常：{inst['name']}")

# 检查即将到期的资源
expiring = tcm.get_expiring_resources(days=30)
for resource in expiring:
    print(f"⏰ 即将到期：{resource['name']}")
```

---

## 📚 相关文档

- [CVM API 文档](https://cloud.tencent.com/document/api/213)
- [Lighthouse API 文档](https://cloud.tencent.com/document/api/1170)
- [COS API 文档](https://cloud.tencent.com/document/api/436)
- [子用户权限配置](https://cloud.tencent.com/document/product/598/10603)

---

## 🆘 故障排除

### 问题 1: 凭证验证失败

```bash
cat config/.env
python3 src/verify_config.py
```

### 问题 2: 权限不足

```bash
tccli cam ListAttachedUserPolicies --AttachUin <UIN>
```

### 问题 3: 创建失败

```bash
tccli cvm DescribeAccountQuota
```
