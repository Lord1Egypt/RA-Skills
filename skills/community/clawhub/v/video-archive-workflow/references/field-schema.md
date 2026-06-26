# Field schema

## Sheet field order

Use this order exactly:

1. 视频名称
2. 视频ID
3. 长度(秒)
4. 文件大小(MB)
5. 帧率(fps)
6. 总码率(kbps)
7. 分辨率
8. 本地地址
9. 下载地址
10. 下载完成时间
11. 上传者
12. 上传者标识
13. 上传日期
14. 平台
15. 视频类型
16. 是否包含字幕
17. 标签
18. 简介
19. 容器
20. 备注

## Value rules

- Leave blank fields empty.
- Do not write `(空)` or similar placeholders.
- Use Beijing time implicitly; do not append timezone labels.
- Format upload date as `YYYY-MM-DD`.
- Keep tags as a single space-separated string.
- Keep description blank when it contains only tags or no meaningful text.
- Keep remarks blank unless the user explicitly asks for a remark.

## Platform rules

### YouTube
- `video_type`: `shorts` when the path contains `/shorts/`, otherwise `normal`.
- `video_id`: the native YouTube video id.
- `uploader`: channel display name.
- `uploader_id`: handle such as `@name`.

### Xiaohongshu
- `uploader`: display name.
- `uploader_id`: Xiaohongshu number shown in the profile.
- Parse tags from title/description hashtags and page text when available.
- If uploader is unresolved, stop and ask the user.

### Bilibili
- `video_id`: BV id.
- `uploader`: owner display name.
- `uploader_id`: owner mid or resolved handle if the workflow defines it.
- Parse tags from title, description, and page `tag-link` text.

### X/Twitter
- Use tweet video metadata only when the status actually contains a video.
- If no video exists, do not fill a video row.

## Tag cleaning

### Title/description hashtags
- Extract only real hashtags.
- Ignore URL fragments.
- Remove full-width spaces, newlines, and repeated whitespace.
- Remove extracted tags from the source text before writing it back.
- Keep first-seen order.
- Remove duplicates.
- Output tags as `#tag1 #tag2`.

### Bilibili page tags
- Parse visible tag text from the page, including `tag-link` anchors.
- Use these tags when title/description tags are absent or incomplete.
- Merge with title/description tags by first-seen order.

## Archive rules

- `容器` means the source container reported by metadata.
- If the source is `mp4`, archive to `mkv` with lossless conversion.
- Keep the source file name as `原名_source.mkv`.
- Keep the archived file name based on the original base name.
- If a filename conflict exists, stop and ask the user.
