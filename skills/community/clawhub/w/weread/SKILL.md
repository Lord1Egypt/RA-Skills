---
name: weread
description: 微信读书（WeRead）数据查询与笔记管理技能。获取书架、搜索书籍、查看阅读进度/时长、获取笔记划线、热门书评、章节信息、随机笔记抽取和批量导出。当用户提到"微信读书"、"WeRead"、"书架"、"读书进度"、"划线"、"笔记"、"书评"、"在读"、"读完"、"阅读时长"、"读书回顾"、"导出笔记"时使用。
---

# 微信读书 Skill

通过微信读书 Web API 获取用户的阅读数据。依赖 Cookie 认证。

## 前置：Cookie 配置

**Cookie 存储路径: `~/.weread/cookie`（纯文本单行）。**

所有 API 命令依赖此文件。Cookie 不存在或过期时，命令会报错并提示重新登录。

### 获取 Cookie（三选一）

**方式 1 — 浏览器自动提取（推荐）：**
1. 用 `browser` 工具打开 `https://weread.qq.com`（profile=openclaw 或 user）
2. 确认已登录（页面显示用户头像/书架）
3. 执行 JavaScript 提取 cookie：`document.cookie`
4. 将结果写入 `~/.weread/cookie`

**方式 2 — 手动粘贴：**
```bash
python3 ~/.openclaw/workspace/skills/weread/scripts/weread_login.py paste
```

**方式 3 — 直接写入：**
用户提供 cookie 字符串后直接写入 `~/.weread/cookie`。

### 验证 Cookie
```bash
python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py verify
```

Cookie 过期时 API 返回 errcode -2012，提示用户重新登录。

## 命令参考

脚本目录: `skills/weread/scripts/`（相对于 workspace）
执行示例使用绝对路径: `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py`

| 命令 | 说明 | 示例 |
|------|------|------|
| `shelf` | 获取书架（书名、作者、进度、阅读时长） | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py shelf` |
| `search <keyword>` | 搜索书架中的书籍（模糊匹配书名/作者） | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py search 心理学` |
| `info <bookId>` | 获取书籍详情（评分、字数、出版信息） | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py info 123456` |
| `progress <bookId>` | 获取阅读进度 | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py progress 123456` |
| `detail <bookId>` | 获取详细阅读信息（时长明细、完成日期） | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py detail 123456` |
| `bookmarks <bookId>` | 获取划线记录 | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py bookmarks 123456` |
| `reviews <bookId>` | 获取我的笔记/想法 | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py reviews 123456` |
| `best-reviews <bookId> [count]` | 获取热门书评 | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py best-reviews 123456 5` |
| `chapters <bookId>` | 获取章节信息 | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py chapters 123456` |
| `verify` | 验证 Cookie 是否有效 | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py verify` |

### 辅助脚本

| 脚本 | 说明 | 示例 |
|------|------|------|
| `random_review.py` | 随机抽取读书笔记（加权，更长更优先） | `python3 ~/.openclaw/workspace/skills/weread/scripts/random_review.py --count 2 --min-length 50` |
| `export_notes.py` | 全量导出笔记到 `~/.weread/` | `python3 ~/.openclaw/workspace/skills/weread/scripts/export_notes.py` |
| `export_notes.py --stats` | 显示笔记统计信息 | `python3 ~/.openclaw/workspace/skills/weread/scripts/export_notes.py --stats` |
| `weread_login.py paste` | 手动粘贴 Cookie 登录 | `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_login.py paste` |

## 典型工作流

### 查看书架概况
```bash
python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py shelf
```
返回所有书籍的 bookId、书名、作者、进度百分比、阅读时长、是否读完。

### 获取某本书的笔记和划线
1. 先搜索获取 bookId：`python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py search 思考快与慢`
2. 用 bookId 获取划线：`python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py bookmarks <bookId>`
3. 用 bookId 获取笔记：`python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py reviews <bookId>`
4. 需要章节信息时：`python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py chapters <bookId>`

### 查看阅读统计
1. `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py shelf` 获取整体阅读时长
2. `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py detail <bookId>` 获取单本详细阅读数据

### 查看热门书评
1. 搜索获取 bookId
2. `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py best-reviews <bookId> 10`

### 随机读书回顾
适用于晨报、日报或任何需要读书笔记回顾的场景：
```bash
python3 ~/.openclaw/workspace/skills/weread/scripts/random_review.py --count 2 --min-length 50 --format text
```
- `--count N`：抽取 N 条笔记（默认 3）
- `--min-length L`：最小字数过滤（默认 20）
- `--format json|text`：输出格式（默认 text）

需要先运行 `export_notes.py` 导出笔记数据。

## 输出格式

所有命令输出 JSON。关键字段：
- `bookId`: 书籍唯一标识（后续命令的入参）
- `progress`: 阅读进度（0-100）
- `readingTime`: 阅读时长（已格式化为 X小时X分钟）
- `finishReading`: 是否已读完
- `markText`: 划线文本
- `content`: 笔记内容

## Cookie 过期处理

当命令报错 "Cookie 已过期" 时：
1. 用浏览器工具打开 `https://weread.qq.com`，确认登录态
2. 提取 `document.cookie` 写入 `~/.weread/cookie`
3. 运行 `python3 ~/.openclaw/workspace/skills/weread/scripts/weread_api.py verify` 确认
