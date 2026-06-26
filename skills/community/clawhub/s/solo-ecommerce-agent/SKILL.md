# solo-ecommerce-agent — 全平台全自动电商运营智能体

> 一人运营多平台店铺，无需人工干预。
> **关键词**：电商运营、自动上架、自动客服、自动发货、选品、订单处理

---

## 功能模块

| 模块 | 说明 | 自动化 |
|------|------|--------|
| 选品扫描 | 多平台热销榜单分析、机会品类推荐 | ✅ 每小时自动扫描 |
| 商品上架 | 商品信息生成、图文处理、一键发布 | ✅ 开启后自动上架 |
| 客服回复 | 买家咨询自动分类+回复，争议自动升级 | ✅ 每5分钟自动处理 |
| 订单处理 | 自动发货、物流录入、退款审核 | ✅ 每10分钟自动处理 |
| 日报汇总 | 每日23:00汇总运营数据发送通知 | ✅ 每日自动推送 |

---

## 快速开始

### 第一步：配置平台

编辑 `~/.qclaw/solo-ecommerce-data/config.json`，填入你的平台信息：

```json
{
  "platform": "douyin",        // douyin | taobao | pinduoduo | jingdong
  "store_name": "你的店铺名",
  "backend_url": "http://127.0.0.1:8080",  // 平台API地址（如有）
  "automation": {
    "publish": { "enabled": true, "need_review": false },
    "customer_service": { "enabled": true, "auto_reply": true },
    "order": { "enabled": true, "auto_ship": true }
  },
  "enabled": true
}
```

### 第二步：开启定时任务

技能加载后，创建以下 cron 任务：

| 任务名 | 触发时间 | 作用 |
|--------|---------|------|
| 选品扫描 | 每小时整点 | 分析热销榜单，推荐机会品类 |
| 客服回复 | 每5分钟 | 自动处理买家消息 |
| 订单处理 | 每10分钟 | 自动发货+物流录入 |
| 日报汇总 | 每天23:00 | 推送当日运营数据 |

### 第三步：触发运营

**对话触发示例：**
- 「帮我扫描今天的选品机会」
- 「上架这款商品：[商品链接/信息]」
- 「检查今天的订单」
- 「生成今天运营日报」

---

## 脚本说明

| 脚本 | 功能 | 数据文件 |
|------|------|---------|
| `product_scanner.py` | 扫描热销榜单，生成推荐 | `recommendations.json` |
| `product_publisher.py` | 发布商品到店铺 | `products.json` |
| `customer_service.py` | 自动回复买家 | `customers.json` |
| `order_processor.py` | 处理订单+物流 | `orders.json` |
| `daily_report.py` | 汇总运营数据 | 日志文件 |

---

## 数据目录

`~/.qclaw/solo-ecommerce-data/`

```
solo-ecommerce-data/
├── config.json           # 主配置文件（必填）
├── products.json         # 商品列表
├── orders.json           # 订单记录
├── customers.json        # 客户对话记录
├── recommendations.json  # 选品推荐
└── logs/
    └── YYYY-MM-DD.log    # 每日运行日志
```

---

## 平台接入说明

### 抖音小店
- 使用 Chrome CDP 浏览器自动化
- Chrome 需开启 `--remote-debugging-port=9222`
- 自动化流程：登录 → 商品管理 → 上架/客服/订单

### 其他平台
- 通过平台开放 API（需申请 AppKey/AppSecret）
- 或使用浏览器自动化模拟操作
- 具体接入方式根据平台文档配置

---

## 状态说明

- `enabled: false` → 技能休眠，所有定时任务跳过
- `enabled: true` → 全速运转
- 单个模块关闭 → 仅该模块跳过，其他模块继续

---

> 最后更新：2026-04-26