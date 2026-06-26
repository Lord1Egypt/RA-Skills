---
name: zbj
version: 0.1.0
description: 猪八戒网(ZBJ) MCP服务器 - AI智能需求发布、订单管理、服务搜索、类目匹配，连接百万服务商的一站式威客平台
author: ZBJ Team
homepage: https://zmcp.zbj.com
repository: https://github.com/zbj/zbj-mcp
openclaw_version: v2026.3.7+
type: script
script:
  command: node
  args: [bridge.js]
install:
  command: npm
  args: [install]
requires:
  binaries:
    - node
    - npm
  env:
    - ZBJ_API_URL
    - ZBJ_API_KEY
primary_credential: ZBJ_API_KEY
permissions:
  - network:zmcp.zbj.com:443
security:
  sandbox: required
  autonomous: false
tags:
  - 猪八戒网
  - zbj
  - 服务交易
  - 需求发布
  - 订单管理
  - 威客平台
  - 外包服务
  - 电商平台
  - marketplace
  - freelance
  - service-platform
  - e-commerce
  - order-management
  - demand-management
  - search
  - mcp-server
  - ai-agent
  - china
  - design
  - development
keywords:
  - 猪八戒
  - 服务交易平台
  - 威客
  - 外包
  - 设计服务
  - 软件开发
  - 网站建设
  - logo设计
  - 营销推广
  - 托管支付
  - 服务商评价
  - 需求投标
  - 类目搜索
  - 店铺搜索
  - AI助手
---

# 猪八戒网(ZBJ) MCP 官方技能 🚀

基于 Model Context Protocol (MCP) 构建的**猪八戒网官方集成**，让 AI Agent 能够智能管理需求发布、订单处理、服务搜索和类目匹配，连接中国最大的服务交易平台。

## 🎯 核心功能

✅ **智能需求管理** - 发布/修改/关闭需求、选标中标、淘汰服务商
✅ **订单全流程** - 查询详情、评价服务商、获取托管支付链接
✅ **全平台搜索** - 服务商品、店铺、需求三维搜索
✅ **AI类目匹配** - 智能识别需求类型，推荐最佳服务类目

**18 个工具** + **2 个资源**，覆盖需求管理、订单管理、搜索服务、类目服务 4 大功能模块。

---

## 安装

### 自动安装（推荐）
```bash
# Clawhub 会自动执行 npm install
# 只需配置 API Key
export ZBJ_API_KEY="your_api_key_here"  # 从 https://account.zbj.com/setting/mcpapikey 获取
```

### 手动安装
```bash
# 1. 进入技能目录
cd ~/.openclaw/skills/zbj

# 2. 安装依赖
npm install

# 3. 配置环境变量
export ZBJ_API_URL="https://zmcp.zbj.com"  # 可选，默认值
export ZBJ_API_KEY="your_api_key_here"     # 必填
```

**依赖说明**：
- `axios ^1.7.7` - HTTP 请求库
- `Node.js 18+` - 运行环境

---

## 🔐 安全说明

### 最小权限原则
本技能严格遵循最小权限原则：
- ✅ **网络访问**：仅允许 `zmcp.zbj.com:443`（猪八戒网官方 API）
- ✅ **执行权限**：仅允许运行 `node` 和 `npm`
- ✅ **沙箱隔离**：强制启用沙箱模式
- ✅ **非自主运行**：需要用户明确调用，不会自动执行
- ❌ 无文件系统读写权限
- ❌ 无系统级权限
- ❌ 无高危操作权限

### API Key 安全建议
1. **使用专用 API Key**：为此技能创建独立的 API Key
2. **最小权限**：仅授予需求发布、订单管理等必要权限
3. **定期轮换**：建议每 90 天更换一次 API Key
4. **环境变量**：不要在代码中硬编码 API Key
5. **安全存储**：使用系统密钥链或加密配置存储

### 数据隐私
- 所有 API 调用通过 HTTPS 加密传输
- 不会在本地缓存敏感信息（除类目数据）
- 不会向第三方服务发送数据

---

## 🎬 适用场景

### 企业级应用
- 🏢 **智能采购助手** - 企业 AI 助手自动发布外包需求，管理服务商对接
- 📊 **订单管理系统** - 集成到企业 ERP，自动化订单跟踪和状态同步
- 💼 **供应商管理** - 批量搜索、评估、选择服务商，构建供应商库

### AI Agent 集成
- 🤖 **智能客服机器人** - 用户咨询时自动推荐服务、报价、发布需求
- 🔍 **需求分析引擎** - 自然语言理解需求，自动匹配类目和服务商
- 📈 **数据分析助手** - 分析平台服务趋势、价格区间、服务商评价

