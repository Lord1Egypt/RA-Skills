---
name: search-1688-supplier
category: official-1688
description: >-
  通过 AlphaShop API 搜索和筛选1688供应商。支持三种输入方式：
  1688商品链接（查找特定商品的供应商）、图片URL（以图搜货）、
  文字关键词（按关键词搜索供应商）。支持按最高价格、最大起批量、
  最低48H发货率进行筛选。适用于查找1688供应商、搜索工厂、
  以图找商、找供应商、搜商家等场景。
metadata:
  version: 1.0.4
  label: 1688供应商搜索
  author: 1688官方技术团队
---

# 1688 供应商搜索

通过 AlphaShop 的 AI 选商 API 搜索1688供应商，支持本地筛选过滤。

## 前置配置（必须先完成）

⚠️ **使用本 SKILL 前，必须先配置以下环境变量，否则供应商搜索 API 调用会失败。**

| 环境变量 | 说明 | 必填 | 获取方式 |
|---------|------|------|---------|
| `ALPHASHOP_ACCESS_KEY` | AlphaShop API 的 Access Key（用于生成 JWT 认证 token） | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |
| `ALPHASHOP_SECRET_KEY` | AlphaShop API 的 Secret Key（用于生成 JWT 认证 token） | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |

如果用户没有提供这些密钥，**必须先询问用户获取后再继续操作**。

**⚠️ AlphaShop 接口欠费处理：** 如果调用 AlphaShop 接口时返回欠费/余额不足相关的错误，**必须立即中断当前流程**，提示用户前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分后再继续操作。

### 配置方式

在 OpenClaw config 中配置：
```json5
{
  skills: {
    entries: {
      "search-1688-supplier": {
        env: {
          ALPHASHOP_ACCESS_KEY: "YOUR_AK",
          ALPHASHOP_SECRET_KEY: "YOUR_SK"
        }
      }
    }
  }
}
```

## 使用方法

```bash
# 按关键词搜索（默认 Auto 模式，让 API 自动判断最佳搜索模式）
python3 scripts/search.py "连衣裙"

# 通过1688商品链接搜索（自动提取商品信息后搜索）
python3 scripts/search.py "https://detail.1688.com/offer/945957565364.html"

# 通过图片URL搜索（以图搜货）
python3 scripts/search.py "https://example.com/product.jpg"

# 带筛选条件搜索（仅在用户明确要求筛选时才加）
python3 scripts/search.py "连衣裙" --max-price 50 --max-moq 100
```

### ⚠️ 搜索模式规则

**默认使用 Auto 模式（不指定 `--mode`），让 API 自动判断。** 禁止自行指定 `--mode SEARCH_OFFER` 或 `--mode SEARCH_PROVIDER`，除非用户明确要求。

### ⚠️ 筛选条件规则

**只有用户明确提出筛选要求时才加对应参数。** 不要自作主张添加筛选条件（如 `--min-ship-rate-48h`），否则可能把有效结果全部过滤掉。用户说"质量好服务好"不等于要加筛选参数——这些信息在返回结果中可以直接看到和分析。

## 输入类型自动识别

脚本会自动识别输入类型：
1. **1688链接**（`detail.1688.com/offer/xxx.html`）→ 通过详情API提取商品标题和图片，再进行搜索
2. **图片URL**（http/https 且包含图片特征）→ 传入 `searchImageUrl` 参数进行以图搜货
3. **商品ID**（纯数字）→ 自动转换为1688链接处理
4. **文本关键词** → 传入 `query` 参数进行关键词搜索

## 筛选条件（API 返回后本地过滤）

| 参数 | 说明 |
|------|------|
| `--max-price` | 最高单价（浮点数），过滤掉价格超过阈值的商品 |
| `--max-moq` | 最大起批量（整数），从 `purchaseInfos` 中解析 |
| `--min-ship-rate-48h` | 最低48H发货率（浮点数，如90表示≥90%），从 `shipInfos` 中解析 |

筛选条件仅对 `SEARCH_OFFER` 模式的结果（offerList）生效。

**筛选严格度：**
- `--max-price` / `--max-moq`：如果字段无法解析，该商品会被**保留**（这些字段通常都有值）
- `--min-ship-rate-48h`：如果48H发货率无法解析（如值为"-"），该商品会被**排除**。用户明确要求此指标时，没有数据的商品不应展示。

## 输出格式

JSON 格式，仅返回筛选后的**第一条匹配结果**：

- `realIntention`：API 实际使用的搜索模式
- `filters_applied`：生效的筛选条件
- `total_before_filter` / `total_after_filter`：筛选前后的结果数量
- `match`：第一条匹配结果，包含：
  - **SEARCH_OFFER 模式**：`product`（商品标题、价格、图片、属性、采购/物流信息）+ `supplier`（公司信息、标签、服务）
  - **SEARCH_PROVIDER 模式**：`supplier`（公司信息、标签、服务）+ `recommendedProducts`（推荐商品列表）
- 如果没有匹配结果，`match` 为 null，并附带 `message` 说明

## 无匹配结果处理规则

当筛选后 `match` 为 null（没有符合条件的供应商/商品）时：

1. **如实告知用户没有找到符合条件的供应商**，不要展示不符合条件的结果
2. **说明原因**：告知筛选前有多少结果、筛选后剩0个、哪个条件导致全部被过滤
3. **给出建议**：让用户自己决定是否放宽条件，列出可调整的选项

**禁止**：不要因为筛选结果为空就偷偷去掉筛选条件重新搜索，也不要把不符合条件的商品当作匹配结果展示。

## 查询规则

**严格使用用户原始查询内容，禁止自行替换或修改。** 即使当前查询没有返回理想结果（如筛选后为空），也不要擅自更换关键词重新搜索。应将实际结果如实反馈给用户，由用户自己决定是否调整查询词或筛选条件。

## 展示规则

展示结果时必须严格按以下顺序，不要混排：

### 1. 商品图片
使用 markdown 图片语法渲染：
- **SEARCH_OFFER 模式**：`![商品图片](match.product.imageUrl)`
- **SEARCH_PROVIDER 模式**：`![商品图片](item.imageUrl)`（针对 `match.recommendedProducts` 中的每个商品）

### 2. 商品详情
商品名称、价格、起批量、发货地、物流数据（48H揽收率/履约率）、销量、核心属性。

**商品链接（必须展示）**：使用 `match.product.detailUrl` 字段。如果该字段为空，则用 `match.product.itemId` 拼接：`https://detail.1688.com/offer/{itemId}.html`。展示时使用 markdown 超链接格式 `[查看商品](url)`，**禁止直接展示原始URL**。

### 3. 供应商信息
公司名称、诚信通年限、标签（源头工厂等）、30天订单、180天买家、品质退款率、客服响应率、回头率、综合服务分、跨境服务标签、店铺链接等。

### 4. 快速评价
对这个商品+供应商的综合点评，包含亮点（✅）和注意事项（⚠️）。

## API 参考文档

完整的 API 接口和数据结构文档请参阅 [references/api.md](references/api.md)。
