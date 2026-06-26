# TencentCloud-CVM - 腾讯云服务器管理技能

## 📋 技能说明

**腾讯云 CVM 云服务器管理工具**，用于创建和管理云服务器实例。

### 入口组件

如需统一管理所有腾讯云服务（CVM + Lighthouse + COS），请使用 **[tencentcloud-manager](../tencentcloud-manager/SKILL.md)** 作为入口组件。

### 相关技能

| 技能 | 说明 |
|------|------|
| [tencentcloud-manager](../tencentcloud-manager/SKILL.md) | 腾讯云统一入口组件 |
| [tencentcloud-ops](../tencentcloud-ops/SKILL.md) | CVM + COS 运维工具包 |
| [tencentcloud-lighthouse](../tencentcloud-lighthouse/SKILL.md) | Lighthouse 轻量服务器管理 |
| [tencentcloud-cos](../tencentcloud-cos/SKILL.md) | COS 对象存储管理 |

### 核心功能

✅ **CVM 服务器管理**
- 创建/删除云服务器
- 按量/包年包月付费
- 开机/关机/重启
- 实例状态查询
- 配置变更

✅ **促销方案查询**
- 实时查询最新促销
- 新人特惠/限时秒杀/按量付费/竞价实例
- 方案对比与推荐

✅ **成本控制**
- 预算告警设置
- 自动关机
- 资源使用监控
- 成本优化建议

✅ **安全管理**
- 安全组配置
- 密钥管理
- 权限控制

---

## 💰 促销方案参考

> ⚠️ **注意**: 以下价格为参考区间（更新于 2026-03-29），实际价格以腾讯云官网实时查询为准。促销活动可能随时调整。

### 方案类型概览

| 方案类型 | 价格区间 (2 核 4G) | 特点 | 适用场景 |
|----------|-------------------|------|---------|
| 新人特惠 | ~¥150-200/年 | 限新用户，限 1 台 | 长期运行 |
| 限时秒杀 | ~¥150-180/年 | 每日限量抢购 | 长期运行 |
| 按量付费 | ~¥100-150/月 | 灵活，随时释放 | 短期测试 |
| 竞价实例 | ~¥30-50/月 | 最高 90% OFF，可能中断 | 容错任务 |

### 获取最新促销

```python
from tencentcloud_cvm import CVMPromotions

promo = CVMPromotions()

# 查询所有促销方案
plans = promo.list_promotions()

for plan in plans:
    print(f"{plan['name']}: {plan['cpu']}vCPU/{plan['memory']}GB - ¥{plan['price']}")
```

---

## 📊 推荐配置清单

### 场景 1: 数据采集服务器

```yaml
配置：2 vCPU / 4 GB / 20 GB SSD / 10 Mbps
付费方式：按量付费
预估成本：~¥150/月

优势：
  ✅ 灵活，可随时停止
  ✅ 成本可控
  ✅ 适合短期任务
```

### 场景 2: 长期运行 (包年包月)

```yaml
配置：2 vCPU / 4 GB / 50 GB SSD / 5 Mbps
付费方式：包年包月 (新人特惠)
预估成本：~¥180/年

优势：
  ✅ 价格最低
  ✅ 资源稳定
  ✅ 无需担心关机
```

### 场景 3: 批量数据处理 (竞价实例)

```yaml
配置：4 vCPU / 8 GB / 100 GB SSD
付费方式：竞价实例
预估成本：~¥60-80/月

优势：
  ✅ 成本最低
  ✅ 性能强劲
  ✅ 适合容错任务
```

---

## ⚠️ 前置配置 (必须完成)

### 步骤 1: 安装腾讯云 CLI

```bash
# macOS
brew install tccli

# 或
pip install tccli

# 验证安装
tccli --version
```

---

### 步骤 2: 获取 API 凭证

1. 访问：https://console.cloud.tencent.com/cam/capi
2. 登录腾讯云账号
3. 创建/查看 API 密钥

---

### 步骤 3: 创建子用户 (推荐)

**为了安全，不要使用主账号直接操作！**

```bash
# 创建子用户
tccli cam CreateUser \
  --Name "cvm-admin" \
  --Remark "CVM 服务器管理员" \
  --UseApi 1 \
  --UseConsole 0
```

---

### 步骤 4: 创建 CVM 管理策略

```bash
# 创建策略文件
cat > /tmp/cvm-policy.json << 'EOF'
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "cvm:*",
        "vpc:*",
        "cbs:*"
      ],
      "resource": "*"
    }
  ]
}
EOF

# 创建策略
tccli cam CreatePolicy \
  --PolicyName "CVM-Manager" \
  --PolicyDocument "$(cat /tmp/cvm-policy.json)" \
  --Description "CVM 服务器管理权限"
```

---

### 步骤 5: 授予子用户权限

```bash
# 获取策略 ID
tccli cam ListPolicies | grep "CVM-Manager"

# 关联策略到子用户
tccli cam AttachUserPolicy \
  --AttachUin <UIN> \
  --PolicyId <POLICY_ID>
```

---

### 步骤 6: 为子用户创建 API 密钥

```bash
# 创建子用户 API 密钥
tccli cam CreateAccessKey \
  --TargetUin <UIN>
```

