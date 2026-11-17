# 可信元数据索引

只有来源得到用户信任时才使用元数据索引，例如官方导出或用户自己维护的目录。这个技能不会解密微信数据库。

支持 CSV、JSON 数组或 JSON Lines。每条记录可以包含：

| 字段 | 必需 | 含义 |
| --- | --- | --- |
| `path` | 是 | 已保存文件的绝对路径 |
| `sender` | 否 | 发送人显示名称或稳定标识符 |
| `sent_at` | 否 | 消息时间，建议使用带时区的 ISO 8601 格式 |
| `chat` | 否 | 会话或群聊名称 |
| `source` | 否 | 该记录的数据来源标记 |

CSV 示例：

```csv
path,sender,sent_at,chat,source
D:\xwechat_files\account\msg\file\report.docx,张三,2026-08-18T14:32:00+08:00,项目群,official-export
```

搜索脚本使用不区分大小写的规范化路径进行匹配。匹配成功时，`metadata_status` 设置为 `verified_index_match`；否则元数据保持不可用。任何文件系统时间都不能代替 `sent_at`。
