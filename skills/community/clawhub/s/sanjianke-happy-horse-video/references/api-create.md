# 创建任务 · create

> a7w 插件 `happy_horse` 的接口 `create` · 平台官方文档

---

`POST /api/v1/apps/happy_horse/create`

## 创建任务（happyhorse 渠道）

`POST /api/v1/apps/happy_horse/create`

与 `submit` 入参完全一致，但锁死 happyhorse 渠道：内部走 aorizon `/api/v2/tasks` 流水线，
需要在应用配置里填入 `api_secret`（aorizon Bearer token），可选 `extra_config.happyhorse_base_url` 覆盖默认网关。

计费同 submit：**点数/秒 × 目标时长**，矩阵按输出分辨率 × 是否含视频输入分档（独立维护，可与 submit 不同）。

## 参数（平台 schema 原文）

```json
{
  "seed": {
    "type": "number",
    "example": 42,
    "options": "0～2147483647 的整数",
    "required": false,
    "description": "随机种子；happyhorse 渠道暂不透传至上游，保留位以便日后启用"
  },
  "media": {
    "type": "array",
    "example": [
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
        "options": "image",
        "required": false,
        "description": "素材类型；可省略自动推断"
      }
    },
    "required": false,
    "description": "统一参考素材数组。文生不传；图生 / 多参考传 1～9 张 image。happyhorse 渠道仅支持 image 类型"
  },
  "model": {
    "type": "string",
    "example": "happyhorse-1.1-t2v",
    "options": "happyhorse-1.1-t2v / happyhorse-1.1-i2v / happyhorse-1.1-r2v",
    "required": true,
    "description": "生成能力代号；create 接口不支持 video-edit"
  },
  "ratio": {
    "type": "string",
    "example": "16:9",
    "options": "16:9 / 9:16 / 1:1 / 4:3 / 3:4",
    "required": false,
    "description": "画幅比例；文生和多参考可传"
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
    "description": "目标视频时长(秒)，整数；文生 / 图生 / 多参考支持 3～15 秒。本平台按该值计费"
  },
  "watermark": {
    "type": "boolean",
    "example": true,
    "options": "true / false",
    "required": false,
    "description": "是否添加水印；happyhorse 渠道暂不透传至上游，保留位以便日后启用"
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
