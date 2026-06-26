---
name: xianyu-api-client
description: Secure Xianyu Guanjia API client with endpoint allowlisting, enforced confirmation for high-risk actions, dry-run mode, and unsafe methods for automation.
version: 1.0.5
author: AI造物的大铁锤
metadata:
  openclaw:
    requires:
      env:
        - XIAN_YU_APP_KEY
        - XIAN_YU_APP_SECRET
      bins:
        - python
    primaryEnv: XIAN_YU_APP_KEY
    homepage: https://www.goofish.pro
    source: https://clawhub.com/skills/xianyu-api-client
---

# 闲鱼API客户端技能

## 技能概述

这是一个专为闲鱼管家开放平台设计的基础API客户端技能，为所有闲鱼相关操作提供安全、可靠的底层通信能力。本技能处理了所有复杂的认证、签名、错误处理等技术细节，让您能够专注于业务逻辑开发，而无需关心底层API实现。

## 核心价值

- **安全可靠**：严格按照闲鱼管家官方签名算法实现，端点白名单防止未授权调用
- **安全确认**：高风险操作（创建/删除商品、改价）自动暂停并等待用户确认
- **开箱即用**：预置所有常用API端点，支持商品管理、订单处理、用户查询等完整功能
- **智能容错**：内置完善的错误处理机制，自动识别并处理各种异常情况
- **Dry Run支持**：支持预览模式，先检查请求数据再实际执行

## 使用前准备

### 必需配置项

在使用本技能之前，您必须完成以下配置：

#### 1. 获取闲鱼管家开发者账号

