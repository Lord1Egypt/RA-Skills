# favorite.db 数据库结构

## 表：fav_db_item

存储所有收藏记录。

| 字段 | 类型 | 说明 |
|------|------|------|
| local_id | INTEGER | 主键，收藏记录ID |
| fav_local_type | INTEGER | 收藏类型 |
| status | INTEGER | 状态标记 |
| create_time | INTEGER | 收藏时间（Unix时间戳） |
| source_id | TEXT | 来源用户/公众号 wxid |
| source_type | INTEGER | 来源类型 |
| content | BLOB | 收藏内容（XML格式，可能压缩） |
| WCDB_CT_content | INTEGER | 压缩类型（4=zstd） |

## fav_local_type 类型值

| 值 | 类型 |
|----|------|
| 1 | 文章/链接 |
| 2 | 图片 |
| 3 | 视频 |
| 4 | 文件 |
| 5 | 语音 |
| 6 | 位置 |
| 7 | 名片 |
| 8 | 文本笔记 |

## content XML 结构

文章类型（fav_local_type=1）的 content 示例：

```xml
<favitem>
  <type>1</type>
  <title>文章标题</title>
  <desc>文章摘要</desc>
  <url>https://mp.weixin.qq.com/s/xxx</url>
  <source>公众号名称</source>
  <sourcetype>9</sourcetype>
  <thumburl>封面图URL</thumburl>
</favitem>
```

## 解析代码

```python
import xml.etree.ElementTree as ET

def parse_favorite_content(content_bytes, ct):
    # 解压 zstd
    if ct == 4:
        import zstandard as zstd
        content = zstd.ZstdDecompressor().decompress(content_bytes)
    else:
        content = content_bytes
    
    root = ET.fromstring(content)
    return {
        'type': root.findtext('type'),
        'title': root.findtext('title', ''),
        'desc': root.findtext('desc', ''),
        'url': root.findtext('url', ''),
        'source': root.findtext('source', ''),
    }
```

## 相关表

- `favorite_fts.db` — 全文搜索索引（SQLite FTS）