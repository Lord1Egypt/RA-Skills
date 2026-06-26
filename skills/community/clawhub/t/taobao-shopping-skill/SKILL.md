---
name: taobao-shopping
description: "淘宝购物助手 — 搜索商品、查看商品详情、加入购物车、查看购物车（支持价格变动提示）、查看评价。当用户提到淘宝购物、查找商品、查看购物车、比价、加入购物车，或需要从淘宝获取商品信息时使用此 skill。支持按销量/价格排序搜索、商品规格选择、批量操作。"
version: 1.0.0
author: He2y
tags: [taobao, shopping, cart, ecommerce, china, search]
---

# 淘宝购物助手 (taobao-shopping)

基于 OpenCLI 的淘宝购物全流程自动化 skill，支持搜索、详情、加购、购物车管理、评价查询。

## 前置要求

1. **Chrome 浏览器已安装且登录淘宝/天猫账号**
2. **OpenCLI 已安装**：`npm install -g @jackwener/opencli`
3. **OpenCLI Browser Bridge 扩展已加载**（在 Chrome 扩展管理页加载 `extension/` 目录为未打包扩展）

> **重要**：首次使用前，请确保 Chrome 已登录淘宝 (www.taobao.com)，因为所有命令依赖 Cookie 认证。

## 快速开始

```bash
# 搜索商品
opencli taobao search "iPhone 17 Pro Max" --limit 10

# 查看商品详情
opencli taobao detail <商品ID>

# 加入购物车
opencli taobao add-cart <商品ID>

# 查看购物车（含价格变动）
opencli taobao cart

# 查看商品评价
opencli taobao reviews <商品ID> --limit 10
```

## 命令详解

### 1. search — 淘宝商品搜索

```bash
opencli taobao search <关键词> [选项]
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | 位置参数 | 必填 | 搜索关键词 |
| `--sort` | 选择 | `default` | 排序方式：`default`(综合)、`sale`(销量)、`price`(价格) |
| `--limit` | 整数 | `10` | 返回结果数量（最大 40） |

**输出格式：**
```
rank | title | price | sales | shop | location | item_id | url
```

**示例：**
```bash
# 搜索 iPhone，按销量排序
opencli taobao search "iPhone 17 Pro Max" --sort sale --limit 20

# 搜索T恤，按价格升序
opencli taobao search "T恤 男" --sort price --limit 10
```

---

### 2. detail — 淘宝商品详情

```bash
opencli taobao detail <商品ID> [选项]
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | 位置参数 | 必填 | 商品 ID（从搜索结果的 item_id 字段获取） |

**输出格式：**
```
field | value
```

包含字段：商品名称、价格、销量、评价数、店铺评分、店铺名称、发货地、可选规格、ID、链接

**示例：**
```bash
opencli taobao detail 827563850178
```

---

### 3. add-cart — 加入购物车

```bash
opencli taobao add-cart <商品ID> [选项]
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | 位置参数 | 必填 | 商品 ID |
| `--spec` | 字符串 | 无 | 规格关键词（如 "红色 XL"，多个用空格分隔，模糊匹配） |
| `--dry-run` | 布尔 | `false` | 仅预览，不实际加入购物车 |

**输出格式：**
```
status | title | price | selected_spec | item_id
```

**示例：**
```bash
# 加入购物车（自动选择第一个可用规格）
opencli taobao add-cart 827563850178

# 指定规格加入购物车
opencli taobao add-cart 827563850178 --spec "银色 512G"

# 预览模式（不实际加入）
opencli taobao add-cart 827563850178 --spec "银色 512G" --dry-run
```

---

### 4. cart — 查看购物车

```bash
opencli taobao cart [选项]
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--limit` | 整数 | `20` | 返回商品数量（最大 50） |

**输出格式：**
```
index | title | price | spec | shop
```

**💡 特色功能：价格变动提示**
- 购物车返回数据包含**现价**和**原价**
- 如果商品有降价，显示格式如：`￥153 (原价￥237, 省84.00)`
- 可以快速识别降价商品

**示例：**
```bash
# 查看购物车前20件商品
opencli taobao cart

# 查看更多商品
opencli taobao cart --limit 50
```

---

### 5. reviews — 查看商品评价

```bash
opencli taobao reviews <商品ID> [选项]
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | 位置参数 | 必填 | 商品 ID |
| `--limit` | 整数 | `10` | 返回评价数量（最大 20） |

**输出格式：**
```
rank | user | content | date | spec
```

**示例：**
```bash
opencli taobao reviews 827563850178 --limit 20
```

---

## 输出格式选项

所有命令支持 `--format` / `-f` 参数：

| 格式 | 说明 |
|------|------|
| `table` | 表格形式（默认） |
| `json` | JSON 数组 |
| `yaml` | YAML 格式 |
| `md` | Markdown 表格 |
| `csv` | CSV 格式 |

**示例：**
```bash
opencli taobao search "iPhone" -f json
opencli taobao cart -f csv
```

---

## 常见问题

### Q: 命令执行缓慢怎么办？
A: 首次执行需要建立浏览器会话（约 7 秒），后续执行会复用会话。可以使用 `--format json` 加速输出解析。

### Q: 提示 "auth-required" 怎么办？
A: 需要在 Chrome 中登录淘宝。打开 www.taobao.com，手动登录后重试。

### Q: 如何获取商品 ID？
A: 使用 `search` 命令，结果中的 `item_id` 字段即为商品 ID。也可以从商品链接中提取：`https://item.taobao.com/item.htm?id=XXXXXXXX`

### Q: 购物车显示的价格是旧的吗？
A: 购物车数据会实时获取，如果商品有降价，会同时显示原价和现价，方便识别。

---

## 依赖说明

此 skill 依赖 OpenCLI 项目中的淘宝适配器模块（`@jackwener/opencli`）。适配器源代码位于：
- 搜索/详情/评价：基于浏览器 DOM 解析
- 购物车：基于购物车页面文本解析
- 加入购物车：基于页面 UI 自动化

所有适配器均使用 **Cookie 认证策略**，无需额外 API Key。

---

## 更新日志

### v1.0.0 (2026-04-14)
- 初始版本
- 支持 search、detail、add-cart、cart、reviews 五个核心命令
- 支持价格变动提示
- 支持多种输出格式
