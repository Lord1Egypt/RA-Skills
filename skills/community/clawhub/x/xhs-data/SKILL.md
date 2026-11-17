---
name: "xhs-data"
description: "小红书数据采集层：笔记提取/用户主页抓取/搜索/媒体下载，Selenium+API双引擎，自动处理加密参数"
user-invocable: true
metadata:
  openclaw:
    emoji: "📥"
    tags: ["xiaohongshu", "data", "scraping", "crawler", "media"]
---

# XHS Data v2.0 — 小红书数据采集层

## 双引擎架构

| 引擎 | 技术 | 适合 |
|------|------|------|
| 🔌 API引擎 | RedCrack 纯Python逆向 | 搜索/评论/用户信息/关注点赞 |
| 🌐 浏览器引擎 | Selenium/Playwright | 用户主页滚动/单篇提取/媒体下载 |

---

## API 引擎

```bash
pip install aiohttp loguru pycryptodome getuseragent
```

### 搜索笔记
```python
xhs = await create_xhs_session(proxy=None, web_session=None)
res = await xhs.apis.note.search_notes("关键词")
```

### 笔记详情
```python
res = await xhs.apis.note.note_detail(note_id, xsec_token)
```

### 评论
```python
res = await xhs.apis.comments.get_comments(note_id, xsec_token)
```

### 用户信息
```python
res = await xhs.apis.user.get_user_info(user_id)
```

### 笔记元数据提取(URL→JSON)
```bash
python scripts/xiaohongshu_extract.py "<url>" --pretty --output /tmp/note.json
```

---

## 浏览器引擎

### 抓取用户主页
```python
# Selenium + Chrome, 滚动到底部, 提取所有note_id
# 输出: note_ids.txt + note_links.json + note_links.md
```

### 抓取单篇笔记
```python
# 保存 page.html + post_data.json + post.md
```

### 媒体下载
```python
# 自动提取 image(jpg/png/webp) + video(mp4)
# 限制: 每篇≤10图, ≤5视频
```

---

## 存储路径
- 用户主页：`~/disk/xiaohongshu/data/{userId}/`
- 单篇笔记：`~/disk/xiaohongshu/posts/{noteId}/`

---

## 风控处理
- 461错误：降频 + sleep + 换关键词 + 用登录态
- 401/403：web_session过期
- 代理：支持 `proxy="http://127.0.0.1:7890"`

---

## 链接格式
- 笔记：`xiaohongshu.com/explore/<note_id>`
- 用户：`xiaohongshu.com/user/profile/<user_id>`

---

## 安全
- 间隔 ≥2秒, 单用户≤500篇
- 只抓公开内容
- 仅供学习研究
