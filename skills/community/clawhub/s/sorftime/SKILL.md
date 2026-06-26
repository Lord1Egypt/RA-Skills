---
name: sorftime-cli
description: >
  通过 sorftime-cli 调用 Sorftime 跨境电商全量数据接口（Amazon 47 + Shopee 5 + Walmart 14 = 66 个 endpoint）。
  当用户或智能体需要：写脚本批量查询 ASIN/类目/关键词/Best Seller/跟卖/子体销量/产品评论，
  自定义编排多个接口完成灵活工作流（如批量采集 → 交叉分析 → 定时监控），
  **必须**使用本技能。
  触发词：sorftime api、sorftime cli、调用 sorftime、批量查 ASIN、批量类目数据、
  sorftime endpoint、自定义 sorftime 工作流、写 sorftime 脚本、sorftime 接口手册、
  amazon 接口、shopee 接口、walmart 接口、sorftime 批量获取、监控注册、跟卖预警脚本、
  子体销量、关键词监控部署、Best Seller 榜单抓取、类目趋势分析脚本、
  跨平台对比（Amazon+Shopee+Walmart）。
---

# Sorftime CLI Skill

Sorftime 提供 Amazon、Shopee、Walmart 三大电商平台的数据分析 API，通过 `sorftime-cli` 命令行工具调用。

## 前置配置

### 安装与认证
> 🔒 安全说明：本工具完全开源，代码可公开审计
> - 开源仓库地址：https://github.com/sorftime/sorftime-cli
> - npm 官方包主页：https://www.npmjs.com/package/sorftime-cli
> - 发布者为 Sorftime 官方认证账号，无恶意代码


```bash
# 全局安装官方 CLI（推荐）
npm install -g sorftime-cli

# 添加账户 （profile-name 可以任意命名， api-key 在 Sorftime 官网获取：https://www.sorftime.com/cli）
sorftime add <profile-name> <api-key>
# 激活账号
sorftime use <profile-name>

```

### 账户管理
```bash
# 列出所有账户
sorftime list / sorftime ls

# 切换当前活跃账户
sorftime use <profile-name>

# 查看当前活跃账户
sorftime whoami

# 删除账户
sorftime remove <profile-name>
```

### 通用命令格式
```bash
sorftime api <接口名称> '{"参数JSON"}' --domain <站点数字ID>
```

### 通用返回结构
所有接口返回统一结构：
```json
{
  "code": 0,
  "message": null,
  "data": {},
  "requestleft": 9999,
  "requestconsumed": 1,
  "requestcount": 1
}
```
- `code=0` 成功，非0失败
- `requestleft` 当月剩余请求次数
- `requestconsumed` 本次消耗次数

### 常见错误码

