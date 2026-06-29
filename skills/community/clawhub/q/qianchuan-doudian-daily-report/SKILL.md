# 千川抖店日报一键生成

每天还在手动打开千川后台、复制消耗、GMV、成交、退款、ROI，再一项项粘到飞书表格里？

这个 Skill 可以自动读取巨量千川、抖店相关经营页面的数据，匹配到飞书表格字段，并辅助生成每日经营日报。适合店铺运营、投放优化、直播电商团队做日报、复盘和数据归档。

一次配置后，每天运行一次命令，就能完成数据抓取、表格填写和日报整理。

## 你能省下什么

| 工作 | 手动整理 | 使用 Skill |
| --- | --- | --- |
| 打开后台查数据 | 5-10 分钟 | 自动完成 |
| 复制千川消耗、GMV、退款、ROI | 10-20 分钟 | 自动写入 |
| 检查分页和总计是否漏数 | 5-10 分钟 | 自动识别总计行 |
| 填写飞书日报表格 | 10-20 分钟 | 自动匹配字段 |
| 生成日报留档 | 10 分钟 | 可选自动生成 |

如果你每天都要整理投放和店铺日报，它可以把半小时左右的重复工作压缩到几十秒。

## 核心功能

- 自动打开指定的巨量千川经营数据页面。
- 复用用户已经授权的登录态读取页面数据。
- 自动读取账户数据、页面总计数据和关键经营指标。
- 优先识别 `共N个账户` 这类总计行，避免只抓第一页导致漏数。
- 自动整理千川消耗、GMV、成交金额、退款、ROI 等指标。
- 自动写入飞书表格对应字段。
- 支持按日期更新每日数据，适合固定时间做经营日报。
- 可选生成 CSV 和 Markdown 报表，方便核对和归档。

## 适合谁用

- 每天要填千川、抖店、商城或直播经营日报的运营同学。
- 需要把后台数据同步到飞书表格的投放同学。
- 需要定期复盘 GMV、消耗、退款、ROI 的店铺负责人。
- 想减少手动复制、分页漏数、公式错填的团队。

## 可采集的数据示例

根据页面实际字段，可采集并整理：

- 千川消耗
- GMV
- GSV
- 用户实际支付金额
- 智能优惠券金额
- 平台补贴金额
- 成交订单数
- 成交金额
- 净成交金额
- 退款金额
- 退款率
- ROI
- 店铺日报需要的其他经营指标

## 使用效果

这个 Skill 的重点不是“抓网页”，而是把经营日报里最容易出错的部分自动化：

- 不再逐个复制后台字段。
- 不再因为分页只看第一页而漏数。
- 不再手动找飞书表格对应单元格。
- 不再每天重复做同一份日报。

## 安全边界

- 默认只允许抓取 `https://business.oceanengine.com/...` 下的页面。
- 只读取配置选择器命中的表格内容，不读取整个网页正文。
- 飞书凭证只能通过环境变量提供，不能写入 `config.json`。
- 写入飞书会修改目标表格，运行前必须设置 `CONFIRM_WRITE_FEISHU=1` 作为显式确认。
- 默认不生成本地 CSV 或 Markdown 文件。确需本地留档时，需在 `config.json` 中设置 `generateReports=true`。
- `STORAGE_STATE_BASE64` 只在内存中解析，不会写入磁盘。
- 如果要读取本地 `storage_state.json`，必须在 `config.json` 中设置 `allowLocalStorageState=true`。

## 配置要求

运行前需要准备：

- Node.js 运行环境。
- Playwright 浏览器依赖。
- 用户本人已授权的巨量千川登录态。
- 飞书开放平台应用的 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`。
- 目标飞书表格的 `spreadsheetToken` 和对应工作表 ID。

## 安装依赖

```sh
npm install
npx playwright install chromium
cp config.example.json config.json
```

## 环境变量

Linux 或 macOS：

```sh
FEISHU_APP_ID=your_feishu_app_id
FEISHU_APP_SECRET=your_feishu_app_secret
CONFIRM_WRITE_FEISHU=1
STORAGE_STATE_BASE64=base64_encoded_playwright_storage_state
```

Windows PowerShell：

```powershell
$env:FEISHU_APP_ID="your_feishu_app_id"
$env:FEISHU_APP_SECRET="your_feishu_app_secret"
$env:CONFIRM_WRITE_FEISHU="1"
$env:STORAGE_STATE_BASE64="base64_encoded_playwright_storage_state"
```

## 配置文件

复制 `config.example.json` 为 `config.json`，然后填写：

- `targetUrl`：要抓取的数据页面，必须是 `https://business.oceanengine.com/...`。
- `feishu.spreadsheetToken`：飞书表格 token。
- `feishu.sourceSheetId`：数据源工作表 ID。
- `feishu.summarySheetId`：汇总工作表 ID。
- `feishu.reportSheetId`：日报工作表 ID。
- `feishu.summarySpendRange`：需要写入消耗数据的单元格范围。
- `feishu.reportDateCell`：日报日期单元格。
- `generateReports`：是否生成本地 CSV 和 Markdown 报表，默认 `false`。
- `allowLocalStorageState`：是否允许读取本地 `storage_state.json`，默认 `false`。

## 运行方式

```sh
node index.js
```

运行完成后会输出：

- 抓取到的数据条数。
- 是否生成本地报表。
- 飞书表格写入结果。

## 注意事项

- 不同后台页面的字段名称可能不同，需要根据目标表格字段做映射。
- 如果网页改版，需要重新核对选择器和字段。
- 如果日报模板公式发生变化，需要同步更新配置中的单元格范围。
- 如果登录态过期，需要由用户重新生成 Playwright storage state。
- 不要发布或提交 `storage_state.json`、`config.json`、生成的报表或任何密钥。
