# TencentCloud-COS - 腾讯云对象存储管理技能

## 📋 技能说明

**腾讯云 COS 对象存储管理工具**，用于创建和管理存储桶、上传下载文件。

### 入口组件

如需统一管理所有腾讯云服务（CVM + Lighthouse + COS），请使用 **[tencentcloud-manager](../tencentcloud-manager/SKILL.md)** 作为入口组件。

### 相关技能

| 技能 | 说明 |
|------|------|
| [tencentcloud-manager](../tencentcloud-manager/SKILL.md) | 腾讯云统一入口组件 |
| [tencentcloud-ops](../tencentcloud-ops/SKILL.md) | CVM + COS 运维工具包 |
| [tencentcloud-cvm](../tencentcloud-cvm/SKILL.md) | CVM 云服务器管理 |
| [tencentcloud-lighthouse](../tencentcloud-lighthouse/SKILL.md) | Lighthouse 轻量服务器管理 |

### 核心功能

✅ **COS 存储桶管理**
- 创建/删除存储桶
- 存储类型管理 (标准/低频/归档)
- 生命周期配置
- 跨地域复制

✅ **文件管理**
- 上传/下载文件
- 批量上传
- 分片上传
- 文件列表查询

✅ **成本控制**
- 存储类型优化
- 生命周期自动转换
- 流量监控

✅ **安全管理**
- 访问权限控制
- 防盗链
- 加密存储

---

## 💰 存储类型价格参考

> ⚠️ **注意**: 以下价格为参考区间（更新于 2026-03-29），实际价格以腾讯云官网为准。

### 存储类型概览

| 存储类型 | 价格区间 | 适用场景 | 节省 |
|----------|---------|---------|------|
| 标准存储 | ~¥0.12-0.15/GB/月 | 频繁访问数据 | - |
| 低频存储 | ~¥0.07-0.09/GB/月 | 不常访问数据 | ~35-40% |
| 归档存储 | ~¥0.02-0.04/GB/月 | 长期保存数据 | ~70-80% |

### 获取最新价格

```python
from tencentcloud_cos import COSCostManager

cost_mgr = COSCostManager()

# 估算成本
cost = cost_mgr.estimate_cost(
    storage_gb=100,
    storage_class='STANDARD',
    months=12
)

print(f"总成本：¥{cost['total']}")
```

---

## 📊 推荐配置清单

### 场景 1: 数据采集存储

```yaml
存储策略:
  - 最近 7 天：标准存储 (频繁查询)
  - 7-30 天：低频存储 (偶尔查询)
  - 30 天+：归档存储 (长期保存)

数据量：450 GB/月
预估成本：~¥40-60/月

优势:
  ✅ 成本优化
  ✅ 热数据快速访问
  ✅ 冷数据便宜存储
```

### 场景 2: 网站静态资源

```yaml
存储类型：标准存储
数据量：100 GB
预估成本：~¥15-20/月 (存储) + 流量费

优势:
  ✅ 快速访问
  ✅ CDN 加速
  ✅ 高可用
```

### 场景 3: 备份归档

```yaml
存储策略:
  - 最近 30 天：低频存储
  - 30 天+：归档存储

数据量：1 TB
预估成本：~¥30-40/月 (30 天后)

优势:
  ✅ 成本极低
  ✅ 长期保存
  ✅ 合规备份
```

---

## ⚠️ 前置配置 (必须完成)

### 步骤 1: 安装 COS SDK

```bash
pip3 install --break-system-packages cos-python-sdk-v5
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
        "name/cos:*"
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
| `name/cos:*` | 对象存储 | 存储桶/对象管理 |

### 未授予的权限 (安全)

| 权限 | 原因 |
|------|------|
| `finance:*` | ❌ 财务权限 |
| `cam:*` | ❌ 用户管理 |

---

## 📦 安装

```bash
# 安装依赖
pip3 install --break-system-packages \
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
TENCENT_REGION=ap-singapore

# 资源命名
RESOURCE_PREFIX=cos

# 存储配置
DEFAULT_STORAGE_CLASS=STANDARD
```

---

## 🚀 使用示例

### 创建存储桶

```python
from tencentcloud_cos import COSManager

cos = COSManager()

bucket = cos.create_bucket(
    bucket_name="my-data-bucket",
    region="ap-singapore",
    storage_class="STANDARD"
)

print(f"✅ 创建成功：{bucket['bucket_name']}")
```

### 上传文件

```python
cos.upload_file(
    bucket="my-data-bucket",
    local_path="/tmp/data.parquet",
    key="data/2024/03/28/data.parquet"
)
```

### 批量上传

```python
files = ["/tmp/data1.parquet", "/tmp/data2.parquet"]

cos.batch_upload(
    bucket="my-data-bucket",
    files=files,
    prefix="data/2024/03/28/"
)
```

### 下载文件

```python
cos.download_file(
    bucket="my-data-bucket",
    key="data/2024/03/28/data.parquet",
    local_path="/tmp/download.parquet"
)
```

### 设置生命周期

```python
cos.put_lifecycle(
    bucket="my-data-bucket",
    rules=[
        {
            "id": "rule1",
            "prefix": "data/",
            "transitions": [
                {"days": 7, "storage_class": "STANDARD_IA"},
                {"days": 30, "storage_class": "ARCHIVE"}
            ]
        }
    ]
)
```

---

## 📊 成本估算参考

> 以下成本仅供参考，实际费用以账单为准。

### 数据存储 (100 GB/月)

| 存储类型 | 月成本 | 年成本 |
|----------|--------|--------|
| 标准存储 | ~¥12-15 | ~¥144-180 |
| 低频存储 | ~¥7-9 | ~¥84-108 |
| 归档存储 | ~¥2-4 | ~¥24-48 |

### 生命周期优化示例

| 策略 | 月成本 | 节省 |
|------|--------|------|
| 全标准存储 | ~¥55-65 | - |
| 生命周期优化 | ~¥35-45 | ~30-40% |

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
- ✅ 使用生命周期优化
- ✅ 及时清理无用文件
- ❌ 不要忘记设置生命周期

### 区域选择

- ✅ 新加坡 (ap-singapore): 网络稳定
- ✅ 香港 (ap-hongkong): 延迟低
- ✅ 上海 (ap-shanghai): 国内访问快

---

## 📚 相关文档

- [COS API 文档](https://cloud.tencent.com/document/api/436)
- [存储类型说明](https://cloud.tencent.com/document/product/436/33417)
- [生命周期管理](https://cloud.tencent.com/document/product/436/30688)

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

### 问题 3: 上传失败

```bash
# 检查存储桶名称格式
# 正确格式：bucket-name.cos.region.myqcloud.com

# 检查网络连接
ping cos.ap-singapore.myqcloud.com
```
