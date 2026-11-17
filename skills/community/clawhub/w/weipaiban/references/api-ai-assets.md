# AI 素材接口

已发布 AI 素材的只读接口。取图用 `scripts/fetch_ai_assets.py`，不要手写分页。本页只在脚本失败或需要核对字段时阅读。

鉴权与发布相同，见 [api-formats.md](api-formats.md)：`Authorization: Bearer <WEIPAIBAN_API_KEY>`。基址 `WEIPAIBAN_API_BASE`，默认 `https://weipaiban.cn`。

成功体是 `{ "data": ... }`。失败体是 `{ "error": { "message": "...", "code": 400 } }`。

## 推荐标签

`GET /api/v1/ai-assets/tags`

```json
{
  "data": {
    "groups": [{ "label": "节日", "tags": ["中秋节"] }],
    "tags": ["中秋节"]
  }
}
```

`groups` 是推荐分组。自定义标签不在此列表里，用户点名后仍可以用下面的列表接口查询。

## 按 tag 列表

`GET /api/v1/ai-assets?tag={tag}&per_page=48&cursor={cursor}`

| 参数       | 说明                                                                                 |
| ---------- | ------------------------------------------------------------------------------------ |
| `tag`      | 必填。一个标签，去空白后 1–32 个字符。服务端按 `tags has tag` 过滤，只返回已发布素材 |
| `per_page` | 脚本固定传 48，这是上限                                                              |
| `cursor`   | 上一页的 `nextCursor`。第一页省略                                                    |

不传 `tag` 会返回全库。本技能禁止这样请求。

```json
{
  "data": {
    "items": [
      {
        "id": "665f1f77bcf86cd799439011",
        "title": "月下庭院",
        "description": "",
        "tags": ["中秋节", "背景"],
        "orientation": "background",
        "transparent": false,
        "width": 1024,
        "height": 3072,
        "url": "https://svg-cdn.creatby.com/ai-assets/a.png",
        "thumb": "https://svg-cdn.creatby.com/ai-assets/a.png_thumb"
      }
    ],
    "perPage": 48,
    "nextCursor": null
  }
}
```

`nextCursor` 非空就要用它请求下一页，直到为 `null`。中途停下就不是这个 tag 的全部素材。

`url` 已是 `svg-cdn.creatby.com` 原图，可直接交给 `build_oss_src.py`。

### `orientation`

`ratio_4x3`、`ratio_3x4`、`ratio_16x9`、`ratio_9x16`、`ratio_2x3`、`ratio_3x2`、`ratio_1x1`、`custom_landscape`、`custom_portrait`、`background`。

`background` 只能由管理员指定，不能从宽高推断。它表示可循环背景。竖图和 `custom_portrait` 不是循环背景。

`transparent: true` 表示已经带透明通道的装饰、贴纸或镂空图。

## 失败

| 状态码 | 处理                                                 |
| ------ | ---------------------------------------------------- |
| 400    | tag 为空、超长或 cursor 非法。修正参数，不要改拉全库 |
| 401    | 请用户到 <https://weipaiban.cn/settings/api-keys> 创建或复制密钥，并更新 `WEIPAIBAN_API_KEY` |
| 403    | 未订阅且不是 developer                               |
| 429    | 脚本会等一次再请求；仍然 429 就停止并稍后重试        |
