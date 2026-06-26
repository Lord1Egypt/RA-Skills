# Z视介 API Notes

## Source

This file is derived from:

- The creator-platform QR login page flow at `https://mp.cztv.com/#/login`
- `/Users/jielihaofeng/Downloads/发布图文.html`
- `/Users/jielihaofeng/Downloads/发布短视频.html`
- `/Users/jielihaofeng/Downloads/编辑图文.html`
- `/Users/jielihaofeng/Downloads/编辑短视频.html`

## QR Login

- User-facing entry: `https://mp.cztv.com/#/login`
- Internal API base URL: `https://mp.cztv.com`
- Step 1, get QR token:
  - Method: `GET`
  - Path: `/userCenter/api/uc/pc/getQrcode`
  - Response sample:

```json
{
  "code": "200",
  "data": {
    "qrCode": "d6tuukn4sv672gfa417grr"
  },
  "msg": "操作成功"
}
```

- Step 2, build the share payload rendered into the QR code:

```json
{
  "type": "login",
  "platForm": "base64(创作者平台)",
  "code": "qrCode"
}
```

- Runtime QR link:
  - `https://zmtv.cztv.com/cmsh5-share/prod/download/index.html?nbtvscaninfo=` + `base64(JSON.stringify(payload))`
- Step 3, poll scan result:
  - Method: `POST`
  - Path: `/userCenter/api/h5/uc/auth/CodeLoginInfo`
  - Body:

```json
{
  "qrCode": "上一步返回的 qrCode",
  "ts": "当前毫秒时间戳字符串",
  "sign": "sha256(929AFCDD22F0F7AE54F511278BE6FF18 + ts + qrCode)"
}
```

- Poll result rules:
  - `code=3030`: 等待扫描
  - `code=3032`: 扫码成功但仍处于确认中，继续轮询
  - `code=200`: 扫码成功
- Frontend behavior note:
  - 官方页面只在 `code=200` 时结束登录
  - 其他状态不会立刻报错，而是继续轮询
- Success extraction rule:
  - Read `data.data.sessionId`
  - If the server also returns cookies, prefer that `sessionId` value only as a fallback
- Local persistence rule:
  - Save the resulting `sessionId` to the session file
  - Subsequent publish and edit calls reuse `Cookie: sessionId=...`
- Artifact rule:
  - The CLI emits both an HTML QR page and a PNG QR image before polling
  - `sessionId` is only persisted after the poll response returns success

## Publish Article

- Method: `POST`
- Path from HTML: `/dasugc/v1/api/v1/article/addShortArticle`
- HTML preview URL: `{{ugcHost-test}}/dasugc/v1/api/v1/article/addShortArticle`
- Session rule: the request header must include `sessionId`; the aggregation layer uses it to resolve `userId`
- Skill runtime note: this skill fixes `source` to `openclaw` when sending the request.
- Body shape:

```json
{
  "source": "文章来源（调用方保证唯一）",
  "section": "文章板块",
  "title": "动态内容",
  "img_array": [
    {
      "pic": "图片地址",
      "height": "图片高度",
      "wide": "图片宽度"
    }
  ],
  "topic": [
    {
      "topic_id": "话题ID",
      "topic_title": "话题内容"
    }
  ],
  "activity_id": "活动ID",
  "position": "位置信息",
  "at_info": [
    {
      "uid": "用户ID",
      "uname": "用户名"
    }
  ],
  "tags": "标签",
  "description": "描述"
}
```

- Response note: the HTML response example shows `data.ugc.shortArticle.data.article_id`.

## Edit Article

- Method: `POST`
- URL in HTML: `http://zugcpublish.cztv.com/dasugc/v1/api/v1/article/editShortArticle`
- Session rule: same `sessionId` header requirement
- Skill runtime note: this skill fixes `source` to `openclaw` when sending the request.
- Documentation note:
  - The plain-text intro in the exported HTML still shows an `img_array`-based example.
  - The structured request-parameter section shows a newer schema centered on `cover_img` and `content`.
  - In real testing, sending only `img_array` can return success without actually updating the cover image.
  - Prefer sending `cover_img`, and keep `img_array` only as a compatibility field if needed.
