# Usage

## 当前可执行部分

执行脚本：
- `scripts/run_video_archive.py <url>`

该脚本目前会完成：
- URL 合法性检查
- yt-dlp 元数据探测
- 生成 `站点-视频ID` 主键
- 本地目录/文件查重
- 调用 `scripts/ytfetch.sh` 完成下载或补全
- 探测本地视频分辨率 / 帧率 / 编码 / 码率
- 输出 `record_fields` 结构化 JSON，可直接用于飞书写表

## 当前限制

- 飞书写表建议由 skill 主流程调用 `feishu_bitable_app_table_record` 执行，而不是在脚本里硬编码平台 API
- 上传者显示名目前优先取 yt-dlp 的 channel/uploader 字段；还没有额外爬 uploader 主页做二次修正
- 缩略图与 `info.json (附件)` 的上传仍需后续补接
