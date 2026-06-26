# telegram-import Skill

将 Telegram 消息从 SQLite 数据库增量导入 LanceDB 向量库。

## 数据源
- **DB**: `D:\chat\telegram_messages.db`
- **表**: `telegram_messages`
- **字段**: id, group_name, group_id, message_id, date, sender_id, sender_name, message, matched_keywords, is_reply, media_type, has_6_digit_number, created_time

## 目标存储
- **LanceDB**: `D:\edata.lance`
- **Checkpoint**: `D:\edata.lance\temp\telegram.ckpt`（pickle 格式，断点续传）

## Schema
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | `telegram:{group_id}:{message_id}` |
| text | string | 消息文本 |
| vector | float[2560] | Qwen3-Embedding-4B 向量 |
| category | string | 固定 `telegram` |
| scope | string | 固定 `shared` |
| importance | float | 固定 `0.5` |
| timestamp | int | 消息时间戳（Unix） |
| metadata | string | JSON：group_name, group_id, message_id, sender_id, sender_name, matched_keywords, is_reply, media_type, has_6_digit_number |

## Embedding
- **LM Studio**: `http://127.0.0.1:1234/v1/embeddings`
- **Model**: `text-embedding-qwen3-embedding-4b`
- **维度**: 2560

## 执行命令
```bash
python.exe "C:\Users\admin\.openclaw\workspace\skills\telegram-import\scripts\chunk_db.py" telegram
```

## 增量逻辑
1. 启动时加载 `telegram.ckpt` 恢复 `seen_keys` 和 `last_idx`
2. 从 `last_idx + 1` 继续扫描 DB
3. 跳过 `seen_keys` 中已存在的 key
4. 过滤空消息（message 为 NULL 或空字符串）
5. 每 500 行保存一次 checkpoint