### 开发者工具
- 🌐 **多平台聚合** - 整合猪八戒网到统一服务采购平台
- 🔗 **工作流自动化** - 与 Slack、飞书、企业微信集成，自动化通知和审批
- 📱 **移动应用集成** - 企业 App 内嵌服务交易能力

---

## 工具列表（18个工具，4个模块）

### 需求管理（8个）
| 工具名 | 功能说明 |
|--------|----------|
| publish_demand | 发布或修改需求，传入 demandId 则为修改 |
| get_demand_detail | 查询需求详情（含投标情况） |
| close_demand | 关闭需求 |
| pause_demand | 暂停需求 |
| open_demand | 公开已暂停的需求 |
| eliminate_seller | 淘汰服务商 |
| select_winner | 选服务商中标 |
| search_demands | 搜索需求（支持状态筛选） |

### 订单管理（5个）
| 工具名 | 功能说明 |
|--------|----------|
| get_order_detail | 查询订单详情 |
| search_orders | 搜索订单 |
| eval_seller | 评价已完成订单的服务商 |
| close_order | 关闭订单 |
| get_trusteeship_pay_url | 获取托管支付地址 |

### 搜索服务（2个）
| 工具名 | 功能说明 |
|--------|----------|
| search_services | 搜索服务商品 |
| search_shops | 搜索店铺/服务商 |

### 类目服务（2个）
| 工具名 | 功能说明 |
|--------|----------|
| get_categories | 获取类目列表（支持层级筛选） |
| search_category | 根据关键词搜索匹配类目 |

### 系统工具（1个）
| 工具名 | 功能说明 |
|--------|----------|
| health_check | 检查后端服务健康状态 |

---

## 资源列表（2个）

| URI | 描述 | MIME 类型 |
|-----|------|-----------|
| `zbj://config` | 系统配置信息 | application/json |
| `zbj://categories` | 所有服务类目数据（AI 智能识别用） | application/json |

---

## 💡 真实使用案例

### 案例 1：企业官网开发需求发布（完整流程）

**场景**：创业公司需要找服务商开发企业官网

```typescript
// 1. AI 智能识别类目
用户："帮我找能做企业网站的服务商"
→ search_category({"keyword": "网站建设"})
→ 返回：categoryId=1001, name="网站建设"

// 2. 发布需求
→ publish_demand({
    "title": "开发响应式企业官网",
    "description": "需要PC+移动端自适应，包含首页、产品介绍、新闻资讯等5个页面",
    "categoryId": 1001,
    "price": 8000,
    "deadline": "2026-04-30"
  })
→ 返回：demandId=12345

// 3. 查看投标情况
→ get_demand_detail({"demandId": 12345})
→ 返回：已有 8 家服务商投标

// 4. 选择中标服务商
用户："选择报价 7500 的那家"
→ select_winner({"demandId": 12345, "sellerId": 67890})
```

### 案例 2：Logo 设计服务搜索与下单

**场景**：需要为新品牌设计 Logo

```typescript
// 1. 搜索 Logo 设计服务
用户："找一些 Logo 设计服务，预算 2000 以内"
→ search_services({
    "keyword": "logo设计",
    "minPrice": 500,
    "maxPrice": 2000,
    "pageSize": 10
  })

// 2. 搜索优质设计师店铺
→ search_shops({
    "keyword": "品牌设计",
    "sort": "rating"  // 按评分排序
  })

// 3. 查看订单详情
→ get_order_detail({"orderId": "ORD20260327001"})

// 4. 获取支付链接
→ get_trusteeship_pay_url({
    "orderId": "ORD20260327001",
    "hostedPrice": 1800,
    "clientType": "h5"
  })
```

### 案例 3：订单管理与服务商评价

**场景**：项目完成后进行评价

```typescript
// 1. 查询所有进行中的订单
→ search_orders({
    "status": "IN_PROGRESS",
    "pageNum": 1
  })

// 2. 查看订单详情
→ get_order_detail({"orderId": "ORD20260320005"})

// 3. 项目完成，评价服务商
用户："项目做得不错，给个好评"
→ eval_seller({
    "orderId": "ORD20260320005",
    "rating": 5,
    "comment": "设计稿很满意，沟通顺畅，交付及时，推荐！",
    "tags": ["设计专业", "沟通顺畅", "交付及时"]
  })
```

### 案例 4：AI 智能需求助手

**对话式交互示例**：

