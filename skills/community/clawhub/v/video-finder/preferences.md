---
name: video_finder_preferences
description: "管理用户的影片偏好配置。首次使用初始化偏好问答、偏好修改、正负面标签和作者维护。触发：改偏好、记喜好、偏好设置、preferences"
---

# preferences — 偏好管理

管理用户的内容偏好配置文件 `preferences.json`。

## 前置条件

- **称呼约定**：`{{{user}}}` 为占位符
- **配置文件**：`./preferences.json`（skill 根目录）

## 初始化流程

### 首次使用

**触发条件**：`preferences.json` 不存在

**操作**：

1. 从模板创建：`cp preferences.example.json preferences.json`
2. 向用户逐一提问，覆盖模板默认值

```
{{{user}}}，这是你第一次用找片功能～我先记一下你的偏好：

1️⃣ 偏好类型：（例：欧美 amateur / JAV / 国产 / 不限）
2️⃣ 画质要求：（例：1080p / 4K / 不限）
3️⃣ 片长下限：（例：5分钟 / 10分钟 / 不限）
4️⃣ 排除标签：（例：黑皮、男同、复古、猎奇）
5️⃣ 首选站点：（例：XVideos / Eporner / Pornhub）
```

**写入** → `preferences.json`

```json
{
  "schema_version": 2,
  "source_type": "<类型>",
  "quality_min": "<画质>",
  "duration_min_seconds": <秒数>,
  "exclude_tags": ["<标签>", ...],
  "preferred_sites": ["<站点>", ...],
  "site_priority": ["<站点>", ...],
  "download_dir": "",
  "plot_tags": false,
  "tag_weights": {},
  "author_weights": {}
}
```

**同时**：创建 `history.md`，写入初始表头。

### 后续使用

直接读取 `preferences.json`，跳过初始化。

## 修改偏好

### 全量重置

用户说"改偏好" / "重新设置" → 重新跑初始化流程，覆盖整个 `preferences.json`。

### 部分更新

用户说具体要改什么 → 只改对应字段，不动其他：

```
"不喜欢 milf 了"       → 从 exclude_tags 删除 "milf"
"加个 tag：outdoor"    → tag_weights["outdoor"] = 初始权重 1
"画质改成 4K"          → quality_min = "4K"
"下载目录改成 /data"   → download_dir = "/data"
"排除 tattoo"          → exclude_tags 追加 "tattoo"
```

## 偏好字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `source_type` | string | 偏好类型（欧美 amateur / JAV / 国产 / 不限） |
| `quality_min` | string | 最低画质（1080p / 4K / 不限） |
| `duration_min_seconds` | number | 片长下限（秒） |
| `exclude_tags` | string[] | 硬排除标签（不受权重影响，永远排除） |
| `preferred_sites` | string[] | 首选站点 |
| `site_priority` | string[] | 站点优先级排序 |
| `download_dir` | string | 下载目录，空字符串=自动沿用上次 |
| `plot_tags` | boolean | 是否搜索剧情标签 |
| `tag_weights` | object | 标签权重表 `{"tag": weight}`，反馈闭环维护 |
| `author_weights` | object | 作者权重表 `{"author": weight}`，反馈闭环维护 |
| `schema_version` | number | schema 版本号，当前 = 2，用于迁移兼容 |

### tag_weights 示例

```json
{
  "tag_weights": {
    "amateur": 12,
    "homemade": 10,
    "natural tits": 8,
    "euro": 7,
    "blonde": 6,
    "young": 5
  },
  "author_weights": {
    "CreatorName": 4,
    "AuthorName": 2
  }
}
```

- 权重 ≥ 3 → 注入搜索查询做正向加权
- 权重 ≤ 0 → 等同硬排除，自动删除
- 每次搜索会话结束：被动增益 +1（命中标签）、全局衰减 -1（全部标签）
- 新标签首次出现 → 初始权重 1

## 用户干预

```
"改下偏好" → 重新初始化，覆盖 preferences.json
```
