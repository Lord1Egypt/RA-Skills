# threads-downloader

自动下载 Threads 视频

---

💡 **Skill / Tool by tangqi**  
🔗 GitHub: https://github.com/tangqi00987

---

## 场景

自媒体创作者需要批量保存 Threads 视频素材进行二次创作，或者保存感兴趣的内容离线观看。

## 使用方法

用户发送 Threads 链接 → 自动解析下载最高清视频 → 保存到指定目录并重命名

## 文件命名规则

- 单条视频：`Threads_Video_{分辨率}_{日期}.mp4`
- 多条视频：`Threads_Video_1_{分辨率}_{日期}.mp4`、`Threads_Video_2_{分辨率}_{日期}.mp4`...

## 示例

用户发送：`https://www.threads.com/@username/post/DVxxx`

→ 下载并保存为：`Threads_Video_1276x720_2026-03-10.mp4`

## 注意事项

- 最高清视频通常是 720p 或 1080p
- 需要在隔离浏览器中操作
- 下载完成后从临时目录复制文件到目标目录

---

<!-- Built by tangqi | GitHub: https://github.com/tangqi00987 -->