完整错误码表（按平台区分）见 [`_common.md`](resources/_common.md#6-错误码表)。快速参考：

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 0 | 成功 | - |
| 4 | 积分余额不足 | 充值或等待下月重置 |
| 10 | 请求参数错误 | 检查参数格式、类型、必填项 |
| 97 | ASIN/产品不存在 | 检查参数 |
| 98 | 采集失败 | 稍后重试 |
| 99 | 正在实时抓取 | 等待后重试 |
| 400 | 非认证 IP | 检查 IP 白名单 |
| 401 | 认证失败/请求接口未开放 | 检查 Account-SK 和接口名称 |
| 500 | 本月请求已达限额 | 等待下月重置或升级套餐 |
| 501 | 一分钟请求已达限额 | 降低频率，1分钟后重试 |
| 502 | 一天请求已达限额 | 等待次日重置或升级套餐 |


---
## Resources 目录索引（按需加载）

> 所有 resources 文件头部均指向 `_common.md` 获取 CLI 模板、Domain 表、错误码。本索引只列接口清单与跳转。

### 公共参考

| 文件 | 内容 |
|------|------|
| [`_common.md`](resources/_common.md) | Amazon/Shopee/Walmart Domain 表、完整错误码（按平台区分）、通用返回结构、CLI 调用模板 |
| [`account.md`](resources/account.md) | 跨平台通用账户管理（3 接口）：CoinQuery、CoinStream、RequestStream |

### Amazon（47 个 endpoint）

| 文件 | 接口数 | 接口清单 |
|------|--------|---------|
| [`amazon-category.md`](resources/amazon-category.md) | 5 | CategoryTree、CategoryRequest、CategoryProducts、CategoryTrend、CategorySearchFromName |
| [`amazon-product.md`](resources/amazon-product.md) | 11 | ProductRequest、ProductSearch、AsinSalesVolume、ProductVariationHistory、ProductReviewsCollection、ProductReviewsCollectionStatusQuery、ProductReviewsQuery、ProductSearchFromName、ASINSubscription、ASINSubscriptionQuery、ASINSubscriptionCollection |
| [`amazon-product-realtime.md`](resources/amazon-product-realtime.md) | 5 | ProductRealtimeRequest、ProductRealtimeRequestStatusQuery、SimilarProductRealtimeRequest、SimilarProductRealtimeRequestStatusQuery、SimilarProductRealtimeRequestCollection |
| [`amazon-keyword.md`](resources/amazon-keyword.md) | 12 | KeywordQuery、KeywordRequest、KeywordSearchResults、KeywordSearchResultTrend、KeywordExtends、CategoryRequestKeyword、ASINRequestKeywordv2、KeywordProductRanking、ASINKeywordRanking、FavoriteKeyword、ChangeFavoriteKeyword、GetFavoriteKeyword |
| [`amazon-monitoring.md`](resources/amazon-monitoring.md) | — | 监控通用规则：period 表达式、积分消耗、站点矩阵、任务状态流转。**接口详情跳转到 3 个子文件。** |
| [`amazon-monitoring-keyword.md`](resources/amazon-monitoring-keyword.md) | 5 | KeywordBatchSubscription、KeywordTasks、KeywordBatchTaskUpdate、KeywordBatchScheduleList、KeywordBatchScheduleDetail |
| [`amazon-monitoring-bestseller.md`](resources/amazon-monitoring-bestseller.md) | 4 | BestSellerListSubscription、BestSellerListTask、BestSellerListDelete、BestSellerListDataCollect |
| [`amazon-monitoring-seller.md`](resources/amazon-monitoring-seller.md) | 5 | ProductSellerSubscription、ProductSellerTasks、ProductSellerTaskUpdate、ProductSellerTaskScheduleList、ProductSellerTaskScheduleDetail |
| [`amazon-recipes.md`](resources/amazon-recipes.md) | — | **多接口编排配方**：选品流程、竞品深挖、监控部署、趋势追踪、跨平台对比。展示 CLI 比 MCP 灵活的核心场景。 |

### Shopee（5 个 endpoint）

| 文件 | 接口数 | 接口清单 |
|------|--------|---------|
| [`shopee-api.md`](resources/shopee-api.md) | 5 | CategoryTree、CategoryRequest、ProductRequest、ProductTrend、ShopRequest |
| [`shopee-data-types.md`](resources/shopee-data-types.md) | — | Shopee 数据类型定义 |

### Walmart（14 个 endpoint）

| 文件 | 接口数 | 接口清单 |
|------|--------|---------|
| [`walmart-api.md`](resources/walmart-api.md) | 5 | CategoryTree、CategoryRequest、ProductRequest、ProductTrendRequest、ProductSalesVolume |
| [`walmart-keyword.md`](resources/walmart-keyword.md) | 9 | KeywordQuery、KeywordSearchFromName、KeywordSearchResults、KeywordRequest、ProductRequestKeyword、KeywordExtends、FavoriteKeyword、ChangeFavoriteKeyword、GetFavoriteKeyword |
| [`walmart-data-types.md`](resources/walmart-data-types.md) | — | Walmart 数据类型定义 |

---

## 目录结构

```
sorftime-cli/
├── SKILL.md                              # 本文件：主索引 + 触发器 + 分流声明
├── README.md                             # 快速参考指南
└── resources/
    ├── _common.md                        # 公共：Domain 表 / 错误码 / 返回结构 / CLI 模板
    ├── account.md                        # 跨平台通用账户管理（3 接口）
    ├── amazon-category.md                # Amazon 类目 5 接口
    ├── amazon-product.md                 # Amazon 产品核心 11 接口
    ├── amazon-product-realtime.md        # Amazon 产品实时采集 5 接口
    ├── amazon-keyword.md                 # Amazon 关键词 12 接口
    ├── amazon-monitoring.md              # Amazon 监控通用规则（索引）
    ├── amazon-monitoring-keyword.md      # Amazon 关键词监控 5 接口
    ├── amazon-monitoring-bestseller.md   # Amazon Best Seller 监控 4 接口
    ├── amazon-monitoring-seller.md       # Amazon 跟卖监控 5 接口
    ├── amazon-recipes.md                 # 多接口编排配方（CLI 差异化场景）
    ├── shopee-api.md                     # Shopee 5 接口
    ├── shopee-data-types.md              # Shopee 数据类型定义
    ├── walmart-api.md                    # Walmart 类目+产品 5 接口
    ├── walmart-keyword.md                # Walmart 关键词+词库 9 接口
    └── walmart-data-types.md             # Walmart 数据类型定义
```

---

## 重要规则

1. **不要猜测 domain 值** — 始终使用 `_common.md` 中的站点速查表
2. **JSON 参数用单引号包裹** — `sorftime api XXX '{"key": "value"}'`
3. **大响应设置超时** — CategoryTree 返回约10MB+数据，建议设置较长超时时间
4. **错误码判断** — 以 `code` 字段为准（小写），`code=0` 表示成功
