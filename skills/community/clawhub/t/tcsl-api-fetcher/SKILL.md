# 天财商龙(tcsl)开放平台 Skill

> 📅 数据更新: 2026-04-27（Playwright 实时抓取）
> 📊 模块: 9 个 | 接口: **99** 个 | 87 含路径
> 🌳 菜单: Element UI 树 (`el-tree`)

## API 模块

| 模块 | 接口数 | Base URL | 说明 |
|------|--------|----------|------|
| **餐饮系统(cy7)** | 11 | `openapi.tcsl.com.cn/cy7/api` | 门店/品项/员工档案 |
| **三方调用(cyfront)** | 16 | `open-test.tcsl.com.cn/cyfront/api` | 菜品同步/查询/上架 |
| **智慧餐厅(无香)** | 13 | `openapi.tcsl.com.cn/wuuxiang` | 点餐/外卖/桌访 |
| **云资金(yzj)** | 10 | `open-test.tcsl.com/api/yzj` | 支付/退款/账务 |
| **订单/SCM8** | 2 | `openapi.tcsl.com.cn/scm8` | 订单查询 |
| **供应链(fx)** | 10 | `openapi.tcsl.com.cn/fx` | 门店/品项/采购 |
| **会员中心(crm)** | 2 | `openapi.tcsl.com.cn/crm` | 会员/交易查询 |
| **SRM** | 2 | `openapi.tcsl.com.cn/srm` | 采购订单/退货 |
| **商龙云(sly)** | 24 | `openapi.tcsl.com.cn/sly` | 物料/品牌/门店/员工CRUD |
| **回调通知** | 6 | — | 支付/点餐状态回调 |
| **通用/文档** | 3 | — | 约定/状态码/样例 |

**总计：99 个接口**

## 三平台对比

| 维度 | 企迈 | 客如云 | 天财商龙 |
|------|------|--------|----------|
| 菜单框架 | qm-tree (vue) | Tailwind ul/li | el-tree (Element) |
| API 数量 | 307 | 178 | **99** |
| 方法 | GET+POST | POST | POST |
| 多 Base URL | ❌ 单一 | ❌ 单一 | ✅ 8个不同Base |
| 解决方案 | 10 (91映射) | 10 (84映射) | ⏳ 待抓取 |
| 沙箱环境 | ❌ | ❌ | ✅ open-test.tcsl.com.cn |

## 更新日志

### 2026-04-27
- 🎯 首次抓取：Element UI 树展开 99 个 API 节点
- 📊 按 Base URL 自动归类 9 个模块
