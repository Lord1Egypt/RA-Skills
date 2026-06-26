# Qwen Image API Notes

官方文档：

- https://help.aliyun.com/zh/model-studio/qwen-image-api
- https://help.aliyun.com/zh/model-studio/models

## 约定

- `qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-max` 走同步接口
- `qwen-image-plus`、`qwen-image` 支持异步接口
- 北京与新加坡地域使用不同的 API Key 和 Base URL，不能混用
- 任务和结果链接有效期均为 24 小时

## 同步接口

- `POST /api/v1/services/aigc/multimodal-generation/generation`
- 请求头：`Authorization: Bearer $DASHSCOPE_API_KEY`
- 请求体使用 `input.messages[0].content[0].text`
- 响应通常从 `output.choices[].message.content[].image` 取图像链接

## 异步接口

- `POST /api/v1/services/aigc/text2image/image-synthesis`
- 需要 `X-DashScope-Async: enable`
- 查询任务：`GET /api/v1/tasks/{task_id}`
- 成功后从 `output.results[].url` 取图像链接

## 尺寸

- `qwen-image-2.0-pro` / `qwen-image-2.0`
  - 默认：`2048*2048`
  - 推荐：`2688*1536`、`1536*2688`、`2048*2048`、`2368*1728`、`1728*2368`
  - 张数：`1-6`
- `qwen-image-max` / `qwen-image-plus` / `qwen-image`
  - 默认：`1664*928`
  - 推荐：`1664*928`、`1472*1104`、`1328*1328`、`1104*1472`、`928*1664`
  - 张数：固定 `1`

## 价格

中国内地单价：

- `qwen-image-2.0-pro`：`0.5 元/张`
- `qwen-image-2.0`：`0.2 元/张`
- `qwen-image-max`：`0.5 元/张`
- `qwen-image-plus`：`0.2 元/张`
- `qwen-image`：`0.25 元/张`

国际单价：

- `qwen-image-2.0-pro`：`0.550443 元/张`
- `qwen-image-2.0`：`0.256873 元/张`
- `qwen-image-max`：`0.550443 元/张`
- `qwen-image-plus`：`0.220177 元/张`
- `qwen-image`：`0.256873 元/张`
