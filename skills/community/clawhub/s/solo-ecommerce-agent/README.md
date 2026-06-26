# solo-ecommerce-agent

**全平台全自动电商运营智能体** — 一人运营多平台店铺，无需人工干预。

## 功能

| 模块 | 说明 | 自动化 |
|------|------|--------|
| 选品扫描 | 多平台热销榜单分析、机会品类推荐 | 每小时自动扫描 |
| 商品上架 | 商品信息生成、图文处理、一键发布 | 开启后自动上架 |
| 客服回复 | 买家咨询自动分类+回复，争议自动升级 | 每5分钟自动处理 |
| 订单处理 | 自动发货、物流录入、退款审核 | 每10分钟自动处理 |
| 日报汇总 | 每日23:00汇总运营数据推送通知 | 每日自动推送 |

## 支持平台

- 抖音小店（浏览器自动化）
- 淘宝/天猫（API 或浏览器自动化）
- 拼多多（API 或浏览器自动化）
- 京东（API 或浏览器自动化）
- 其他平台（可扩展）

## 安装

```bash
openclaw skill install solo-ecommerce-agent
```

## 配置

编辑 `~/.qclaw/solo-ecommerce-data/config.json`：

```json
{
  "platform": "douyin",
  "store_name": "你的店铺名",
  "automation": {
    "publish": { "enabled": true },
    "customer_service": { "enabled": true },
    "order": { "enabled": true }
  },
  "enabled": true
}
```

## 使用方式

### 对话触发（按需）
- 「帮我扫描今天的选品机会」
- 「上架这款商品：[商品信息]」
- 「检查今天的订单状态」
- 「生成今天运营日报」

### 全自动（定时）
配置 cron 任务后，智能体在后台自动运行：
- 每小时整点：选品扫描
- 每5分钟：客服回复
- 每10分钟：订单处理
- 每天23:00：运营日报

## 数据目录

`~/.qclaw/solo-ecommerce-data/`

```
solo-ecommerce-data/
├── config.json           # 主配置文件
├── products.json         # 商品列表
├── orders.json           # 订单记录
├── customers.json        # 客户对话
├── recommendations.json  # 选品推荐
└── logs/                 # 运行日志
```

## 系统要求

- Python 3.8+
- Chrome 浏览器（平台自动化用）
- OpenClaw 最新版

## License

MIT