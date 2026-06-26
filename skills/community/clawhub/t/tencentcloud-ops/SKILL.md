# TencentCloud-OPS - 腾讯云运维技能

## 📋 技能说明

**腾讯云 CVM/COS 资源管理工具**，用于创建和管理云服务器 (CVM)、对象存储 (COS) 等资源。

### 入口组件

本技能提供 CVM + COS 运维功能。如需统一管理所有腾讯云服务（CVM + Lighthouse + COS），请使用 **[tencentcloud-manager](../tencentcloud-manager/SKILL.md)** 作为入口组件。

### 相关技能

| 技能 | 说明 |
|------|------|
| [tencentcloud-manager](../tencentcloud-manager/SKILL.md) | 腾讯云统一入口组件 |
| [tencentcloud-cvm](../tencentcloud-cvm/SKILL.md) | CVM 云服务器管理（含促销方案） |
| [tencentcloud-lighthouse](../tencentcloud-lighthouse/SKILL.md) | Lighthouse 轻量服务器管理 |
| [tencentcloud-cos](../tencentcloud-cos/SKILL.md) | COS 对象存储管理 |

### 核心功能

✅ **CVM 服务器管理**
- 创建/删除云服务器
- 按量付费控制
- 自动关机/开机
- 实例状态查询

✅ **COS 存储管理**
- 创建/删除存储桶
- 文件上传/下载
- 存储类型管理
- 生命周期配置

✅ **成本控制**
- 预算告警设置
- 资源使用监控
- 自动释放闲置资源

✅ **安全管理**
- 安全组配置
- 密钥管理
- 权限控制

---

## 💰 价格参考

> ⚠️ **注意**: 以下价格为参考区间（更新于 2026-03-29），实际价格以腾讯云官网实时查询为准。

### CVM 云服务器

| 方案类型 | 2 核 4G 参考 | 特点 |
|----------|-------------|------|
| 按量付费 | ~¥120-150/月 | 灵活，随时释放 |
| 竞价实例 | ~¥30-50/月 | 最高 90% OFF |

### COS 对象存储

| 存储类型 | 参考价格 | 适用 |
|----------|---------|------|
| 标准存储 | ~¥0.12-0.15/GB/月 | 频繁访问 |
| 低频存储 | ~¥0.07-0.09/GB/月 | 不常访问 |
| 归档存储 | ~¥0.02-0.04/GB/月 | 长期保存 |

---

## ⚠️ 前置配置 (必须完成)

### 步骤 1: 安装腾讯云 CLI

```bash
brew install tccli
```

### 步骤 2: 获取 API 凭证

1. 访问：https://console.cloud.tencent.com/cam/capi
2. 登录腾讯云账号
3. 创建/查看 API 密钥

### 步骤 3: 创建子用户 (推荐)

```bash
tccli cam CreateUser \
  --Name "resource-admin" \
  --Remark "资源管理员" \
  --UseApi 1 \
  --UseConsole 0
```

### 步骤 4: 创建自定义策略

**CVM 管理策略**:

```bash
cat > /tmp/cvm-policy.json << 'EOF'
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": ["cvm:*", "vpc:*", "cbs:*"],
      "resource": "*"
    }
  ]
}
EOF

tccli cam CreatePolicy \
  --PolicyName "CVM-Manager" \
  --PolicyDocument "$(cat /tmp/cvm-policy.json)" \
  --Description "CVM 服务器管理权限"
```

**COS 管理策略**:

```bash
cat > /tmp/cos-policy.json << 'EOF'
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": ["name/cos:*"],
      "resource": "*"
    }
  ]
}
EOF

tccli cam CreatePolicy \
  --PolicyName "COS-Manager" \
  --PolicyDocument "$(cat /tmp/cos-policy.json)" \
  --Description "COS 管理权限"
```

### 步骤 5: 授予子用户权限

```bash
tccli cam ListPolicies
tccli cam AttachUserPolicy --AttachUin <UIN> --PolicyId <POLICY_ID>
```

### 步骤 6: 为子用户创建 API 密钥

```bash
tccli cam CreateAccessKey --TargetUin <UIN>
```

**⚠️ 重要**: 立即保存 SecretId 和 SecretKey，只显示一次！

### 步骤 7: 配置环境变量

```bash
cd skills/tencentcloud-ops
cp config/.env.example config/.env
vim config/.env
```

```bash
TENCENT_SECRET_ID=AKIDxxxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_REGION=ap-seoul
```

### 步骤 8: 验证配置

```bash
python3 src/verify_config.py
```

---

## 🔒 权限说明

### 授予的权限

| 权限 | 范围 | 说明 |
|------|------|------|
| `cvm:*` | 云服务器 | 创建/删除/管理 CVM |
| `vpc:*` | 私有网络 | 安全组/网络配置 |
| `cbs:*` | 云硬盘 | 磁盘管理 |
| `name/cos:*` | 对象存储 | 存储桶管理 |

