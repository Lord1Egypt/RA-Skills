# JSON 输入与导出

支持 `--input FILE`（推荐）或兼容环境变量 `TRIP_DATA`；明确指定的文件优先于环境变量。文件/变量最大 1 MiB，不自动读取 `.env`。错误 JSON、错误字段或缺少输入均停止，不回退演示。

`examples/mock-data.json` 是完整可运行示例；其中中文和历史价格只用于展示。真实输入删去 `mock: true`，使用已核实资料或明确写“待核实”。

必填字段：`destination` 非空字符串，`days` 为 1–30 整数，`travelers` 为 1–100 整数。可选 `title`、`subtitle`、`budget`、`preferences`、`tips`、`language`、`mock`。

- 普通文本最多 2000 字符；普通数组最多 100 项。`language` 为 `zh-CN` 或 `en`，默认英文，`--language` 可明确选择界面语言。不会自动翻译用户输入的景点名称或文本。
- `attractions`：`name/type[]/ticketPrice/rating/openingHours/estimatedDuration/description/highlight/reservationRequired/address/_reason`。保留模拟推荐使用的 `_matchScore/_budgetFit/_withinBudget`。
- `itinerary` 最多 30 天，每天包含 `date/items/notes`，每项包含 `time/icon/title/detail/cost`。条目 cost 是显示文本，预算运算使用 costs。
- `hotels`：`name/area/rating/price/features/distance`。
- `transport`：`airport/trainStation/metroNote/tips`。
- `costs`：`total` 与 `items[]`；每项 `name/amount/pct`。数值费用必须非负且有限，最大 1e9；null 表示未知，不会渲染为免费。评分范围 0–5。
- 可选 `platformUrls` 最多 3 个，仅允许 `https://www.tuniu.com/`、`https://m.tuniu.com/`、`https://www.12306.cn/`。二维码直接在本地编码并内嵌，不访问二维码服务器。
- 未知字段（含旧 `costs.paymentUrls`、订单号和乘客字段）会拒绝。请不要把个人资料塞入自由文本。

```bash
node scripts/generate-trip-page.js --input trip.json --language en
node scripts/generate-trip-page.js --mock
node scripts/qrcode.js https://www.tuniu.com/ homepage.png
```

输出固定在本 skill 内的 `output/`，与当前 shell 工作目录无关。行程文件名使用随机 UUID。二维码可选参数只能是 `homepage.png` 一类 PNG 文件名，不接受目录、绝对路径或路径穿越；已存在的文件/符号链接会拒绝覆盖。输出根目录不允许符号链接或 junction。

旧版 `--open` 和二维码任意路径参数已移除。渲染器导出 `getHTML` 为异步函数（需 await），生成二维码也使用异步调用；页面无可执行脚本，并包含禁止脚本/外部资源的 CSP。