```
用户："我想做一个小程序商城"

AI：正在为您匹配最合适的服务类目...
   → search_category({"keyword": "小程序开发"})

   已找到类目：【移动应用开发 > 小程序开发】

   为您搜索相关服务商...
   → search_services({"keyword": "小程序商城", "pageSize": 5})

   找到 156 个相关服务，推荐以下 5 家：
   1. XX科技 - ¥8,000 起 ⭐4.9 (已服务 320 单)
   2. XX工作室 - ¥6,500 起 ⭐4.8 (已服务 180 单)
   ...

   是否需要我帮您发布需求，让服务商主动报价？

用户："好的，预算 1 万以内，要求支持拼团和优惠券"

AI：正在为您发布需求...
   → publish_demand({
       "title": "小程序商城开发",
       "description": "需要开发微信小程序商城，包含商品展示、购物车、订单管理、拼团功能、优惠券系统",
       "categoryId": 2103,
       "price": 10000
     })

   ✅ 需求发布成功！需求编号：#12346
   已通知平台服务商，预计 24 小时内开始收到报价。
```

---

## 🛠️ 快速开始

```bash
# 健康检查
/run zbj health_check '{}'

# 搜索类目
/run zbj search_category '{"keyword":"网站"}'

# 发布需求
/run zbj publish_demand '{"title":"开发企业官网","description":"需要开发响应式企业官网","categoryId":1001,"price":5000}'

# 搜索服务
/run zbj search_services '{"keyword":"logo设计","pageNum":1,"pageSize":20}'
```

---

## 获取 API Key

### 1. 访问 API Key 管理页面
**https://account.zbj.com/setting/mcpapikey**

### 2. 创建专用 API Key
- 为此技能创建独立的 API Key（便于管理和撤销）
- 设置合理的权限范围：
  - ✅ 需求发布与管理
  - ✅ 订单查询与管理
  - ✅ 服务搜索
  - ✅ 类目查询
  - ❌ 不需要账户管理等其他权限

### 3. 配置环境变量
```bash
# Linux/macOS
export ZBJ_API_KEY="your_api_key_here"

# Windows PowerShell
$env:ZBJ_API_KEY="your_api_key_here"

# Windows CMD
set ZBJ_API_KEY=your_api_key_here
```

### 4. 验证配置
```bash
# 运行健康检查
/run zbj health_check '{}'

# 应该返回：{"status":"ok","message":"ZBJ MCP service is running"}
```

---

## 环境变量

| 变量名 | 说明 | 必填 | 默认值 | 安全建议 |
|--------|------|------|--------|----------|
| ZBJ_API_URL | 后端 API 地址 | 否 | https://zmcp.zbj.com | 使用官方地址，除非有私有部署 |
| ZBJ_API_KEY | API 认证密钥 | ✅ 是 | - | 使用专用 Key，定期轮换，最小权限 |
| ZBJ_API_TIMEOUT | API 请求超时时间 (ms) | 否 | 30000 | 根据网络情况调整，建议 10000-60000 |

---

## 🔧 故障排查

### 常见问题

#### 1. API Key 未配置
```
Error: ZBJ_API_KEY is not set
```
**解决方案**：设置环境变量 `export ZBJ_API_KEY="your_key"`

#### 2. 网络连接失败
```
Error: connect ETIMEDOUT
```
**解决方案**：
- 检查网络连接
- 验证防火墙是否允许访问 `zmcp.zbj.com:443`
- 尝试增加超时时间 `export ZBJ_API_TIMEOUT=60000`

#### 3. API Key 权限不足
```
Error: 403 Forbidden
```
**解决方案**：在 API Key 管理页面检查并更新权限

#### 4. 依赖安装失败
```
Error: Cannot find module 'axios'
```
**解决方案**：手动运行 `npm install`

---

## 📊 技术栈与兼容性

### 核心依赖
- **TypeScript** 5.3+
- **@modelcontextprotocol/sdk** 1.0+
- **Node.js** 18+ (推荐 20 LTS)
- **Zod** 3.22+ (参数验证)
- **axios** ^1.7.7 (HTTP 客户端)

### 平台兼容性
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- ✅ Windows 10/11 (需要 Node.js 18+)
- ✅ Docker / 容器环境

---

## 📝 更新日志

### v0.1.0 (2026-03-27)
- 🎉 首次发布
- ✅ 实现 18 个工具（需求管理、订单管理、搜索、类目）
- ✅ 提供 2 个资源（配置、类目数据）
- ✅ 添加自动安装机制
- ✅ 强制沙箱隔离，最小权限原则
- ✅ 完善安全说明和故障排查文档

---

## 🤝 贡献与支持

### 报告问题
遇到问题？请访问：
- **GitHub Issues**: https://github.com/zbj/zbj-mcp/issues
- **官方文档**: https://zmcp.zbj.com/docs

### 功能建议
欢迎提交功能建议和改进意见！

### 开源协议
MIT License - 可自由使用、修改、分发

---

## ⚠️ 免责声明

1. 本技能为第三方集成工具，非猪八戒网官方客户端
2. 使用本技能前请阅读并同意猪八戒网服务条款
3. 请妥善保管 API Key，避免泄露造成损失
4. 建议在测试环境验证后再用于生产环境
5. 作者不对因使用本技能造成的任何损失负责
