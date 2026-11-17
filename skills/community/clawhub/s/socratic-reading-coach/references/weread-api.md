# 微信读书 Agent API 参考

> 本文档从 `server.js` 代理逻辑和前端调用中提取整理，用于扩展或排查问题。
> 所有请求通过本地服务 `/api/weread` 转发到 `https://i.weread.qq.com/api/agent/gateway`。

## 认证方式

- Header: `Authorization: Bearer ${WEREAD_API_KEY}`
- 环境变量：`WEREAD_API_KEY`（在 `~/.zshrc` / `~/.bashrc` 中配置）

## 请求格式

```json
{
  "api_name": "/store/search",
  "skill_version": "1.0.4",
  "...其他参数": "..."
}
```

`skill_version` 由服务端自动注入（取值 `WEREAD_OFFICIAL_SKILL_VERSION`，对应官方 weread-skills 包版本，当前 1.0.4），前端调用时无需传入。
注意：网关校验的是**官方 weread-skills 版本号**，与本 Skill 自身版本（SKILL_VERSION）无关；官方升级后需同步更新 server.js 顶部该常量。

## 接口列表

### 1. 搜索书籍 `/store/search`

搜索微信读书库中的书籍。

**参数：**
| 字段 | 类型 | 说明 |
|---|---|---|
| keyword | string | 搜索关键词（书名/作者） |
| count | number | 返回结果数量，建议 3 |

**返回关键字段：**
```
results[].books[].bookInfo
  ├── bookId      书籍ID（后续接口必需）
  ├── title       书名
  ├── author      作者
  ├── cover       封面图URL
  ├── newRating   评分（×10，如 85 表示 8.5 分）
  └── newRatingCount  评价人数
```

### 2. 获取书籍信息 `/book/info`

获取书籍简介等详细信息。

**参数：**
| 字段 | 类型 | 说明 |
|---|---|---|
| bookId | string | 从搜索结果获取 |

**返回关键字段：**
- `intro`：书籍简介（用于思维导图生成的上下文）

### 3. 获取章节目录 `/book/chapterinfo`

获取全书章节结构。

**参数：**
| 字段 | 类型 | 说明 |
|---|---|---|
| bookId | string | 书籍ID |

**返回关键字段：**
```
chapters[]
  ├── chapterUid   章节唯一ID
  ├── chapterIdx   章节序号
  ├── title        章节标题
  └── level        层级（1=一级标题，2=二级...）
```

### 4. 获取热门划线 `/book/bestbookmarks`

获取全书被划线最多的段落（万人划线）。

**参数：**
| 字段 | 类型 | 说明 |
|---|---|---|
| bookId | string | 书籍ID |
| chapterUid | number | 0 表示获取全书划线 |
| synckey | number | 同步游标，首次传 0 |

**返回关键字段：**
```
items[]
  ├── markText     划线原文
  ├── totalCount   划线人数（热度指标）
  ├── chapterUid   所属章节ID
  └── range         划线在章节中的位置范围

chapters[]
  ├── chapterUid   章节ID
  └── title        章节标题（用于映射划线所属章节）
```

### 5. 获取我的划线 `/book/bookmarklist`（v1.2.0 新增）

获取当前账号在本书内的划线/书签（个人划线）。网关侧自动过滤书签（type=0），主要返回划线段落。

**参数：**
| 字段 | 类型 | 说明 |
|---|---|---|
| bookId | string | 书籍ID |

**返回关键字段：**
```
updated         更新时间戳（可作 synckey 用）
bookmarks[]
  ├── markText     划线原文
  ├── chapterUid   所属章节ID
  ├── type          0=书签 1=划线 2=想法（网关默认过滤非划线）
  └── range         划线在章节中的位置范围
```

> 前端会连带调用 `/review/list/mine` 并**合并**展示，标注类型（划线/想法）。

### 6. 获取我的想法/点评 `/review/list/mine`（v1.2.0 新增）

获取当前账号对本书写过的高亮想法/点评，可为对话补充"我自己的笔记"上下文。

**参数：**
| 字段 | 类型 | 说明 |
|---|---|---|
| bookid | string | 书籍ID（**注意参数名是小写 `bookid`**，与其余接口的 camelCase `bookId` 不同，误传会取不到数据） |
| synckey | number | 同步游标，首次传 0 |
| count | number | 拉取数量 |

**返回关键字段：**
```
reviews[]
  ├── markText     想法引用的原文
  ├── content      想法内容
  ├── chapterUid   所属章节ID
  ├── abstract     引文摘要（部分字段名因接口版本而异，前端按需兼容）
  └── range         引文位置范围
```

> 该接口未被官方 weread-skills 文档明确列出，参数契约以拆包核对 `cdn.weread.qq.com/skills/weread-skills.zip` 及实测为准。

## 本地服务端点

| 端点 | 方法 | 说明 |
|---|---|---|
| `/api/weread` | POST | 微信读书 API 代理，body 为 `{ api_name, ...params }`；仅放行上方 6 个白名单接口 |
| `/api/status` | GET | 服务状态检查，返回 `{ ok, weread, skillVersion }` |
| `/` | GET | 返回前端页面 |

## 服务端白名单（ALLOWED_APIS）

`server.js` 中的白名单同时承担**入参裁剪**（只透传声明字段）与**接口拒绝**（未声明一律 403）两个职责。新增接口时需同时改两处：白名单 + `references/weread-api.md` 文档。

| api_name | 允许透传字段 |
|---|---|
| `/store/search` | keyword, count |
| `/book/info` | bookId |
| `/book/chapterinfo` | bookId |
| `/book/bestbookmarks` | bookId, chapterUid, synckey |
| `/book/bookmarklist` | bookId |
| `/review/list/mine` | bookid（小写）, synckey, count |

## 常见错误

| 现象 | 原因 | 解决 |
|---|---|---|
| `errcode` 非 0 | API Key 无效或过期 | 检查 `WEREAD_API_KEY` |
| 502 Bad Gateway | 无法连接微信读书服务器 | 检查网络连接 |
| 搜索结果为空 | 书名拼写错误或该书未上架 | 换关键词或确认书名 |
| 403 `不允许的接口` | 前端调用了白名单外的 api_name | 若确需该接口，加入 ALLOWED_APIS 并核对官方参数契约 |
| 我的划线/想法为空 | 该书未划线；或 `/review/list/mine` 用了大写 `bookId` | 在微信读书 App 内先划线；检查参数名为小写 `bookid` |
