# XHS MCP API 文档

## 登录管理

### check_login_status()

检查当前登录状态。

```javascript
const result = await checkLoginStatus();
// 返回: { success: true, logged_in: true, message: "已登录" }
```

### get_login_qrcode()

获取登录二维码（扫码登录）。

```javascript
const result = await getLoginQRCode();
// 返回: { success: true, qrCode: "base64图片数据", expiresIn: 300 }
```

### delete_cookies()

删除登录状态。

```javascript
const result = await deleteCookies();
// 返回: { success: true, message: "Cookies已删除" }
```

---

## 内容获取

### list_feeds()

获取首页推荐。

```javascript
const result = await listFeeds();
// 返回: {
//   success: true,
//   feeds: [
//     {
//       id: "笔记ID",
//       xsec_token: "安全令牌",
//       title: "标题",
//       author: "作者",
//       like_count: "点赞数",
//       cover: "封面图URL"
//     }
//   ]
// }
```

### search_feeds(keyword, filters?)

搜索笔记。

```javascript
const result = await searchFeeds('咖啡', {
  sort_by: '最新',          // 综合 | 最新 | 最多点赞 | 最多评论 | 最多收藏
  note_type: '图文',        // 不限 | 视频 | 图文
  publish_time: '一周内',   // 不限 | 一天内 | 一周内 | 半年内
  search_scope: '不限',     // 不限 | 已看过 | 未看过 | 已关注
  location: '不限'          // 不限 | 同城 | 附近
});
```

### get_feed_detail(feed_id, xsec_token, options?)

获取笔记详情。

```javascript
const result = await getFeedDetail('笔记ID', 'xsec_token', {
  loadAllComments: false,
  limit: 20
});
```

---

## 互动操作

### like_feed(feed_id, xsec_token, unlike?)

点赞/取消点赞。

```javascript
// 点赞
await likeFeed('笔记ID', 'xsec_token', false);

// 取消点赞
await likeFeed('笔记ID', 'xsec_token', true);
```

### favorite_feed(feed_id, xsec_token, unfavorite?)

收藏/取消收藏。

```javascript
// 收藏
await favoriteFeed('笔记ID', 'xsec_token', false);

// 取消收藏
await favoriteFeed('笔记ID', 'xsec_token', true);
```

### post_comment_to_feed(feed_id, xsec_token, content)

发表评论。

```javascript
await postComment('笔记ID', 'xsec_token', '评论内容');
```

### reply_comment_in_feed(feed_id, xsec_token, content, comment_id?, user_id?)

回复评论。

```javascript
await replyComment('笔记ID', 'xsec_token', '回复内容', '评论ID', '用户ID');
```

---

## 用户信息

### user_profile(user_id, xsec_token)

获取用户主页信息。

```javascript
const result = await userProfile('用户ID', 'xsec_token');
// 返回: { success: true, user: { nickname, desc, fansCount, followsCount }, notes: [...] }
```

---

## 内容发布

### publish_content(options)

发布图文笔记。

```javascript
const result = await publishContent({
  title: '标题（最多20字）',
  content: '正文内容（最多1000字）',
  images: ['./photo1.jpg', '/absolute/path/photo2.jpg'],
  tags: ['标签1', '标签2'],
  isOriginal: false,
  visibility: '公开可见'  // 公开可见 | 仅自己可见 | 仅互关好友可见
});
```

### publish_with_video(options)

发布视频笔记。

```javascript
const result = await publishWithVideo({
  title: '标题（最多20字）',
  content: '正文内容（最多1000字）',
  video: './video.mp4',
  tags: ['标签1', '标签2'],
  visibility: '公开可见'
});
```

---

## 性能指标

| 操作 | 平均耗时 |
|------|---------|
| 检查登录状态 | 14秒（首次） |
| 获取首页推荐 | 10.5秒 |
| 搜索笔记 | 5.6秒 |
| 获取笔记详情 | 5.7秒 |
| 点赞/取消点赞 | 4.5-6秒 |
| 收藏/取消收藏 | 4.2-4.8秒 |

---

## 错误处理示例

```javascript
try {
  const result = await searchFeeds('美食');

  if (!result.success) {
    console.error('搜索失败:', result.message);
    return;
  }

  if (result.feeds.length === 0) {
    console.log('无搜索结果');
    return;
  }

  // 处理结果
  console.log(`找到 ${result.feeds.length} 条结果`);

} catch (error) {
  console.error('操作出错:', error.message);
}
```

---

## 批量操作示例

```javascript
const keywords = ['咖啡', '美食', '旅行'];

for (const keyword of keywords) {
  const results = await searchFeeds(keyword);

  if (results.success && results.feeds.length > 0) {
    // 点赞前3条
    for (let i = 0; i < Math.min(3, results.feeds.length); i++) {
      const feed = results.feeds[i];
      await likeFeed(feed.id, feed.xsec_token);
      await new Promise(r => setTimeout(r, 2000)); // 间隔2秒
    }
  }

  await new Promise(r => setTimeout(r, 5000)); // 关键词间隔5秒
}
```
