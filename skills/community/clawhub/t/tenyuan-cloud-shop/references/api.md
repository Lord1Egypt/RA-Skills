# 后端 API 契约 — ruancy-cloud-market v0.3.2

Base URL：`https://ruancyai.com/cloud`（本地开发为 `http://localhost:8787/cloud`）

所有响应均为 JSON。创建档口为 multipart 上传，其余为普通 JSON。

## 1. 创建云铺档口

```
POST /cloud/api/shops
Content-Type: multipart/form-data
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `description` | string | 是 | 用户的一句话描述，如「云南高山沃柑 5 斤 29.9 包邮，电话138xxxx」 |
| `images` | file[] | 否 | 产品照片，最多 3 张，字段名固定 `images` |

成功响应 `200`：

```json
{
  "ok": true,
  "shopId": "s-xxxxxxxx",
  "shop": {
    "name": "AI 起的店名",
    "slogan": "标语",
    "phone": "从描述中抽取的电话（可能为空）",
    "wechat": "从描述中抽取的微信号（可能为空）"
  },
  "shareText": "可直接发朋友圈的文案",
  "pageUrl": "https://ruancyai.com/cloud/shop/s-xxxxxxxx",
  "voiceScript": "口播文案",
  "audioUrl": "https://ruancyai.com/cloud/uploads/voice-xxx.mp3（服务端已配 TTS key 时才有）"
}
```

说明：
- 未配 `OPENAI_API_KEY` 时 `audioUrl` 为 `null`，页面自动降级为只显示口播文案。
- 未配视觉/抽取模型 key 时后端可能返回 503，此时如实告知用户服务暂不可用，**不要本地编造档口数据**。
- 返回中的 `pageUrl` / `audioUrl` 均为绝对地址（后端按 `PUBLIC_BASE_URL` 拼接，库内只存相对路径，换域名自动跟随）。

## 2. 上传店主微信二维码

```
POST /cloud/api/shops/{shopId}/qrcode
Content-Type: multipart/form-data
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `qrcode` | file | 是 | 二维码图片，字段名固定 `qrcode` |

成功响应 `200`：`{ "ok": true, "shopId": "...", "qrCodeUrl": "绝对地址" }`

上传后档口页「联系老板」卡片自动渲染二维码（长按识别）。

## 3. 获取分享素材

```
GET /cloud/api/shops/{shopId}/share
```

成功响应 `200`：

```json
{
  "ok": true,
  "shopId": "s-xxxxxxxx",
  "pageUrl": "https://ruancyai.com/cloud/shop/s-xxxxxxxx",
  "shareText": "分享文案（已自动附带档口链接）"
}
```

## 4. 档口页（浏览器访问）

```
GET /cloud/shop/{shopId}
```

返回完整 HTML 档口页：产品卡、口播音频、分享链接区、联系老板（电话/微信/二维码）、返回云市场页脚。

## 错误形态

| 状态码 | 含义 | Agent 应对 |
|---|---|---|
| 400 | 描述缺失或图片超限 | 检查后重试一次，仍失败则向用户澄清 |
| 413 | 图片超过大小限制（服务端 10MB） | 请用户换小图 |
| 503 | AI 服务未配置/不可用 | 如实告知「云铺服务暂不可用」，不得编造结果 |
| 5xx 其他 | 服务端异常 | 告知稍后再试 |

## 部署状态口径

- 后端部署目标：新加坡 1 号机 47.236.166.4，反代挂 `ruancyai.com/cloud`。
- **本 Skill 提交上架前，后端必须已上线并通过验收清单**（见工程 DEPLOY.md），否则商店用户首次使用即失败。
