# 离线演示

完成 `npm ci --ignore-scripts` 后运行：

```bash
node scripts/generate-trip-page.js --mock
node scripts/query-5city-trip.js --mock
```

不需要 API Key，不联系途牛。示例日期、班次、酒店及价格均为模拟数据，不可用于实际购票决策。结果写入 skill 的 output/，网页显示模拟标签。

`mock-data.json` 演示行程输入结构，`query-plan.json` 演示多城市查询输入结构。两者都不包含乘客身份、订单号或支付地址。可选二维码只打开公开平台首页。

未提供 `--mock` 时，真实查询缺少凭据或失败会停止，不自动变成演示结果。
