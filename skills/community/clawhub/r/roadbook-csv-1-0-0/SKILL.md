---
name: roadbook-csv
description: 通过 CSV 格式提交旅行线路数据，自动生成路书分享链接。数据存储在 Redis，支持多日行程、酒店住宿跨天衔接、高德地图可视化。
metadata:
  openclaw:
    requires:
      env:
        - name: CYEAM_API_KEY
          description: Cyeam 开放平台 API Key，用于调用路书生成接口
          required: true
      bins:
        - curl
---

# Roadbook CSV - 旅行线路 CSV 提交工具

通过 CSV 文本提交旅行线路地点数据，自动生成路书分享 ID 和链接，可在高德地图上查看完整行程。

## 使用流程

1. **检查环境变量 `CYEAM_API_KEY`**
   - 如果未设置：提示用户先设置环境变量（见下方「申请 API Key」）
   - 如果已设置：直接整理 CSV 并调用 API

2. **整理 CSV 数据**（5 列，见下方格式说明）
3. **调用 API 生成路书**
4. **返回路书链接和二维码**

## CSV 格式

每行一个地点，逗号分隔，共 5 列：

```
名称,地址,类型,日期,备注
```

| 列 | 说明 | 示例 |
|---|---|---|
| 名称 | 地点名称 | 中国陶瓷琉璃馆 |
| 地址 | 详细地址 | 淄博市张店区华光路320号 |
| 类型 | 景点/餐饮/住宿/起点/其他 | 景点 |
| 日期 | DayX 或 日期 | Day1 / 5.1 |
| 备注 | 行程备注 | 下午 / 早市逛吃 |

### 完整示例

```csv
淄博酒店,淄博市张店区某路,住宿,4.30,入住
八大局便民市场,淄博市张店区共青团东路,餐饮,5.1,早市逛吃
中国陶瓷琉璃馆,淄博市张店区华光路320号,景点,5.1,国家级免费
海岱楼钟书阁,淄博市张店区齐盛湖公园内,景点,5.1,夜景打卡
牧羊村烧烤,淄博市张店区林泽街,餐饮,5.1,晚餐
```

### 日期与备注格式

- `Day1,下午` → 第一天，备注"下午"
- `5.1,早市逛吃` → 5月1日，备注"早市逛吃"
- `Day2,` → 第二天，无备注（备注列留空）

**注意**：如果前一天最后一个地点的类型是"住宿"，系统会自动将其作为第二天的起点展示在地图和行程列表中。

## 调用接口

### 提交 CSV 生成路书

**端点：** `https://cyeam-open-main-d02895c.d2.zuplo.dev/api/roadbook/csv`

**认证：** `Authorization: Bearer $CYEAM_API_KEY`

```bash
curl -X POST "https://cyeam-open-main-d02895c.d2.zuplo.dev/api/roadbook/csv" \
  -H "Authorization: Bearer $CYEAM_API_KEY" \
  -H "Content-Type: text/plain" \
  -d "名称,地址,类型,日期,备注"
```

> **为什么使用这两个域名？** 写入端点（`zuplo.dev`）是 Cyeam 开放平台的 API 网关，负责接收 CSV 数据并生成分享 ID；读取端点（`cyeam.com`）是前端展示页面，用户通过该链接查看地图路书。两者都是 Cyeam 官方服务的一部分。

**返回：**
```json
{
  "id": "bf9186906ec8",
  "url": "https://www.cyeam.com/tool/roadbook?id=bf9186906ec8",
  "text": "https://www.cyeam.com/tool/roadbook?id=bf9186906ec8",
  "qrcode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

| 字段 | 说明 |
|---|---|
| `id` | 分享 ID |
| `url` | 路书页面链接 |
| `text` | 要编码为二维码的文本内容（通常与 url 相同） |
| `qrcode` | Base64 编码的 PNG 二维码图片 |

### 获取已分享的路书数据

**端点：** `https://www.cyeam.com/api/roadbook/get?id={id}`

**无需认证**

```bash
curl -s "https://www.cyeam.com/api/roadbook/get?id=bf9186906ec8"
```

**返回：**
```json
{
  "data": "[{...地点数据JSON数组...}]"
}
```

## 使用场景

### 为用户规划旅行路线

当用户给出旅行计划时，整理成 CSV 格式调用接口：

```
> 用户：帮我规划一个淄博两日游，第一天住淄博酒店，第二天去八大局吃早点，然后参观陶瓷琉璃馆，晚上吃烧烤。

> 助手：（检查 CYEAM_API_KEY 后，整理为 CSV 调用接口）
curl -X POST "https://cyeam-open-main-d02895c.d2.zuplo.dev/api/roadbook/csv" \
  -H "Authorization: Bearer $CYEAM_API_KEY" \
  -H "Content-Type: text/plain" \
  -d "淄博酒店,淄博市张店区华光路,住宿,Day1,入住
八大局便民市场,淄博市张店区共青团东路,餐饮,Day2,早市逛吃
中国陶瓷琉璃馆,淄博市张店区华光路320号,景点,Day2,下午参观
牧羊村烧烤,淄博市张店区林泽街,餐饮,Day2,晚餐"

> 助手：路书已生成，点击链接查看完整行程地图：https://www.cyeam.com/tool/roadbook?id=xxx
```

## 申请 API Key

如环境变量 `CYEAM_API_KEY` 未设置，或调用返回 401，需先申请：

1. 访问 [Cyeam 开放平台](https://cyeam-open-main-d02895c.zuplo.site/api/~endpoints)
2. 点击右上角 **Sign In** 登录/注册
3. 进入 Developer Portal 创建 API Key
4. 设置环境变量：`export CYEAM_API_KEY="YOUR_API_KEY"`

## 注意事项

- 接口接收 `text/plain` 格式的 CSV 文本（不是 multipart/form-data）
- 数据存储在 Redis，默认有效期 30 天
- 返回的链接打开后，前端会自动进行地理编码并在高德地图上展示
- 支持覆盖已有分享（在 URL 中加 `?id=已有ID`）
- 创建端点域名为 `cyeam-open-main-d02895c.d2.zuplo.dev`，读取端点域名为 `www.cyeam.com`，请勿修改
- 如果 API 调用返回非 200 状态码（如 401/403/404/500），向用户报告具体错误信息，不再重试
