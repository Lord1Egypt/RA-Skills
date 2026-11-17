# Travel Planner HY 1.3.2

旅行规划、公开景点资料检索、每日行程和预算整理，以及本地 HTML/二维码导出。延续线上 1.3.1 的信息规划范围，不提供预订、订单或支付功能。

需要 Node.js 22+：

```bash
npm ci --ignore-scripts
node scripts/generate-trip-page.js --mock
npm test
```

页面支持中文和英文界面，跟随用户选择。示例使用中文并明确标记模拟数据，不代表实时报价。

安全修复包含：输入 schema 与 HTML 转义、无脚本静态页面及 CSP、平台链接白名单、固定输出目录和独占文件创建、公开攻略域名/DNS/重定向限制、来源提示注入边界。

旧 `paymentUrls` 改为顶层 `platformUrls`，仅支持指定平台公开首页；旧 `--open` 已取消。二维码输出参数仅允许 PNG 文件名。完整命令及输入格式见 [usage.md](references/usage.md)，权限和网络说明见 [SKILL.md](SKILL.md)。

该发布版不需要 API Key，不读取 .env。本地生成不会联网；fetch-guide 会向经过校验的公开网站发送请求。不得将个人行程、密钥或订单信息混入公开查询。
