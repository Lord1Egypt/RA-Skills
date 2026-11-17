# 任务目录与续作契约

每件作品使用 `/tmp/weipaiban-{taskId}/`。`taskId` 使用时间戳或标题 slug；所有阶段读写同一目录。

## 目录

```text
/tmp/weipaiban-{taskId}/
├── meta.json
├── design-brief.md
├── design.json
├── asset-request.json
├── asset-pool.json
├── image-progress.json
├── asset-manifest.json
├── upload-result.json
├── work.html
└── images/
```

- `design-brief.md`：给用户确认的创意、叙事、所选 format 的层级关系和交互说明。
- `design.json`：所选 format 的结构化设计；字段由 format 文档定义。
- `asset-request.json`：图片槽位。哪一张图来自素材池，在拉池之后回填。
- `asset-pool.json`：`fetch_ai_assets.py` 写下的该 tag 全部已发布图。
- `image-progress.json`：选图与处理进度。续作时跳过 `uploaded` 与 `placeholder`。
- `asset-manifest.json`：最终 CDN URL。HTML 只能消费这里的 `src`。
- `work.html`：待发布的完整交互 HTML。

## `meta.json`

```json
{
  "taskId": "20260921-river-walk",
  "taskDir": "/tmp/weipaiban-20260921-river-walk",
  "theme": "江岸夜巡",
  "format": "layered-scroll",
  "currentStep": "design-approved",
  "title": "江岸夜巡",
  "workId": null
}
```

`currentStep` 只使用以下值：

1. `format-selected`
2. `design-draft`
3. `design-approved`
4. `assets-processing`
5. `assets-ready`
6. `work-ready`
7. `done`

续作时读取 `meta.json` 和当前阶段产物，从最后一个完整状态继续。不要新建第二个 taskDir，也不要覆盖已经写入 manifest 的 `src`。

## `asset-request.json`

```json
{
  "taskId": "20260921-river-walk",
  "imageSource": "ai-assets",
  "tag": "旅游",
  "theme": "江岸夜巡",
  "styleAnchor": "沉静的木刻版画，纸张颗粒，暖灰与暗红色调",
  "lightingHint": "侧逆光，固定主体与透明叠层轮廓清楚",
  "assets": [
    {
      "assetId": "foreground-landmark",
      "name": "透明前景地标",
      "role": "transparent",
      "usedBy": ["foreground-landmark"],
      "width": 220,
      "height": 220,
      "cropMode": "contain",
      "needsTransparent": true,
      "visual": "古塔正面剪影，完整居中",
      "aiAssetId": ""
    }
  ]
}
```

作品级：

| 字段            | 说明                                                                   |
| --------------- | ---------------------------------------------------------------------- |
| `imageSource`   | `ai-assets`、`user`、`external-skill`、`placeholder`。默认 `ai-assets` |
| `tag`           | `ai-assets` 时必填，只有一个                                           |
| `externalSkill` | `imageSource` 为 `external-skill` 时填写用户点名的技能名               |

槽位：

- `assetId` 是 design、progress、manifest 和 HTML 之间的稳定主键。
- `role` 是 `background`、`transparent` 或 `scene`。分配方式见 [assets.md](assets.md)。
- `width` / `height` 是画布占位。`background` 的高度在选中图之后按原图比例回填。
- `cropMode`：`transparent` 和 `background` 用 `contain`；`scene` 默认 `cover`。
- `repeatable` 只有循环背景可以写 `true`。
- `visual` 只帮助从池里分辨主体，不送进生图接口。
- `userFile` 有值时，该槽位改用用户文件。
- `aiAssetId` 在选中库图后回填。
- logo 和二维码不进入清单。

## `image-progress.json`

每个条目保留 `assetId`、`status`、`aiAssetId` 和错误信息。状态可用 `pending`、`pooled`、`uploaded`、`failed`、`placeholder`。重新运行时跳过 `uploaded` 与 `placeholder`；`pooled` 继续做 OSS。

## `asset-manifest.json`

```json
{
  "taskId": "20260921-river-walk",
  "imageSource": "ai-assets",
  "tag": "旅游",
  "assets": [
    {
      "assetId": "foreground-landmark",
      "status": "uploaded",
      "source": "ai-assets",
      "aiAssetId": "665f1f77bcf86cd799439011",
      "src": "https://svg-cdn.creatby.com/ai-assets/a.png?x-oss-process=image/resize,m_lfit,w_1080,h_1080",
      "originSrc": "https://svg-cdn.creatby.com/ai-assets/a.png",
      "ossProcess": "image/resize,m_lfit,w_1080,h_1080",
      "outputWidth": 1080,
      "outputHeight": 1080,
      "naturalWidth": 2048,
      "naturalHeight": 2048,
      "boxWidth": 220,
      "boxHeight": 220,
      "cropMode": "contain"
    }
  ]
}
```

`source` 是 `ai-assets`、`user`、`external-skill` 或 `placeholder`。占位项使用 dialect 里的稳定 CDN URL。失败项可以无 `src`，但必须 `status=failed`，并在成品摘要中披露。最终 HTML 不得出现生图服务的临时 URL。
