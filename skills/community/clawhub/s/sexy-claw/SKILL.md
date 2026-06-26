---
name: sexy-Claw
description: >
  🦞 色😍龙虾 - 根据主人审美偏好，在多个平台（小红书、抖音、YouTube、B站）搜索并推荐颜值博主/视频。
  自动获取用户cookies，学习主人喜好，推送个性化内容。
  
  使用场景：
  - 主人说"找美女/小姐姐/颜值博主"
  - 主人提到特定平台（小红书/抖音/YouTube/B站）
  - 主人给出审美偏好（如"喜欢 habin/leeesovely 这种类型"）
  - 主人要求"推荐类似 XXX 的博主"
  
  触发词：找美女、搜小姐姐、颜值博主、推荐博主、habin、leeesovely、
         小红书美女、抖音美女、B站小姐姐、YouTube美女、色龙虾
---

# 🦞 Sexy-Claw 色😍龙虾

根据主人审美品味，在多个社交平台搜索并推荐颜值博主/视频。

> "让每一次搜索都充满惊喜 😍"

## 工作流程

### 1. 获取主人审美偏好

首次使用时，询问主人：
- 喜欢什么类型？（甜美/御姐/清纯/性感/可爱...）
- 有喜欢的博主吗？（habin/leeesovely/真栗/兔娘...）
- 偏好哪个平台？（小红书/抖音/YouTube/B站）

将偏好保存到 `references/user_preference.json`

### 2. 获取平台 Cookies

如果主人未提供 cookies，引导主人获取：

**小红书**：
```
1. 登录 https://www.xiaohongshu.com
2. F12 → Application → Cookies
3. 复制 web_session, a1 等关键字段
```

**抖音**：
```
1. 登录 https://www.douyin.com
2. F12 → Application → Cookies
3. 复制 sessionid, ttwid 等关键字段
```

**B站**：
```
1. 登录 https://www.bilibili.com
2. F12 → Application → Cookies
3. 复制 SESSDATA, bili_jct 等关键字段
```

**YouTube**：
- 通常不需要 cookies，直接搜索即可

将 cookies 保存到 `references/platform_cookies.json`

### 3. 搜索推荐

根据主人偏好，在对应平台搜索：

```bash
# 小红书
python3 scripts/xhs_search.py "关键词" 10

# 抖音
python3 scripts/douyin_search.py "关键词" 10

# B站
python3 scripts/bilibili_search.py "关键词" 10

# YouTube
yt-dlp --dump-json "ytsearch5:关键词"
```

### 4. 打开视频

将搜索结果按播放量/点赞排序，打开前3-5个最热门的视频：

```bash
open "视频链接"
```

## 平台支持

| 平台 | 状态 | 需要的 Cookies |
|------|------|----------------|
| 小红书 | ✅ | web_session, a1 |
| 抖音 | ✅ | sessionid, ttwid |
| B站 | ✅ | SESSDATA, bili_jct |
| YouTube | ✅ | 无需 |

## 脚本使用

### 搜索小红书
```bash
python3 scripts/xhs_search.py "颜值 美女" 10
```

### 搜索抖音
```bash
python3 scripts/douyin_search.py "美女" 10
```

### 搜索B站
```bash
python3 scripts/bilibili_search.py "真栗" 10
```

### 获取用户视频
```bash
python3 scripts/bilibili_search.py user 129641517 5
```

## 主人偏好记录

保存在 `references/user_preference.json`：

```json
{
  "preferred_type": ["御姐", "甜美"],
  "favorite_creators": ["habin", "leeesovely", "真栗"],
  "preferred_platforms": ["抖音", "B站"],
  "last_search": "2024-01-01",
  "search_history": []
}
```

## Cookies 记录

保存在 `references/platform_cookies.json`：

```json
{
  "xiaohongshu": {
    "web_session": "xxx",
    "a1": "xxx"
  },
  "douyin": {
    "sessionid": "xxx",
    "ttwid": "xxx"
  },
  "bilibili": {
    "SESSDATA": "xxx",
    "bili_jct": "xxx"
  }
}
```

## 注意事项

1. **隐私保护**：cookies 只保存在本地，不上传
2. **定期更新**：cookies 会过期，需要定期重新获取
3. **频率控制**：避免频繁搜索，防止触发平台风控
4. **主人确认**：首次使用需主人明确同意保存偏好和cookies

---

🦞 **色龙虾，让美好触手可及** 😍