- Body shape:

```json
{
  "article_id": "动态图文ID（文章ID）",
  "source": "文章来源（调用方保证唯一）",
  "title": "动态内容",
  "content": "内容",
  "description": "描述",
  "cover_img": "封面图",
  "topic": [
    {
      "topic_id": "话题ID",
      "topic_title": "话题内容"
    }
  ],
  "at_info": [
    {
      "uid": "用户ID",
      "uname": "用户名"
    }
  ],
  "release_scope": "OPEN",
  "release_included": null,
  "release_excluded": null,
  "background_image": "",
  "location": {
    "address": "简要地址信息",
    "country": "国家",
    "city": "城市",
    "province": "省份",
    "lon": "经度",
    "lat": "纬度"
  },
  "collection_id": "",
  "ai_generated": 0
}
```

- Response note: the HTML response example also resolves to `data.ugc.shortArticle.data.article_id`.

## Publish Video

- Method: `POST`
- Path from HTML: `/dasugc/v1/api/v1/article/addVideo`
- HTML preview URL: `{{ugcHost-test}}/dasugc/v1/api/v1/article/addVideo`
- Session rule: the request header must include `sessionId`; the aggregation layer uses it to resolve `userId`
- Skill runtime note: this skill fixes `source` to `openclaw` when sending the request.
- Body shape:

```json
{
  "source": "文章来源（调用方保证唯一）",
  "section": "文章板块",
  "uuid": "用户ID",
  "title": "标题",
  "cover_img": "封面图",
  "width": "视频宽度",
  "height": "视频高度",
  "video_url": "视频地址",
  "play_time": [
    "时",
    "分",
    "秒"
  ],
  "type": 3,
  "topic": [
    {
      "topic_id": "话题ID",
      "topic_title": "话题名称"
    }
  ],
  "activity_id": "活动ID",
  "position": "位置信息",
  "at_info": [
    {
      "uid": "用户ID",
      "uname": "用户名"
    }
  ],
  "tags": "标签",
  "description": "描述",
  "tribe_info": [
    {
      "tribeId": "部落ID",
      "tribeName": "部落名称"
    }
  ]
}
```

- Type note from HTML: supports `type=3` 视频, `type=4` 动态小视频, `type=7` 动态短视频.
- Response note: the HTML response example shows `data.ugc.video.data.article_id`.

## Edit Video

- Method: `POST`
- Path from HTML: `/dasugc/v1/api/v1/article/editVideo`
- HTML preview URL: `{{ugcHost-test}}/dasugc/v1/api/v1/article/editVideo`
- Session rule: same `sessionId` header requirement
- Skill runtime note: this skill fixes `source` to `openclaw` when sending the request.
- Body shape:

```json
{
  "article_id": "视频ID",
  "source": "文章来源（调用方保证唯一）",
  "section": "文章板块",
  "uuid": "用户ID",
  "title": "标题",
  "cover_img": "封面图",
  "width": "视频宽度",
  "height": "视频高度",
  "video_url": "视频地址",
  "play_time": [
    "时",
    "分",
    "秒"
  ],
  "type": 3,
  "topic": [
    {
      "topic_id": "话题ID",
      "topic_title": "话题内容"
    }
  ],
  "activity_id": "活动ID",
  "position": "位置信息",
  "at_info": [
    {
      "uid": "用户ID",
      "uname": "用户名"
    }
  ],
  "tags": "标签",
  "description": "描述"
}
```

## Host Note

The bundled config defaults the publish and edit host to `http://zugcpublish.cztv.com`.

This is an inference from the HTML docs:

- `编辑图文.html` exported an absolute URL on that host
- The other three HTML files showed `{{ugcHost-test}}/...`

Override the host with `--base-url` if your runtime environment uses another domain.
