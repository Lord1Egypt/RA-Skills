# HTTP 接口和 Python 脚本

## 运行配置

```text
CHART_RENDER_BASE_URL              默认：https://chart.cqccjy.cn
CHART_RENDER_API_KEY               可选；有值时作为 X-API-Key 发送
CHART_RENDER_HTTP_TIMEOUT_SECONDS  默认：15 秒
```

命令行参数会覆盖环境变量。脚本只使用 Python 标准库，可从任意工作目录运行。

## 接口对应关系

| 用途 | 方法 | 接口 | Python 脚本 |
| --- | --- | --- | --- |
| 健康检查 | `GET` | `/health` | 可手动调用 |
| 渲染器就绪 | `GET` | `/readiness` | 可手动调用 |
| 当前 V2 能力摘要 | `GET` | `/v2/contracts` | `get_capabilities.py` |
| 完整 Schema、默认值、示例 | `GET` | `/v2/contracts` | `get_capabilities.py --full` |
| 实际色系 ID | `GET` | `/v1/themes` | `get_themes.py` |
| 图形目录和参考图 | `GET` | `/v2/catalog` | `get_reference_images.py` |
| 单图 Schema、示例、参考图 | `GET` | `/v2/catalog` | `get_graphic_contract.py <id>` |
| PNG | `POST` | `/v2/render/png` | `render_graphic.py --format png` |
| SVG | `POST` | `/v2/render/svg` | `render_graphic.py --format svg` |

## 鉴权

服务开启 API Key 后，使用 `X-API-Key` 或 `Authorization: Bearer ...`。脚本发送 `X-API-Key`。鉴权失败时报告错误，不要换接口或删除 API Key。

## 查询命令

```bash
python3 scripts/get_capabilities.py
python3 scripts/get_capabilities.py --full --output contract.json
python3 scripts/get_themes.py
python3 scripts/get_reference_images.py --kind smartart --output-dir references/smartart
python3 scripts/get_graphic_contract.py smartart.cycle --preview-output references/smartart.cycle.svg
```

不带 `--id` 的参考图脚本会输出精简目录，不把大量 Base64 data URL 打进上下文；使用 `--output-dir` 会把参考图保存为本地 SVG。单图契约脚本返回精确的 `parameters` 和 `exampleRequest`。

## 渲染命令

```bash
python3 scripts/render_graphic.py request.json --format png --output output/graphic.png --metadata-output output/graphic.metadata.json
python3 scripts/render_graphic.py request.json --format svg --output output/graphic.svg
cat request.json | python3 scripts/render_graphic.py - --format png --output output/graphic.png
```

请求 JSON 会原样发送，脚本不会偷偷补充 `theme`。服务返回的二进制图片会原样保存，metadata 会记录哈希、像素尺寸、逻辑尺寸、页面、渲染器和推荐显示尺寸。

## 重要响应头

常用响应头包括 `X-Render-Kind`、`X-Render-Variant`、`X-Image-Width`、`X-Image-Height`、`X-Layout-Width`、`X-Layout-Height`、`X-Raster-Scale`、`X-Display-Width-Mm`、`X-Display-Height-Mm`、`X-Document-Page-Preset`、`X-Document-Page-Selection` 和 `X-Document-Page-Fallback`。

插入 Word 时使用 `X-Display-Width-Mm`，不能把 PNG 像素宽度当成毫米。

## 错误处理

- `400`：JSON、类型、未知字段或枚举错误。
- `401`：API Key 缺失或错误。
- `422`：语义数据、关系、数量限制或布局错误。
- `500`：服务端渲染错误。

遇到 `400` 或 `422`，读取响应 JSON，按错误路径对照单图 Schema 修复一次后重试。版面溢出先省略 `page`，再考虑横版或拆图；不能静默删数据或缩小文字。
