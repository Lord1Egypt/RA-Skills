# SKILL.md - 社交媒体一键发布助手

## 描述

一键发布内容到多个社交媒体平台（掘金/知乎/微博/小红书），支持定时发布和格式适配。

## 功能

- **多平台发布**：掘金、知乎、微博、小红书
- **格式适配**：自动适配各平台字数限制和格式要求
- **定时发布**：设置发布时间，自动执行
- **发布日志**：记录发布链接和状态

## 使用方法

```bash
# 安装
claw install social-publisher

# 发布到所有平台
claw run social-publisher --content "文章内容" --title "标题"

# 发布到指定平台
claw run social-publisher --platform juejin --content "文章内容"

# 定时发布
claw run social-publisher --content "文章内容" --schedule "2026-03-21 10:00"
```

## 配置

需要在 `~/.openclaw/workspace/config/social-publisher.json` 配置各平台 Cookie：

```json
{
  "juejin": {
    "cookie": "your-juejin-cookie"
  },
  "zhihu": {
    "cookie": "your-zhihu-cookie"
  },
  "weibo": {
    "cookie": "your-weibo-cookie"
  }
}
```

## 注意事项

- Cookie 有效期约 1 年，过期需重新登录获取
- 小红书需要人工验证码，无法完全自动化
- 建议先用测试账号验证发布功能

## 价格

免费（引流到安装服务 ¥99）

## 作者

yang1002378395