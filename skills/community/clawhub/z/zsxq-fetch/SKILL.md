---
name: zsxq-fetch
description: 知识星球帖子抓取助手 — 自动抓取指定星球的最新帖子，支持全部/仅精华两种筛选模式，支持通过帖子链接或 ID 获取单条帖子详情，支持多星球配置。本 Skill 应在用户需要查看、汇总或检索知识星球内容时使用。
user-invocable: true
metadata:
  requires: node (>= 18)
primaryEnv: ZSXQ_TOKEN
---

# 知识星球帖子抓取助手

从指定知识星球抓取最新帖子内容，支持全部帖子与仅精华两种筛选模式，支持通过帖子链接或 ID 查看单条帖子详情，支持多星球配置管理。所有输出使用**中文**。

---

## 认证与环境

### 必需环境变量

```bash
export ZSXQ_TOKEN="你的token值"
```

**执行前必须检查 `$ZSXQ_TOKEN` 是否已设置。**
未设置时提示：
> 请先设置知识星球 Token：`export ZSXQ_TOKEN="your_token"`
> 获取方式：浏览器打开 wx.zsxq.com → 登录 → F12 → Application → Cookies → 复制 `zsxq_access_token` 的值。

### 依赖安装

无第三方依赖，仅需 Node.js >= 18。首次使用运行一次即可：

```bash
bash {baseDir}/install.sh
```

---

## 配置文件

### `{baseDir}/groups.json` — 多星球配置

```json
[
  {
    "group_id": "YOUR_GROUP_ID",
    "name": "星球名称",
    "scope": "digests",
    "max_topics": 20
  }
]
```

字段说明：
- `group_id`：从星球 URL `wx.zsxq.com/group/{group_id}` 获取
- `name`：星球名称（展示用）
- `scope`：`digests`（仅精华）| `all`（全部），推荐 `digests`
- `max_topics`：每个星球最多抓取的帖子数

---

## 数据抓取脚本 `{baseDir}/fetch_topics.js`

提供四个子命令：

### 1. 获取帖子列表

```bash
node {baseDir}/fetch_topics.js topics <group_id> [count] [scope]
```

- `group_id`：星球 ID
- `count`：帖子数，默认 20
- `scope`：`all`（全部）| `digests`（精华），默认 `all`
- 请求间隔 1 秒（翻页限速）
- 帖子正文截取前 5000 字

输出格式（stdout）：

```json
{
  "group_id": "123456",
  "scope": "digests",
  "count": 5,
  "topics": [
    {
      "topic_id": "789",
      "type": "talk",
      "title": "",
      "text": "帖子内容...",
      "create_time": "2026-03-01T10:30:00.000+0800",
      "owner": { "user_id": "111", "name": "作者" },
      "likes_count": 10,
      "comments_count": 5,
      "reading_count": 200,
      "readers_count": 180,
      "digested": true,
      "image_count": 2
    }
  ]
}
```

### 2. 获取精华帖（快捷方式）

```bash
node {baseDir}/fetch_topics.js digests <group_id> [count]
```

等价于 `topics <group_id> [count] digests`。

### 3. 获取指定帖子详情

```bash
node {baseDir}/fetch_topics.js topic <group_id> <topic_id_or_url>
```

支持两种输入形式：
- 纯帖子 ID：`node fetch_topics.js topic 15552545485212 82811454228448260`
- 完整链接：`node fetch_topics.js topic 15552545485212 https://wx.zsxq.com/topic/82811454228448260`

通过翻页帖子列表匹配目标 topic_id，最多搜索最近 300 条，文本截断上限 5000 字。

输出格式（stdout）：

```json
{
  "topic_id": "123456789",
  "type": "talk",
  "title": "",
  "text": "帖子完整内容...",
  "create_time": "2026-03-01T10:30:00.000+0800",
  "owner": { "user_id": "111", "name": "作者" },
  "likes_count": 10,
  "comments_count": 5,
  "reading_count": 200,
  "readers_count": 180,
  "digested": true,
  "image_count": 2,
  "url": "https://wx.zsxq.com/topic/123456789"
}
```

### 4. 列出已加入的星球

```bash
node {baseDir}/fetch_topics.js groups
```

返回当前账号已加入的所有星球信息（group_id、名称、成员数、帖子数等）。

---

## 执行流程

### 场景一：汇总多个星球最新帖子

**步骤 1：检查环境**
- 验证 `$ZSXQ_TOKEN` 已设置
- 读取 `{baseDir}/groups.json`（星球配置）

**步骤 2：抓取帖子**

对 `groups.json` 中每个星球，按配置的 `scope` 和 `max_topics` 执行：

```bash
node {baseDir}/fetch_topics.js topics <group_id> <max_topics> <scope>
```

多个星球依次抓取，间隔 1.5 秒。

**步骤 3：输出摘要**

按星球分组，每条帖子输出：
- 作者、发布时间
- 内容摘要（核心观点 1-2 句）
- 互动数据（阅读 / 点赞 / 评论）
- 帖子链接：`https://wx.zsxq.com/topic/{topic_id}`

### 场景二：查看指定帖子详情

当用户提供帖子链接或 ID 时，直接执行：

```bash
node {baseDir}/fetch_topics.js topic <group_id> <topic_id_or_url>
```

输出帖子完整内容，包括作者、时间、正文、互动数据。

### 场景三：查找可用星球

当用户不确定 `group_id` 时，执行：

```bash
ZSXQ_TOKEN=xxx node {baseDir}/fetch_topics.js groups
```

列出账号已加入的所有星球供用户选择。

---

## 错误处理

| 错误场景 | 检测方式 | 处理 |
|---------|---------|------|
| Token 未设置 | `$ZSXQ_TOKEN` 为空 | 提示用户设置并说明获取方法 |
| Token 过期 | HTTP 401 | 提示重新获取 token |
| 未加入星球 | HTTP 403 | 提示用户需先加入该星球 |
| API 限流 | HTTP 429 | 自动重试（指数退避 2s/4s/8s） |
| 星球不存在 | API 返回 `succeeded=false` | 跳过该星球，报告中标注 |
| 帖子不存在 | API 返回 `succeeded=false` | 返回 `topic_not_found` 错误 |

**原则：部分失败不中断整体流程。** 单个星球失败仍处理其他星球。

---

## 详细 API 参考

如需了解 API 完整参数、响应结构、错误码等，参阅 `{baseDir}/references/api-reference.md`。
