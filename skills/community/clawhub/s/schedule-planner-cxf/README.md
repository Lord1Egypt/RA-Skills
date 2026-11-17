# schedule-planner-cxf 1.0.13

出行价格查询、比价与本地行程网页。可选生成途牛/12306 公开首页的二维码；不接收乘客身份资料、订单或支付链接，不执行预订与支付。

## 使用

需要 Node.js 22+。

```bash
npm ci --ignore-scripts
node scripts/generate-trip-page.js --mock
npm test
```

真实查询需要用户在本地进程环境设置 `TUNIU_API_KEY`。该密钥用于对途牛 HTTPS 服务鉴权，查询城市和日期也会发送至途牛。缺少配置时实时查询停止；离线演示须显式指定 `--mock`。

默认生成到本 skill 的 `output/`。`--desktop` 只在用户明确要求桌面输出时使用。浏览器自动启动已移除。

完整能力边界见 [SKILL.md](SKILL.md)，参数见 [references/usage.md](references/usage.md)。脚本不自动加载 `.env`。

## 1.0.12 迁移

- 固定 `tuniu-cli@1.0.7`，通过锁文件安装；移除运行时包下载和自定义 CLI 路径。安装脚本被禁用。
- 输入中的 `passenger`、`orderId`、`paymentUrl` 不再支持。需要公开首页快捷入口时使用 `platformUrl`。
- 旧版 `--open`、二维码任意输出路径不再支持。多城市查询要求显式 plan；生成对比页改为读取查询 JSON，不再隐式联网。
- HTML 对所有字符串转义，并校验类型、数量、长度、URL 和输出路径；生成页面使用限制性 CSP。

本地代码约束不能替代宿主沙箱。安全扫描可能继续标记受限的 `child_process` 查询调用；这不等于运行时下载或任意 shell 执行。线上审计结论需在发布新版本后由平台复检。
