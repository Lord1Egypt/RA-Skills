---
name: weibo-login
description: 登录微博账号的技能。使用浏览器扫码登录微博(weibo.com)，用于保持会话状态以便后续抓取内容或发帖。当用户需要登录微博时使用此技能。
---

# Weibo Login Skill

## 扫码登录（推荐）

使用浏览器打开微博扫码登录：
```
browser(action=open, url="https://weibo.com/login")
```

等待用户扫码确认后，访问以下URL验证登录状态：
```
browser(action=navigate, url="https://weibo.com/u/你的uid/home")
```

## 注意事项
- 微博登录有反爬机制，避免频繁操作
- 建议使用已保存的cookies维持登录状态
- 移动端UA可能更容易登录
