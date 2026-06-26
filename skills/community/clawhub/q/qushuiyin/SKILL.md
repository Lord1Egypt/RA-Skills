---
name: video-download
description: 短视频去水印下载。检测到抖音、快手、小红书、B站、微博、西瓜视频等平台链接时，自动解析并下载无水印视频，直接发送文件给用户。
---

# Video Download Skill

## 触发条件

用户消息中包含以下任意短视频平台链接时，**无需任何触发词，自动执行**：

- 抖音: `v.douyin.com` / `douyin.com`
- 快手: `v.kuaishou.com` / `kuaishou.com`
- 小红书: `xhslink.com` / `xiaohongshu.com`
- B站: `b23.tv` / `bilibili.com`
- 微博: `weibo.com`
- 西瓜视频: `ixigua.com`

## 执行步骤

1. 从消息中提取 URL（正则: `https?://[^\s]+`，匹配上述域名）
2. 运行脚本：
   ```bash
   python3 /root/.openclaw/skills/video-download/scripts/download.py '<url>'
   ```
3. 解析输出：
   - 成功（`SUCCESS:`开头）→ 回复下载链接
   - 失败（`FAIL:`开头）→ 回复错误原因

## 回复格式

成功后：
1. 用 `message` 工具直接发送视频文件（`media` 参数填本地文件路径，`channel` 对应来源频道）
2. 回复文字：✅ 无水印视频已发送

如果发文件失败，则回复下载链接：
> ✅ 无水印视频：http://81.70.156.92:8899/videos/xxx.mp4

失败：
> ❌ 解析失败：<原因>

## 注意事项

- 不需要 Cookie，使用第三方 API 解析
- 文件保存于 `/www/wwwroot/default/videos/`，通过 nginx 8899 端口提供下载
- 支持抖音分享文字（含杂文字），自动提取 URL
