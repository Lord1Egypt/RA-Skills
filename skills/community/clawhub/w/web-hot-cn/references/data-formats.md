# 数据格式参考

## 通用输出格式

每个数据结果包含：

```json
{
  "success": true,
  "label": "数据描述",
  "data": {
    "sj": [],
    "time": "YYYY-MM-DD HH:mm:ss"
  },
  "count": 50
}
```

---

## 热搜数据

**适用平台：** 抖音、微博、百度、B站、快手

```typescript
interface HotItem {
  url: string       // 搜索链接
  label: string     // 标签（如 "热"、"新"）
  word: string      // 热搜关键词
  hot_value: string // 热度值（数字或 🔥）
  img?: string      // 配图（仅百度）
}
```

| 平台 | url 格式 | hot_value | img |
|------|---------|-----------|------|
| 抖音 | `https://douyin.com/root/search/{word}` | 数字 | ❌ |
| 微博 | `https://s.weibo.com/weibo?q={word}` | 数字或 🔥 | ❌ |
| 百度 | 原始链接 | 数字 | ✅ |
| B站 | `https://search.bilibili.com/all?keyword={word}` | 🔥 | ❌ |
| 快手 | `https://www.kuaishou.com/short-video/{id}` | 数字 | ❌ |

---

## 音乐榜数据

```typescript
interface MusicItem {
  geshou: string  // 歌手名
  name: string    // 歌曲名
  hot: string     // 排名 / 热度 / 专辑名
  img?: string    // 封面 URL（部分平台）
}
```

| 平台 | hot 含义 | img |
|------|---------|----|
| QQ音乐 | 排名变化值 | ❌ |
| 网易云 | 专辑名 | ✅ 封面 |
| 酷狗 | 排名序号 | ✅ 链接 |
| 酷我 | 排名序号 | ❌ |

---

## 影视数据

### 电影（猫眼票房）

```typescript
interface MovieItem {
  syts: string     // 上映天数
  pfzb: string     // 票房占比
  name: string     // 电影名
  piaofang: string // 累计票房
}
```

### 电视剧 / 网播 / 综艺

```typescript
interface TVItem {
  pfzb: string     // 频道 / 平台
  name: string     // 名称
  piaofang: string // 收视率 / 热度
}
```

### App Store 应用/游戏

```typescript
interface AppItem {
  img: string      // 图标 URL
  url: string      // App Store 链接
  name: string     // 应用名
  pingfen: string  // 评分（如 "4.8⭐"）
}
```

---

## 报纸数据

```typescript
interface PaperItem {
  page: number       // 版面号
  title: string      // 标题（如 "01版：要闻"）
  pdf_url: string    // PDF 下载地址
  file_name: string  // 下载文件名
  image_url: string  // 高清大图地址（可直接用于 Agent 加载渲染图片）
}
```