- 访问 [闲鱼管家开放平台](https://www.goofish.pro)
- 注册并登录您的开发者账号
- 创建新的应用，获取以下关键信息：
  - **应用KEY (appKey)**：一串数字，如 `203413189371893`
  - **应用密钥 (appSecret)**：一串字母数字组合，如 `o9wl81dncmvby3ijpq7eur456zhgtaxs`

#### 2. 配置环境变量（推荐方式）

将获取到的密钥信息配置为环境变量，这是最安全的方式：

```bash
# Linux/Mac系统
export XIAN_YU_APP_KEY=您的应用KEY
export XIAN_YU_APP_SECRET=您的应用密钥

# Windows系统（命令提示符）
set XIAN_YU_APP_KEY=您的应用KEY
set XIAN_YU_APP_SECRET=您的应用密钥
```

#### 3. 或者程序化配置

如果您不想使用环境变量，也可以在代码中直接传入密钥：

```python
from xianyu_api_client_skill import XianYuAPIClient

client = XianYuAPIClient(
    app_key="您的应用KEY",
    app_secret="您的应用密钥"
)
```

### 权限要求

- 您的闲鱼管家应用必须具有相应的API调用权限
- 确保您的闲鱼店铺已经通过相关认证
- 某些高级功能可能需要额外的权限申请

## 支持的功能范围

### 商品管理

**创建商品完整参数说明（基于实际成功经验）：**

```json
{
  "item_biz_type": 2,
  "sp_biz_type": 1, 
  "channel_cat_id": "e11455b218c06e7ae10cfa39bf43dc0f",
  "price": 29900,
  "original_price": 39900,
  "express_fee": 0,
  "stock": 1,
  "outer_id": "YOUR_UNIQUE_ID",
  "stuff_status": 100,
  "publish_shop": [{
    "user_name": "您的闲鱼号",           // 必需！如：xy137114666612
    "images": ["https://example.com/image.jpg"],  // 必需！至少1张图片URL
    "title": "商品标题",              // ≤60字符，不能包含表情符号
    "content": "详细商品描述",
    "service_support": "SDR",         // 固定值
    "province": 110000,              // 省代码
    "city": 110100,                  // 市代码  
    "district": 110101               // 区代码
  }]
}
```

**关键注意事项：**

- ✅ **user_name必需**：必须填写您的真实闲鱼号

- ✅ **images必需**：必须提供有效的图片URL数组

- ✅ **标题限制**：不超过60字符，不能包含表情符号（🎯❌）

- ✅ **价格单位**：以分为单位（29900 = ¥299）

- ✅ **成功响应**：code=0 表示成功，不是200

- 查询商品详情和列表

- 编辑商品信息

- 商品上下架操作

- 库存管理

- 商品删除

### 用户与店铺

- 查询闲鱼店铺信息
- 获取店铺统计数据

### 订单处理

- 查询订单列表和详情
- 订单物流发货
- 订单价格修改

### 辅助功能

- 查询商品类目和属性
- 查询快递公司信息
- 省市区数据标准化

## 安全确认机制

本技能采用强制确认机制，确保所有高风险操作都是安全且可控的：

### 默认安全模式（推荐）

所有写操作**默认需要用户确认**，无法跳过。以下操作会暂停并等待用户确认：

- 创建商品 (`/api/open/product/create`)
- 编辑商品 (`/api/open/product/edit`)
- 删除商品 (`/api/open/product/del`)
- 上架/下架商品 (`/api/open/product/onshelf`, `/api/open/product/offshelf`)
- 修改订单价格 (`/api/open/order/modifyprice`)
- 订单发货 (`/api/open/order/logistics`)

```python
# 默认安全模式：高风险操作会暂停等待确认
client.request("/api/open/product/create", product_data)
client.create_product(product_data)
client.delete_product(product_data)
client.modify_order_price(order_data)
```

### Dry Run 预览模式

在实际执行前，先用 `dry_run=True` 预览请求数据：

```python
# 预览请求，不实际发送
result = client.request("/api/open/product/create", product_data, dry_run=True)
```

### 自动化模式（Unsafe 方法）

对于确认需要自动化脚本使用的场景，提供了 `_unsafe` 后缀的方法。这些方法**跳过所有确认**，请务必先用 `dry_run=True` 预览：

```python
# 1. 先预览确认数据正确
client.request_unsafe("/api/open/product/create", product_data, dry_run=True)

# 2. 预览无误后执行（跳过确认）
result = client.request_unsafe("/api/open/product/create", product_data)

# 或者使用便捷方法
client.create_product_unsafe(product_data)
client.delete_product_unsafe(product_data)
client.modify_order_price_unsafe(order_data)
```

**警告**：`_unsafe` 方法跳过所有安全确认，仅适用于：
- 已验证过的自动化脚本
- 经过 dry_run 预览的请求
- 使用低权限凭证的自动化账户

## Security Model

This skill interacts with the Xianyu Guanjia Open Platform using API credentials. The following security controls are enforced at the code level.

### Scope of Access

This skill should only be installed if you need Xianyu shop automation. It is designed exclusively for managing products, orders, and store information on the Xianyu marketplace. It does not access any other platform, service, or local resource beyond the Xianyu Open Platform API.

### Endpoint Allowlist (Code-Enforced)

All API calls are restricted to a hardcoded allowlist in `__init__.py`. Any request to an endpoint outside this list is rejected with a `ValueError` before any network call is made. The allowed endpoints are:

| Endpoint | Type | Confirmation |
|----------|------|:---:|
| `/api/open/product/detail` | Read | No |
| `/api/open/product/list` | Read | No |
| `/api/open/order/detail` | Read | No |
| `/api/open/order/list` | Read | No |
| `/api/open/user/shopinfo` | Read | No |
| `/api/open/category/query` | Read | No |
| `/api/open/express/companies` | Read | No |
| `/api/open/area/geo` | Read | No |
| `/api/open/product/create` | **Write** | **Yes** |
| `/api/open/product/edit` | **Write** | **Yes** |
| `/api/open/product/del` | **Write** | **Yes** |
| `/api/open/product/onshelf` | **Write** | **Yes** |
| `/api/open/product/offshelf` | **Write** | **Yes** |
| `/api/open/order/modifyprice` | **Write** | **Yes** |
| `/api/open/order/logistics` | **Write** | **Yes** |

### Write Operation Confirmation (Code-Enforced)

All write operations (create, edit, delete, on/off-shelf, price change, logistics) are defined in `HIGH_RISK_ENDPOINTS` and **require interactive user confirmation by default**. The default `request()` method calls `_do_request(endpoint, data, confirm=True)`, which prints the full request payload and waits for explicit `y` input before proceeding.

```python
# Default path: ALWAYS prompts for confirmation before write operations
client.request("/api/open/product/create", product_data)   # prompts [y/N]
client.create_product(product_data)                         # prompts [y/N]
client.delete_product(product_data)                         # prompts [y/N]
client.modify_order_price(order_data)                       # prompts [y/N]
```

There is no way to suppress confirmation through the default `request()` method.

### Dry-Run Mode

All methods support `dry_run=True`, which prints the full request payload without making any network call. Always use dry-run before executing write operations:

```python
result = client.request("/api/open/product/create", product_data, dry_run=True)
# Output: [Dry Run] full JSON payload — no API call made
```

### Unsafe Methods (Explicit Opt-In for Automation)

For controlled automation scenarios, the skill provides separately named `_unsafe` methods (`request_unsafe`, `create_product_unsafe`, `delete_product_unsafe`, `modify_order_price_unsafe`) that skip the interactive confirmation prompt.

**These methods are intentionally separated from the default safe path** to prevent accidental use. They should only be used when:

1. The caller has already reviewed the request via `dry_run=True`
2. The automation workflow is tightly controlled and audited
3. The credentials used have minimum necessary permissions
4. The caller explicitly chooses the `_unsafe` variant by name

The `_unsafe` methods are not accessible through the default `request()` path. An agent or script must explicitly call `request_unsafe()` or `create_product_unsafe()` by name.

### Credential Security

This skill reads Xianyu API credentials (`XIAN_YU_APP_KEY`, `XIAN_YU_APP_SECRET`) from environment variables or constructor parameters. These credentials are used solely for signing API requests to the Xianyu Open Platform.

**Required practices:**

- **Use a dedicated low-permission Xianyu application key** for this skill. Do not reuse credentials from other applications.
- **Store secrets in environment variables or a secret manager.** Never hardcode credentials in source code or commit them to version control.
- **Rotate credentials periodically** (recommended: every 3-6 months) and immediately if compromise is suspected.
- **Do not share credentials with unrelated skills or agents.** Each skill should use its own dedicated application key with minimum necessary API permissions.
- **Revoke credentials immediately** if the skill is uninstalled or no longer trusted.

### 请求限制

- **遵守API频率限制**：闲鱼管家有严格的请求频率限制，请合理安排请求间隔
- **批量操作优化**：优先使用批量API而不是多次单次调用
- **错误重试策略**：实现合理的重试机制，避免因临时网络问题导致失败

## 依赖关系

本技能是其他闲鱼相关技能的基础依赖：

- **xianyu-product-manager-skill**：商品管理技能依赖本技能进行API通信
- **xianyu-automation-skill**：自动化技能依赖本技能执行所有底层操作

## 版本兼容性

- **当前版本**：1.0.3
- **API兼容性**：闲鱼管家开放平台 v1
- **Python版本**：3.7+

## 故障排除

如果遇到问题，请按以下步骤排查：

1. **检查配置**：确认appKey和appSecret正确无误
2. **验证权限**：确认您的应用具有相应API权限
3. **查看日志**：启用详细日志模式获取更多信息
4. **联系支持**：如果问题持续存在，请联系闲鱼管家技术支持

## 开始使用

配置完成后，您就可以在其他闲鱼技能中无缝使用本技能，或者直接调用其提供的API方法进行自定义开发。