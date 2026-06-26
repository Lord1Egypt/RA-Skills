---
name: trump-truth-social-tracker
description: 跟踪特朗普 Truth Social 帖子数据。从 CNN 归档 API 获取数据并同步到本地 SQLite 数据库，支持查询、统计和分析。触发场景：(1) 用户要求同步/更新 Truth Social 数据 (2) 查询特朗普帖子内容、互动数据 (3) 分析帖子趋势或统计信息 (4) 用户提到"Truth Social"、"特朗普推文"相关关键词。
---

# Truth Social Tracker

跟踪特朗普在 Truth Social 平台的帖子，数据来源为 CNN 归档 API。

## 数据源

- **URL**: `https://ix.cnn.io/data/truth-social/truth_archive.json`
- **更新频率**: CNN 实时更新
- **字段**: id, created_at, content, url, media, replies_count, reblogs_count, favourites_count

## 数据库

- **路径**: `~/.openclaw/workspace/temp/trump_truth_social.sqlite`
- **表名**: `truth_posts`
- **主键**: id
- **只保存**: 有内容（content 非空）的帖子

### 表结构

```sql
CREATE TABLE truth_posts (
    id TEXT PRIMARY KEY,
    created_at TEXT,
    content TEXT NOT NULL,
    url TEXT,
    replies_count INTEGER,
    reblogs_count INTEGER,
    favourites_count INTEGER,
    media TEXT,
    fetched_at TEXT
);
```

## 使用方法

### 同步数据

```bash
# 全量同步
python3 ~/.openclaw/workspace/skills/trump-truth-social-tracker/scripts/sync_truth_social.py

# 增量同步（最多10条新帖子）
python3 ~/.openclaw/workspace/skills/trump-truth-social-tracker/scripts/sync_truth_social.py --incremental 10 --alert

# 增量同步 + 预警 + 写入 report 文件
python3 ~/.openclaw/workspace/skills/trump-truth-social-tracker/scripts/sync_truth_social.py --incremental 10 --alert --write-report --output-json
```

输出统计信息：总帖子数、时间范围、互动总数。

### 查询数据

```bash
# 使用 sqlite3 查询
sqlite3 ~/.openclaw/workspace/temp/trump_truth_social.sqlite

# 常用查询示例
SELECT content, created_at, favourites_count 
FROM truth_posts 
ORDER BY favourites_count DESC LIMIT 10;

SELECT * FROM truth_posts 
WHERE content LIKE '%Iran%' 
ORDER BY created_at DESC;

SELECT COUNT(*) FROM truth_posts;
```

## 脚本

### scripts/sync_truth_social.py

核心同步脚本，功能：
1. 获取 CNN 归档 JSON
2. Upsert 到 SQLite（INSERT OR REPLACE）
3. 过滤无内容帖子
4. 输出统计信息

**参数**:
- `--db-path`: 自定义数据库路径
- `--json-url`: 自定义数据源 URL
- `--incremental N`: 增量同步，最多 N 条新帖子
- `--alert`: 检测金融市场影响关键词
- `--write-report`: 将预警写入 `reports/trump_truth_social_alerts.md` 文件
- `--output-json`: JSON 格式输出

**示例**:
```bash
# 全量同步
python3 sync_truth_social.py

# 增量同步 + 预警检测
python3 sync_truth_social.py --incremental 10 --alert

# 心跳任务使用（增量 + 预警 + 写入 report）
python3 sync_truth_social.py --incremental 10 --alert --write-report --output-json
```

## 报告文件

预警信息持续追加到：

`~/.openclaw/workspace/reports/trump_truth_social_alerts.md`