# ClawHub Skill 数据字段说明

> `listPublicPageV4` 返回的每个 Skill 对象结构

## 完整字段

```typescript
interface SkillRecord {
  latestVersion: Version;
  owner: Owner;
  ownerHandle: string;          // 作者 handle (重复字段)
  skill: Skill;                 // 核心数据
}

interface Version {
  _creationTime: number;        // 版本创建时间戳
  _id: string;                  // 版本 ID
  changelog: string;            // 更新日志
  changelogSource: string;      // "user" / "auto"
  createdAt: number;            // 创建时间戳
  skillId: string;              // 关联 Skill ID
  version: string;              // 版本号，如 "3.0.21"
}

interface Owner {
  _creationTime: number;
  _id: string;
  displayName: string;          // 作者显示名
  handle: string;               // 作者 handle
  image: string;                // 头像 URL
  kind: "user" | "org";         // 类型
  linkedUserId?: string;
}

interface Skill {
  _creationTime: number;
  _id: string;                  // Skill 唯一 ID
  badges: object;               // 徽章（多数为空）
  capabilityTags: string[];     // 能力标签，如 ["mcp", "github"]
  createdAt: number;            // 创建时间戳
  displayName: string;          // 显示名，如 "Self-Improving Agent"
  isSuspicious: boolean;        // 是否可疑
  latestVersionId: string;
  ownerPublisherId: string;
  ownerUserId: string;
  slug: string;                 // URL slug，如 "self-improving-agent"
  stats: Stats;                 // ⭐ 统计数据
  summary: string;              // 一句话描述
  tags: object;                 // 标签
}

interface Stats {
  comments: number;             // 评论数
  downloads: number;            // 累计下载
  installsAllTime: number;      // 累计安装
  installsCurrent: number;      // 当前活跃安装
  stars: number;                // ⭐ 星标数
  versions: number;             // 版本数
}
```

## 关键 URL 构造

```python
def get_skill_url(skill, owner):
    """构造 Skill 详情页 URL"""
    return f"https://clawhub.ai/{owner.handle}/{skill.slug}"
```

## 关键指标计算

### 1. star_rate（口碑率）

```python
star_rate = stars / max(downloads, 1) * 100
# 单位：百分比
# 示例：3729 / 456369 * 100 = 0.82%
```

### 2. installsCurrent/installsAllTime（活跃度）

```python
activity_rate = installsCurrent / max(installsAllTime, 1) * 100
# 单位：百分比
# 示例：6347 / 6679 * 100 = 95%
```

### 3. days_since_created（年龄）

```python
import time
now_ms = int(time.time() * 1000)
days = (now_ms - createdAt) / (1000 * 60 * 60 * 24)
```

### 4. version_score（更新活跃度）

```python
# 简单评分：版本数越多越活跃
# 更复杂可结合 changelog 长度、updated 时间
```

## 时间戳转换

Convex 使用毫秒时间戳，需要：

```python
from datetime import datetime
dt = datetime.fromtimestamp(_creationTime / 1000)
```

## 数据清洗建议

| 字段 | 处理 |
|------|------|
| `summary` | 截断到 200 字（飞书消息限制） |
| `capabilityTags` | 去重、转小写 |
| `displayName` | 保留原始大小写 |
| `stats.*` | 整数化（Convex 返回 float） |
| `_id` | 哈希为 URL 安全字符串 |

## 已知字段陷阱

⚠️ **`summary` 字段可能为 HTML 转义字符串**：

```json
"summary": "Use when: (1) A command or operation fails unexpectedly, (2) User corrects Clau..."
```

末尾的 `...` 是真实截断，不是显示省略。

⚠️ **`owner.image` 可能是 `aka.doubaocdn.com` 代理**：

```json
"image": "https://aka.doubaocdn.com/s/3nS91wXFlx"
```

不是 GitHub 头像原 URL，但显示效果一致。

## 完整 Skill 示例

```json
{
  "latestVersion": {
    "_creationTime": 1777649615088,
    "_id": "k97cs17rev4fbbwsh40dwf9jah85x0ws",
    "changelog": "re-upload",
    "changelogSource": "user",
    "createdAt": 1777649615088,
    "skillId": "kd71q6bf0e8vcgdcxfdd3qyd817ynzhk",
    "version": "3.0.21"
  },
  "owner": {
    "_creationTime": 0,
    "_id": "s1794qsnpbjfkfnp0k226sefv583hfzt",
    "displayName": "pskoett",
    "handle": "pskoett",
    "image": "https://avatars.githubusercontent.com/u/177305814?v=4",
    "kind": "user",
    "linkedUserId": "kn70cjr952qdec1nx70zs6wefn7ynq2t"
  },
  "ownerHandle": "pskoett",
  "skill": {
    "_creationTime": 1767632598365,
    "_id": "kd71q6bf0e8vcgdcxfdd3qyd817ynzhk",
    "badges": {},
    "capabilityTags": [],
    "createdAt": 1767632598365,
    "displayName": "Self-Improving Agent",
    "isSuspicious": false,
    "latestVersionId": "k97cs17rev4fbbwsh40dwf9jah85x0ws",
    "ownerPublisherId": "s1794qsnpbjfkfnp0k226sefv583hfzt",
    "ownerUserId": "kn70cjr952qdec1nx70zs6wefn7ynq2t",
    "slug": "self-improving-agent",
    "stats": {
      "comments": 53,
      "downloads": 456369,
      "installsAllTime": 6679,
      "installsCurrent": 6347,
      "stars": 3729,
      "versions": 31
    },
    "summary": "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Clau...",
    "tags": {
      "latest": "k97cs17rev4fbbwsh40dwf9jah85x0ws"
    }
  }
}
```

## 派生数据结构（用于推荐）

```typescript
interface RecommendedSkill {
  rank: number;                 // 推荐排名
  skill_id: string;             // Skill._id
  display_name: string;         // Skill.displayName
  author: string;               // Owner.handle
  url: string;                  // 构造的 URL
  summary: string;              // 截断后的描述
  stars: number;
  downloads: number;
  installsCurrent: number;
  installsAllTime: number;
  comments: number;
  star_rate: number;            // %
  activity_rate: number;        // %
  age_days: number;             // 创建天数
  capability_tags: string[];
  pain_points_matched: string[]; // 命中的痛点场景
  score: number;                // 综合得分
  module: string;               // 来自哪个模块
  recommend_reason: string;     // 推荐理由（中文）
  next_action: string;          // 下一步行动
}
```
