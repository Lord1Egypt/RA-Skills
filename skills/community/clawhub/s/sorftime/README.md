# Sorftime CLI 快速参考

> 基于 npm 包 `sorftime-cli`，调用 Sorftime 跨境电商全量 66 个数据接口（Amazon 47 + Shopee 5 + Walmart 14）。

---

## 安装

```bash
npm install -g sorftime-cli

# 配置 profile（token 在 Sorftime 专业版后台获取）
sorftime add myprofile <your-account-sk>
sorftime use myprofile
```

---

## 5 分钟上手

```bash
# 1. 查 类目 Best Seller Top 100
sorftime api CategoryRequest '{"nodeId": "3743561"}' --domain 1

# 2. 查单个产品详情
sorftime api ProductRequest '{"asin": "B0CVM8TXHP"}' --domain 1

# 3. 查关键词 "power bank" 的详情
sorftime api KeywordRequest '{"keyword": "power bank"}' --domain 1

# 4. 多条件组合筛选（关键词：Power Bank + 价格范围：20-50 + 月销量大于500）
sorftime api ProductSearch '{"keyword":"Power Bank","PriceRangeMin":20,"PriceRangeMax":50,"MonthSaleVolumeRangeMin":500}' --domain 1
```

---

## Domain 速查

### Amazon（14个站点）

| domain | 站点 | 区域 | domain | 站点 | 区域 |
|--------|------|------|--------|------|------|
| 1 | us 美国 | 北美 | 7 | jp 日本 | 亚洲 |
| 2 | gb 英国 | 欧洲 | 8 | es 西班牙 | 欧洲 |
| 3 | de 德国 | 欧洲 | 9 | it 意大利 | 欧洲 |
| 4 | fr 法国 | 欧洲 | 10 | mx 墨西哥 | 北美 |
| 5 | in 印度 | 亚洲 | 11 | ae 阿联酋 | 中东 |
| 6 | ca 加拿大 | 北美 | 12 | au 澳大利亚 | 大洋洲 |
| | | | 13 | br 巴西 | 南美 |
| | | | 14 | sa 沙特 | 中东 |

### Shopee（8个站点）

| domain | 站点 | domain | 站点 |
|--------|------|--------|------|
| 201 | vn 越南 | 205 | my 马来西亚 |
| 202 | id 印尼 | 206 | tw 中国台湾 |
| 203 | sg 新加坡 | 207 | ph 菲律宾 |
| 204 | th 泰国 | 208 | br 巴西 |

### Walmart

| domain | 站点 |
|--------|------|
| 21 | us 美国 |

---

## 文件索引

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

## CLI vs API vs MCP 怎么选

Sorftime 提供三种数据访问方式，覆盖不同使用人群：

| 维度 | CLI（本工具） | 直接调用 API | MCP（AI 智能体工具） |
|------|-------------|------------|-------------------|
| **本质** | 官方封装的命令行客户端 | 原始 HTTP 接口 | AI 智能体的预设工具集 |
| **覆盖范围** | 全量 61 个 endpoint | 全量 61 个 endpoint | 预设子集（约 42 个） |
| **使用方式** | 写脚本、命令行批处理 | 集成到自有系统/代码 | 自然语言对话 |
| **参数灵活度** | 任意 endpoint + 任意参数 | 完全自由 | 受限于预设字段 |
| **适用人群** | 开发者、数据分析师 | 有技术团队的卖家 | 普通运营、卖家 |
| **典型场景** | 批量查询、定时监控、自定义工作流 | 自建 ERP/BI 系统 | "帮我分析竞品""这个类目怎么样" |

**一句话**：
- 要**写脚本批处理** → 用 **CLI**
- 要**接入自有系统** → 直接调 **API**
- 要**自然语言问 AI** → 用 **MCP**

---
