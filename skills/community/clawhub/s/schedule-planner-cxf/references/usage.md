# 输入与输出

所有命令从技能根目录运行。输入文件由 `--input` 明确指定；单个 JSON 最多 1 MiB。输出使用随机文件名，不覆盖已有文件，不从目的地文本拼接路径。默认目录固定在技能根目录下的 `output/`，不随当前工作目录改变。

## 行程网页

参考 `examples/mock-data.json`。必填：`tripType`、`destination`、`duration`、`segments`、`costs.total`。

- `segments` 最多 100 项，`type` 为 `train`、`flight` 或 `hotel`；交通项需 `departure`、`arrival`，酒店需 `name`。
- 可选文本字段：`segmentNo`、`trainNo`、`flightNo`、`date`、`seat`、`duration`、`address`、`roomType`、`checkIn`、`checkOut`。文本最多 2000 字符；`price`、`nights` 为非负有限数值。
- 可选 `dailyPlan` 数组中每项含 `day`、`title`、`items`。`tips` 为字符串数组，每个数组最多 100 项。
- `costs` 只接受 `total`、`train`、`train1`、`train2`、`flight`、`flightOutbound`、`flightReturn`、`hotel`、`ticket`、`other` 非负数值。费用为参考，不表示已付款或已预订。
- `mock: true` 显示醒目的模拟标签。`language` 为 `zh-CN` 或 `en`；默认英文。
- `platformUrl` 可选，仅接受 SKILL.md 中的三个 HTTPS 公开首页；URL 先校验、再规范化，链接与二维码使用同一结果。
- 未知字段会被拒绝。不要把姓名、证件、电话或其他个人资料放进自由文本。

```bash
node scripts/generate-trip-page.js --input trip.json
node scripts/generate-trip-page.js --input trip.json --desktop
node scripts/qrcode.js https://www.tuniu.com/
```

二维码入口不再接受任意输出路径，仅支持默认 output/ 或 `--desktop`。不生成支付二维码，不自动打开浏览器。HTML 只含内联样式、转义文本和可选本地 data 图片，CSP 禁止脚本和外部资源加载。

## 单次实时查询

`query.json` 示例，日期应改为用户实际日期：

```json
{
  "server": "train",
  "tool": "searchLowestPriceTrain",
  "params": {
    "departureCityName": "杭州",
    "arrivalCityName": "南京",
    "departureDate": "2026-10-01"
  }
}
```

允许的组合：

| server | tool | 参数 |
| --- | --- | --- |
| train | searchLowestPriceTrain | departureCityName, arrivalCityName, departureDate |
| flight | searchLowestPriceFlight | departureCityName, arrivalCityName, departureDate |
| hotel | tuniu_hotel_search | cityName, checkIn, checkOut；可选 keyword, pageNum |

日期必须为真实的 YYYY-MM-DD，退房晚于入住。`pageNum` 为 1–100 的整数。单个查询文本最多 200 字符；拒绝额外字段，包括乘客与订单参数。请在本地进程环境配置 `TUNIU_API_KEY`，不要把密钥写入输入文件。CLI 使用项目内固定 endpoint 配置，不读取用户家目录中的配置或缓存，不进行动态服务发现。鉴权密钥和查询参数会发送至途牛服务。

## 多城市查询

`examples/query-plan.json` 是固定历史日期的离线演示输入。真实查询请另外准备 `plan.json`，填入用户请求的城市与日期。每条 `routes` 项包含 `type/from/to/date`，每条 `hotels` 项包含 `city/checkIn/checkOut`。不会自动替换用户的交通方式。

```bash
node scripts/query-5city-trip.js --mock
node scripts/query-5city-trip.js --input plan.json
node scripts/generate-5city-trip.js --input output/comparison-实际文件名.json
```

查询 JSON 带有 `mock` 布尔标识，网页保留模拟/真实查询的区别。价格缺失标为未知，不应作为免费项目或最低价参与推荐。终端中的文件名才是实际输出路径。