### 未授予的权限 (安全)

| 权限 | 原因 |
|------|------|
| `finance:*` | ❌ 财务权限 |
| `cam:*` | ❌ 用户管理 |
| `billing:*` | ❌ 账单管理 |

---

## 📦 安装

```bash
pip3 install --break-system-packages \
  tencentcloud-sdk-python \
  cos-python-sdk-v5 \
  python-dotenv
```

---

## 🔧 配置

### 环境变量文件 (.env)

```bash
# 腾讯云 API 凭证 (子用户)
TENCENT_SECRET_ID=AKIDxxxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxx

# 区域配置
TENCENT_REGION=ap-seoul
TENCENT_ZONE=ap-seoul-1

# 资源命名
RESOURCE_PREFIX=resource

# 成本控制 (可选)
BUDGET_ALERT=100
AUTO_SHUTDOWN_DAYS=30
```

### 安全建议

```bash
# ✅ 做好:
- 使用子用户密钥 (非主账号)
- .env 文件加入 .gitignore
- 定期轮换密钥 (90 天)
- 设置最小权限

# ❌ 避免:
- 提交 .env 到 Git
- 使用主账号密钥
- 密钥长期不更换
- 授予过多权限
```

---

## 🚀 使用示例

### 创建 CVM 服务器

```python
from tencentcloud_ops import CVMManager

cvm = CVMManager()

instance = cvm.create_instance(
    instance_type="S2.MEDIUM2",
    image_id="img-ubuntu-2204",
    system_disk_size=20,
    bandwidth=10,
    instance_name="data-collector",
    charge_type="POSTPAID"
)

print(f"✅ 创建成功：{instance['InstanceId']}")
```

### 创建 COS 存储桶

```python
from tencentcloud_ops import COSManager

cos = COSManager()

bucket = cos.create_bucket(
    bucket_name="my-data-bucket",
    region="ap-seoul",
    storage_class="STANDARD"
)

print(f"✅ 创建成功：{bucket['bucket_name']}")
```

### 上传文件到 COS

```python
cos.upload_file(
    bucket="my-data-bucket",
    local_path="/tmp/data.parquet",
    key="data/2024/03/28/data.parquet"
)
```

### 查询资源

```python
# 查询所有 CVM
instances = cvm.describe_instances()
for inst in instances:
    print(f"{inst['InstanceId']}: {inst['InstanceName']} - {inst['State']}")

# 查询所有 COS 存储桶
buckets = cos.list_buckets()
for bucket in buckets:
    print(f"{bucket['Name']} - {bucket['Region']}")
```

### 自动关机

```python
cvm.schedule_shutdown(
    instance_id="ins-xxxxxx",
    days=30
)
```

---

## 📊 成本估算参考

> 以下成本仅供参考，实际费用以账单为准。

### 30 天按量付费

| 资源 | 配置 | 成本参考 |
|------|------|---------|
| CVM | 2 vCPU / 4 GB | ~¥120-150 |
| 系统盘 | 20 GB SSD | ~¥25-30 |
| 带宽 | 10 Mbps | ~¥20-30 |
| COS | 450 GB 标准存储 | ~¥55-70 |
| **总计** | - | **~¥220-280** |

### 30 天后 (仅存储)

| 资源 | 月成本参考 |
|------|-----------|
| COS 存储 (450 GB) | ~¥55-70/月 |

---

## ⚠️ 注意事项

### 安全

- ✅ 使用子用户密钥，不用主账号
- ✅ 设置最小权限 (CVM+COS only)
- ✅ .env 文件妥善保管
- ✅ 定期轮换密钥 (90 天)
- ❌ 不要提交密钥到 Git
- ❌ 不要授予财务权限

### 成本

- ✅ 设置预算告警
- ✅ 使用按量付费
- ✅ 配置自动关机
- ✅ 及时释放闲置资源
- ❌ 不要忘记关机
- ❌ 不要长期闲置

### 区域选择

- ✅ 首尔 (ap-seoul): 延迟低
- ✅ 新加坡 (ap-singapore): 网络稳定
- ⚠️ 香港 (ap-hongkong): 可能有访问限制
- ❌ 避免选择过远区域

---

## 📚 相关文档

- [腾讯云 API 文档](https://cloud.tencent.com/document/api)
- [CVM API](https://cloud.tencent.com/document/api/213)
- [COS API](https://cloud.tencent.com/document/api/436)
- [CAM 用户管理](https://cloud.tencent.com/document/product/598)
- [API 3.0 Explorer](https://console.cloud.tencent.com/api/explorer)

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
tail -f logs/tencent_ops.log
tccli cvm DescribeAccountQuota
```
