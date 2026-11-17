# 提交任务 · submit

> a7w 插件 `happy_horse` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/happy_horse/submit`

## 提交任务

`POST /api/v1/apps/happy_horse/submit`

创建一条视频生成任务，返回平台 `task_id`。
计费为 **定价矩阵（点数/秒）× 目标时长**：矩阵按输出分辨率 × 是否含视频输入分档（与 Seedance 矩阵 JSON 同形；Happy Horse 通常两档填相同点数/秒）。

平台需在应用管理中配置可用的服务地址与密钥；未配置时提交将提示服务未就绪。

### 主要参数

- `resolution`：`720P` 或 `1080P`
- `duration`：目标时长(秒)，文生 / 图生 / 多参考支持 3～15 秒；视频编辑时长由输入视频决定
- `prompt`：文本描述，必填
- `model`：能力代号，决定文生、图生、多参考或视频编辑
- `media`：统一参考素材数组；视频编辑传 1 个 video，可附参考图

### 请求示例
```json
{
  "resolution": "720P",
  "duration": 5,
  "prompt": "都市夜景，车流水灯，中景推进镜头"
}
```

## 参数（平台 schema 原文）

```json
{
  "seed": {
    "type": "number",
    "example": 42,
    "options": "0～2147483647 的整数",
    "required": false,
    "description": "随机种子，用于尽量复现生成效果；不传则随机"
  },
  "media": {
    "type": "array",
    "example": [
      {
        "url": "https://example.com/input.mp4",
        "type": "video"
      },
      {
        "url": "https://example.com/ref1.jpg",
        "type": "image"
      }
    ],
    "children": {
      "url": {
        "type": "string",
        "required": true,
        "description": "素材 URL，需为公网可访问地址"
      },
      "type": {
        "type": "string",
        "options": "image / video",
        "required": false,
        "description": "素材类型；可省略自动推断"
      }
    },
    "required": false,
    "description": "统一参考素材数组。文生不传；单图首帧传 1 张 image；多参考传 1～9 张 image（建议至少 2 张）；视频编辑传 1 个 video，可附 0～5 张 image"
  },
  "model": {
    "type": "string",
    "example": "happyhorse-1.1-t2v",
    "options": "happyhorse-1.1-t2v / happyhorse-1.1-i2v / happyhorse-1.1-r2v / happyhorse-1.0-video-edit",
    "required": true,
    "description": "生成能力代号，决定 media 的使用规则"
  },
  "ratio": {
    "type": "string",
    "example": "16:9",
    "options": "16:9 / 9:16 / 1:1 / 4:3 / 3:4",
    "required": false,
    "description": "画幅比例；文生和多参考可传，单图首帧不需要传"
  },
  "prompt": {
    "type": "string",
    "example": "一只猫在草地上奔跑",
    "required": true,
    "description": "画面、镜头、风格与对白等描述；最多 2500 字，不能为空"
  },
  "duration": {
    "type": "number",
    "example": 5,
    "options": "3～15 的整数",
    "required": true,
    "description": "目标视频时长(秒)，整数；文生、图生、多参考支持 3～15 秒。本平台按该值计费"
  },
  "watermark": {
    "type": "boolean",
    "example": true,
    "options": "true / false",
    "required": false,
    "description": "是否添加水印；不传默认 true"
  },
  "resolution": {
    "type": "string",
    "example": "720P",
    "options": "720P / 1080P",
    "required": true,
    "description": "目标分辨率；支持 720P、1080P（也接受小写，平台会归一）"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
- 分档：`720p`=0.9，`1080p`=1.6
