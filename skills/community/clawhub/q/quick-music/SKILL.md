---
name: quick-music
description: 轻量快捷的音乐搜索工具。一条命令搜歌、拿播放链接，零依赖即开即用。
---

# Quick Music — 轻量找歌

## 快速使用

```bash
node scripts/quick-music.js "周杰伦"
node scripts/quick-music.js "晴天" --page 2 --limit 5
node scripts/quick-music.js "周杰伦" --play 1
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 第一个参数 | 搜索关键词（歌名/歌手） | 必填 |
| `--page` | 搜索页码 | 1 |
| `--limit` | 每页数量 | 10 |
| `--play` | 获取第 N 首歌的播放链接 | 不获取 |

## 使用流程

1. 先搜索歌曲，会列出歌曲列表（序号、歌名、歌手）
2. 用 `--play N` 获取指定序号歌曲的播放链接

## 示例

```bash
# 搜索周杰伦的歌
node scripts/quick-music.js "周杰伦"

# 获取搜索结果中第 3 首的播放链接
node scripts/quick-music.js "周杰伦" --play 3

# 搜索特定歌曲
node scripts/quick-music.js "晴天"
```
