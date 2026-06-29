# API 数据字段映射

脚本内部将 Redfox API 原始返回字段映射为统一字段名：

| 脚本输出字段 | API 原始路径 | 说明 |
|-------------|-------------|------|
| `title` | `data.list[].data.description` | 作品标题/描述 |
| `author` | `data.list[].data.nickname` | 作者昵称 |
| `coverUrl` | `data.list[].data.image` | 封面图 |
| `videoUrl` | `data.list[].data.videoUrl` | 作品视频链接 |
| `likeCount` | `data.list[].data.likeNum` | 点赞数（null → 0） |
| `duration` | `data.list[].data.duration` | 视频时长 |
| `publishTime` | `data.list[].data.publishTime` | Unix 时间戳 → `MM-DD HH:MM` |
| `opusId` | `data.list[].data.opusId` | 作品 ID |
| `cookiesBuffer` | `data.cookiesBuffer` | 翻页游标 |
| `offset` | `data.offset` | 偏移量 |