**⚠️ 重要**: 立即保存 SecretId 和 SecretKey，只显示一次！

---

### 步骤 7: 配置环境变量

```bash
# 复制示例文件
cd skills/tencentcloud-cvm
cp config/.env.example config/.env

# 编辑 .env 文件
vim config/.env
```

```bash
# .env 文件
TENCENT_SECRET_ID=AKIDxxxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_REGION=ap-seoul
TENCENT_ZONE=ap-seoul-1
```

---

### 步骤 8: 验证配置

```bash
# 测试 API 连接
cd skills/tencentcloud-cvm/src
python3 verify_config.py
```

---

## 🔒 权限说明

### 授予的权限

| 权限 | 范围 | 说明 |
|------|------|------|
| `cvm:*` | 云服务器 | 创建/删除/管理 CVM |
| `vpc:*` | 私有网络 | 安全组/网络配置 |
| `cbs:*` | 云硬盘 | 磁盘管理 |

### 未授予的权限 (安全)

| 权限 | 原因 |
|------|------|
| `finance:*` | ❌ 财务权限 |
| `cam:*` | ❌ 用户管理 |
| `billing:*` | ❌ 账单管理 |

---

## 📦 安装

```bash
# 安装依赖
pip3 install --break-system-packages \
  tencentcloud-sdk-python \
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
RESOURCE_PREFIX=cvm

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

### 查看促销方案

```python
from tencentcloud_cvm import CVMPromotions

promo = CVMPromotions()

# 查看所有促销方案
plans = promo.list_promotions()

for plan in plans:
    print(f"{plan['name']}: {plan['price']}/年")
    print(f"  配置：{plan['cpu']} vCPU / {plan['memory']} GB")
    print(f"  折扣：{plan['discount']}")
```

### 创建 CVM 服务器

```python
from tencentcloud_cvm import CVMManager

cvm = CVMManager()

# 列出可用方案
plans = cvm.list_available_plans()
print("可用方案:")
for i, plan in enumerate(plans, 1):
    print(f"{i}. {plan['name']} - {plan['price']}/月")

# 创建服务器
instance = cvm.create_instance(
    plan_id=selected,
    instance_name="data-collector",
    charge_type="POSTPAID"  # 按量付费
)

print(f"✅ 创建成功：{instance['InstanceId']}")
```

### 查询实例

```python
from tencentcloud_cvm import CVMManager

cvm = CVMManager()

# 查询所有 CVM
instances = cvm.describe_instances()
for inst in instances:
    print(f"{inst['InstanceId']}: {inst['InstanceName']} - {inst['State']}")
    print(f"  配置：{inst['Cpu']} vCPU / {inst['Memory']} GB")
    print(f"  公网 IP: {inst['PublicIpAddresses']}")
```

### 开机/关机

```python
from tencentcloud_cvm import CVMManager

cvm = CVMManager()

# 关机
cvm.stop_instance("ins-xxxxxx")

# 开机
cvm.start_instance("ins-xxxxxx")

# 重启
cvm.restart_instance("ins-xxxxxx")
```

### 自动关机

```python
from tencentcloud_cvm import CVMManager

cvm = CVMManager()

# 设置定时关机
cvm.schedule_shutdown(
    instance_id="ins-xxxxxx",
    days=30
)
```

---

## 📊 成本估算参考

> 以下成本仅供参考，实际费用以账单为准。

| 配置 | 按量付费 (月) | 包年包月 (年) | 竞价实例 (月) |
|------|--------------|--------------|--------------|
| 2 核 2G | ~¥80-100 | ~¥80-120 | ~¥20-30 |
| 2 核 4G | ~¥120-150 | ~¥150-200 | ~¥30-50 |
| 4 核 8G | ~¥250-300 | ~¥350-450 | ~¥60-80 |

---

## ⚠️ 注意事项

### 安全

- ✅ 使用子用户密钥，不用主账号
- ✅ 设置最小权限 (CVM only)
- ✅ .env 文件妥善保管
- ✅ 定期轮换密钥 (90 天)
- ❌ 不要提交密钥到 Git
- ❌ 不要授予财务权限

### 成本

- ✅ 设置预算告警
- ✅ 使用按量付费 (测试)
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

- [腾讯云 API 文档](https://cloud.tencent.com/document/api/213)
- [CVM 产品文档](https://cloud.tencent.com/document/product/213)
- [促销活动中心](https://cloud.tencent.com/act)
- [CAM 用户管理](https://cloud.tencent.com/document/product/598)
- [API 3.0 Explorer](https://console.cloud.tencent.com/api/explorer)

---

## 🆘 故障排除

### 问题 1: 凭证验证失败

```bash
# 检查 .env 文件
cat config/.env

# 验证密钥
python3 src/verify_config.py

# 重新配置
tccli configure
```

### 问题 2: 权限不足

```bash
# 检查子用户权限
tccli cam ListAttachedUserPolicies --AttachUin <UIN>

# 重新关联策略
tccli cam AttachUserPolicy --AttachUin <UIN> --PolicyId <POLICY_ID>
```

### 问题 3: 创建失败

```bash
# 查看错误日志
tail -f logs/cvm_ops.log

# 检查配额
tccli cvm DescribeAccountQuota
```
