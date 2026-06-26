# TencentCloud-Lighthouse - 腾讯云轻量应用服务器管理技能

## 📋 技能说明

**腾讯云轻量应用服务器 (Lighthouse) 管理工具**，用于创建和管理轻量应用服务器。

### 入口组件

如需统一管理所有腾讯云服务（CVM + Lighthouse + COS），请使用 **[tencentcloud-manager](../tencentcloud-manager/SKILL.md)** 作为入口组件。

### 相关技能

| 技能 | 说明 |
|------|------|
| [tencentcloud-manager](../tencentcloud-manager/SKILL.md) | 腾讯云统一入口组件 |
| [tencentcloud-ops](../tencentcloud-ops/SKILL.md) | CVM + COS 运维工具包 |
| [tencentcloud-cvm](../tencentcloud-cvm/SKILL.md) | CVM 云服务器管理 |
| [tencentcloud-cos](../tencentcloud-cos/SKILL.md) | COS 对象存储管理 |

### 核心功能

✅ **轻量应用服务器管理**
- 创建/删除轻量服务器
- 包年包月付费
- 开机/关机/重启
- 实例状态查询
- 应用镜像选择

✅ **促销方案查询**
- 实时查询最新促销
- 新人特惠/限时秒杀/包年包月
- 方案对比与推荐

✅ **应用镜像**
- 系统镜像 (Ubuntu/CentOS/Debian)
- 应用镜像 (WordPress/Docker/LNMP)
- 自定义镜像

✅ **成本控制**
- 预算告警
- 续费管理

---

## 💰 促销方案参考

> ⚠️ **注意**: 以下价格为参考区间（更新于 2026-03-29），实际价格以腾讯云官网实时查询为准。

### 方案类型概览

| 方案类型 | 价格区间 (2 核 2G) | 特点 | 适用场景 |
|----------|-------------------|------|---------|
| 新人特惠 | ~¥80-120/年 | 限新用户，限 1 台 | 长期运行 |
| 限时秒杀 | ~¥70-100/年 | 每日限量抢购 | 长期运行 |
| 包年包月 | ~¥400-500/年 | 价格稳定 | 企业用户 |

### 获取最新促销

```python
from tencentcloud_lighthouse import LighthousePromotions

promo = LighthousePromotions()
promo.print_promotions()
```

---

## 📊 推荐配置清单

### 场景 1: 数据采集脚本

```yaml
配置：2 核 2G / 50G 盘 / 30M 带宽
付费方式：包年包月 (新人特惠)
预估成本：~¥100/年

优势:
  ✅ 带宽高 (30M)，数据下载快
  ✅ 价格便宜
  ✅ 适合长期运行
```

### 场景 2: WordPress 博客

```yaml
配置：1 核 1G / 30G 盘 / 30M 带宽
应用镜像：WordPress
付费方式：包年包月 (新人特惠)
预估成本：~¥60/年

优势:
  ✅ 一键安装 WordPress
  ✅ 带宽高，访问快
  ✅ 成本极低
```

### 场景 3: Docker 容器环境

```yaml
配置：2 核 4G / 60G 盘 / 30M 带宽
应用镜像：Docker
付费方式：包年包月 (新人特惠)
预估成本：~¥150-200/年

优势:
  ✅ 内存充足
  ✅ 预装 Docker
  ✅ 适合容器化应用
```

---

## ⚠️ 前置配置 (必须完成)

### 步骤 1: 安装腾讯云 CLI

```bash
brew install tccli
```

### 步骤 2-7: 配置子用户权限

参考 tencentcloud-cvm 技能的配置步骤。

**权限策略**:
```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "lighthouse:*",
        "vpc:*"
      ],
      "resource": "*"
    }
  ]
}
```

---

## 🔒 权限说明

### 授予的权限

| 权限 | 范围 | 说明 |
|------|------|------|
| `lighthouse:*` | 轻量应用服务器 | 创建/删除/管理 |
| `vpc:*` | 私有网络 | 安全组/网络 |

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
TENCENT_REGION=ap-singapore

# 资源命名
RESOURCE_PREFIX=lighthouse

# 成本控制
BUDGET_ALERT=100
```

---

## 🚀 使用示例

### 查看促销方案

```python
from tencentcloud_lighthouse import LighthousePromotions

promo = LighthousePromotions()
promo.print_promotions()
```

### 创建轻量服务器

```python
from tencentcloud_lighthouse import LighthouseManager

lh = LighthouseManager()

# 显示促销方案
lh.show_promotions()

# 创建服务器
instance = lh.create_instance(
    plan_id="new-2c2g",
    blueprint_id="bp-ubuntu-2204",
    instance_name="my-server"
)

print(f"✅ 创建成功：{instance['InstanceId']}")
```

### 选择应用镜像

```python
from tencentcloud_lighthouse import LighthouseManager

lh = LighthouseManager()

# 列出可用镜像
blueprints = lh.list_blueprints()

print("可用镜像:")
for bp in blueprints:
    print(f"  {bp['id']}: {bp['name']} ({bp['type']})")
```

### 查询实例

```python
from tencentcloud_lighthouse import LighthouseManager

lh = LighthouseManager()

instances = lh.describe_instances()
for inst in instances:
    print(f"{inst['InstanceId']}: {inst['InstanceName']}")
    print(f"  配置：{inst['CPU']} vCPU / {inst['Memory']} GB")
    print(f"  带宽：{inst['Bandwidth']} Mbps")
    print(f"  状态：{inst['State']}")
```

---

## 📊 成本估算参考

> 以下成本仅供参考，实际费用以账单为准。

| 配置 | 新人特惠 (年) | 常规包年 (年) |
|------|--------------|--------------|
| 1 核 1G | ~¥50-80 | ~¥200-300 |
| 2 核 2G | ~¥80-120 | ~¥400-500 |
| 2 核 4G | ~¥150-200 | ~¥600-800 |
| 4 核 8G | ~¥300-400 | ~¥1200-1500 |

---

## ⚠️ 注意事项

### 安全

- ✅ 使用子用户密钥，不用主账号
- ✅ 设置最小权限
- ✅ .env 文件妥善保管
- ✅ 定期轮换密钥 (90 天)
- ❌ 不要提交密钥到 Git

### 成本

- ✅ 设置预算告警
- ✅ 新人特惠最划算
- ✅ 及时释放闲置资源
- ❌ 不要忘记续费

### 区域选择

- ✅ 新加坡 (ap-singapore): Lighthouse 优势区域
- ✅ 首尔 (ap-seoul): 延迟低
- ⚠️ 香港 (ap-hongkong): 可能有访问限制

---

## 📚 相关文档

- [轻量应用服务器 API](https://cloud.tencent.com/document/api/1170)
- [促销活动中心](https://cloud.tencent.com/act)
- [应用镜像文档](https://cloud.tencent.com/document/product/1170/38176)

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
tccli lighthouse DescribeInstances
```
