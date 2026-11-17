---
name: website-content
description: 通过开放 API 向客户的线上官网写入内容(文章/产品/案例)。注意:写入即时生效、对外公开可见,且没有删除接口。用于「给官网发一篇文章」「上架一个产品」「加一个客户案例」这类任务。执行写操作前必须先与用户确认目标站点和内容。触发词:官网发布/发文章/上架产品/加案例/更新官网内容。
---

# 官网内容 API

> ## ⚠️ 写操作前必读
>
> **写接口直接落到线上，对外公开可见，而且没有删除接口。**
>
> - 内容提交后立即生效 —— 官网是 SSR 实时读取，不走"构建 → 发布"流程，没有缓冲期
> - 写错了**删不掉**。只能改成草稿/隐藏让它从官网消失，或者让客户去后台处理
> - 因此：**动手前先跟用户确认目标站点和要发的内容**，确认后再调接口
> - 内容还没定稿时，先发草稿态：文章 `is_draft: 1`、产品 `is_hidden: 1`。
>   **案例没有草稿开关**，只能直接发或发完再改
> - 一次提交多个语言时逐条检查 —— 失败的语言不影响其他语言，`results[]` 里逐条看

## 一、准备

| 环境变量 | 说明 |
|---|---|
| `WEBSITE_API_BASE` | 接口基址，如 `https://my.xtocn.com/api` |
| `WEBSITE_API_TOKEN` | 读写 Token。客户后台「官网设置 → Token 管理」生成，**权限必须选「读写」** |

`WEBSITE_API_TOKEN` 是**读写凭据**，能改客户线上的公开内容。不要把它打印到日志、
写进文件或贴进对话；怀疑泄露就让客户在后台停用并重新生成。

自建/本地环境可把 base 换成 `https://{站点}/index.php?s=/v1`。

```bash
curl -s "$WEBSITE_API_BASE/website.post/lists?lang=zh-CN&limit=5" \
  -H "Authorization: Bearer $WEBSITE_API_TOKEN"
```

## 二、认证

Token 放 `Authorization: Bearer tok_xxx`，也接受 `?token=tok_xxx`。

**写操作**（`add` / `edit`）强制校验：无 Token → 401；Token 无效或已停用 → 401；
Token 是只读权限 → 403。不接受任何兜底方式。

**读操作**（`lists` / `detail`）按以下顺序兜底：

1. 有效 Token → 用该 Token 的租户
2. `?domain=www.example.com` → 查 `website_domain` 表定位租户
3. 服务端开了 `WEBSITE_DEMO` 时 → 用演示租户

都拿不到租户时，读接口返回 `invalid token`。

## 三、接口一览

| 意图 | HTTP | 路由 |
|---|---|---|
| 新增文章 | POST | `website.post/add` |
| 编辑文章 | POST | `website.post/edit` |
| 文章列表 | GET | `website.post/lists` |
| 文章详情 | GET | `website.post/detail` |
| 新增/编辑/列表/详情（产品） | — | 把 `post` 换成 `product` |
| 新增/编辑/列表/详情（案例） | — | 把 `post` 换成 `cases`（注意复数） |
| 工具清单 | GET | `website.mcp/index` |

同一套能力也通过 MCP 暴露，路由 `website.mcp/{tool}`，工具名 `postAdd` / `postEdit` /
`postList` / `postDetail`，产品与案例同理（`productAdd`、`caseList`…共 12 个）。
MCP 是薄代理，行为与 HTTP API 完全一致，上面所有参数规则都适用。

## 四、请求格式（写接口三选一）

```jsonc
// ① items[] —— 各语言自带文案。多语言首选（服务端不做翻译，文案由调用方准备）
{ "items": [
    { "lang": "zh-CN", "title": "AI 帮企业把客户找回来", "body": "<p>…</p>" },
    { "lang": "en",    "title": "Let AI bring your customers back", "body": "<p>…</p>" }
]}

// ② langs[] —— 把顶层字段复制给每个语言。只适合内容本就一致的场景
{ "langs": ["zh-CN", "en"], "title": "…", "body": "…" }

// ③ 单条 —— 不传 lang 时默认 zh-CN
{ "lang": "en", "title": "…", "body": "…" }
```

传的 `lang` 必须**正好等于该站点已启用的语言代码**。不是格式归一化 —— 不在启用列表里
就直接回退成站点默认语言，**而且不报错**。所以 `en-US` 这种写法会静默写成一篇默认语言
（通常是 `zh-CN`）的内容。发多语言之前先确认客户启用了哪些语言代码，发完用 `lists`
按语言复核一遍。

## 五、字段参考

只列白名单内的字段；传白名单外的字段会被**静默丢弃**，不报错。

### 文章 `post`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `title` | string | ✅ 新增时 | — | 标题 |
| `slug` | string | | 由 title 生成 | URL 别名，见「八、服务端自动处理」 |
| `description` | string | | | 摘要 |
| `image` | string | | | 封面图 **URL** |
| `tags` | string[] | | | 标签数组 |
| `body` | string | | | 正文，**HTML** |
| `seo_title` | string | | 取 `title` | |
| `seo_desc` | string | | | |
| `is_draft` | int | | `0` | `1` 存为草稿，列表和官网都不显示 |
| `publish_date` | string | | 今天 | `YYYY-MM-DD`；传空字符串会存成 NULL |

### 产品 `product`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `title` | string | ✅ 新增时 | — | |
| `subtitle` | string | | | 副标题 |
| `slug` | string | | 由 title 生成 | |
| `image` | string | | | 图片 URL |
| `summary` | string | | | 一句话描述 |
| `features` | string[] | | | 特性列表 |
| `body` | string | | | 详情，HTML |
| `seo_title` | string | | 取 `title` | |
| `seo_desc` | string | | | |
| `sort_order` | int | | `0` | 越小越靠前 |
| `is_hidden` | int | | `0` | `1` 隐藏，不显示在官网和列表 |

### 案例 `case`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `title` | string | ✅ 新增时 | — | |
| `slug` | string | | 由 title 生成 | |
| `industry` | string | | | 行业 |
| `service` | string | | | 服务内容 |
| `image` | string | | | 图片 URL |
| `summary` | string | | | 一句话结果 |
| `body` | string | | | 正文，HTML |
| `seo_title` | string | | 取 `title` | |
| `seo_desc` | string | | | |
| `sort_order` | int | | `0` | 越小越靠前 |

## 六、接口详解

### 新增 `POST website.post/add`

请求体按「四、请求格式」三选一。每个语言条目独立处理：

- `title` 为空 → 该条失败，错误 `title 必填`，**其他语言照常写入**
- 成功条目的 `slug` 冲突时自动加 `-2`、`-3`…

```bash
curl -s "$WEBSITE_API_BASE/website.post/add" \
  -H "Authorization: Bearer $WEBSITE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[
        {"lang":"zh-CN","title":"AI 帮企业把客户找回来","body":"<p>…</p>"},
        {"lang":"en","title":"Let AI bring your customers back","body":"<p>…</p>"}
      ]}'
```

### 编辑 `POST website.post/edit`

**部分更新** —— 只传要改的字段，没传的保持原值。

定位方式二选一：

```jsonc
{ "id": 78, "lang": "zh-CN", "description": "改过的描述" }         // 按 id
{ "slug": "about-us", "lang": "en", "seo_title": "About XiongTao" } // 按 slug + lang
```

⚠️ **按 `id` 定位时，务必带上该行原本的 `lang`。** 更新语句会把 `lang` 一起写回，
而 `lang` 缺省是 `zh-CN` —— 想改一篇英文内容却漏了 `lang`，它会**被改成中文行**。

⚠️ 同理，`slug` 也会被写回。按 `id` 编辑时若不传 `slug`，用的是该行原值（不会清空）；
但传了错的值就会改掉它的 URL，线上的旧链接会失效。

按 `slug` + `lang` 定位时两个都要传，定位不到 → 该条失败，错误 `内容不存在`。

`items[]` 批量编辑时，每条都要带自己的 `id` 或 `slug`+`lang`。

### 列表 `GET website.post/lists`

| 参数 | 默认 | 说明 |
|---|---|---|
| `lang` | `zh-CN` | |
| `page` | `1` | **案例接口没有分页** |
| `limit` | `20` | 同上 |

过滤与排序：

| 接口 | 只返回 | 排序 |
|---|---|---|
| `post/lists` | `is_draft = 0` | `publish_date` 倒序 |
| `product/lists` | `is_hidden = 0` | `sort_order` 升序 |
| `cases/lists` | 全部 | `sort_order` 升序 |

返回 `{"list": [...], "total": N}`。**草稿/隐藏的内容在列表里查不到**，
写完想复核草稿要先在后台确认。

### 详情 `GET website.post/detail`

参数 `slug` + `lang`，返回 `{"detail": {...}}`。查不到返回错误 `not found`。

## 七、返回值与错误

### 成功

```json
{
  "status": 200,
  "message": "添加完成",
  "data": {
    "results": [ {"lang": "zh-CN", "ok": true, "id": 78, "slug": "ai-3f2a"} ],
    "saved": 1,
    "failed": 0
  }
}
```

部分语言失败时 `message` 会变成 `添加完成(1 条失败)`，`results[]` 里失败那条带 `error`。
**必须逐语言看 `results[].ok`**，不能只看 `status`。

### 错误

**认证失败返回真正的 HTTP 401 / 403**（ThinkPHP 异常）。而**业务失败返回 HTTP 200，
错误藏在 body 里**：

```json
{"status": 500, "message": "title 必填", "data": []}
```

所以判断成败要看 `body.status`，不能只看 HTTP 状态码。

| HTTP | `message` | 原因 |
|---|---|---|
| 401 | `缺少 Token,请在 Header 传入 Authorization: Bearer tok_xxx` | 写操作没带 Token |
| 401 | `Token 无效或已停用` | Token 不存在或 `is_active=0` |
| 403 | `当前 Token 只有只读权限,写内容需要「读写」Token` | 换成读写 Token |
| 200 | `invalid token` | 读操作没解析出任何租户 |
| 200 | `title 必填` | 新增时某个语言没给标题 |
| 200 | `内容不存在(可用 lists 查询 id/slug)` | 编辑时定位不到 |
| 200 | `not found` | 详情查不到 |
| 200 | `缺少内容:请传 items[] 或 langs[] + 字段` | 写请求体是空的 |

## 八、服务端自动处理

| 行为 | 规则 |
|---|---|
| **生成 slug** | 不传就由 `title` 生成：转小写、非字母数字换成 `-`。标题含中文、或结果短于 3 字符时，补 4 位哈希（如 `ai-3f2a`）；标题全非 ASCII 且转不出东西时用 `item-xxxx`。最长截断 80 字符 |
| **slug 去重** | 同一 `store + lang` 内唯一。冲突依次加 `-2`、`-3`…；超过 50 次改用 6 位随机串 |
| **SEO 兜底** | 传了 `title` 但没传 `seo_title` → `seo_title = title` |
| **默认值** | 见「五、字段参考」的默认列 |
| **HTML 解码** | `body` 会做一次 `htmlspecialchars_decode`，所以传 `&lt;p&gt;` 也会被当成 `<p>` 解析。**直接传原始 HTML 即可** |
| **敏感词打码** | 命中广告法词表的字段会被等长 `*` 掩码，返回消息会提示。各类型的检查范围见下 |
| **语言归一化** | 见「四、请求格式」 |

会被打码的字段：

- `post`：`title`、`description`、`tags`、`body`、`seo_title`、`seo_desc`
- `product`：`title`、`subtitle`、`summary`、`features`、`body`、`seo_title`、`seo_desc`
- `case`：`title`、`industry`、`service`、`summary`、`body`、`seo_title`、`seo_desc`

## 九、多语言

**服务端不做翻译。** 要发哪几个语言由用户决定 —— 先问清楚，不要默认"中文优先"或
自动补英文。确定后用 `items[]` 一次带上各语言文案（语言代码必须是站点已启用的，
见「四、请求格式」的坑）。

确实需要翻译时，注意这几点：

- **长度只是建议，不是限制。** 后端没有任何长度校验；`title ≤ 25 字`、`seo_title ≤ 60 字符`、
  `seo_desc ≤ 150 字符` 只出现在 AI 生成提示词里，作为写作目标。超了不会报错
- **术语按客户给的对照处理**：品牌名、产品名、以及客户指定的专有名词保持原样，
  不要自行意译。拿不准就先问
- **结构保持不变**：`body` 的 `<p>/<h2>/<ul>/<li>/<a>` 标签、`href`/`src`/`alt` 属性、
  URL、数字、日期都原样保留，只翻标签之间的文字
- **广告法**：避免「最 / 第一 / 唯一 / 国家级 / 100%」这类绝对化用语。
  服务端会自动打码，但别依赖它 —— 打码后内容就残缺了

## 十、限制

- **图片只收 URL**，不提供上传。先把图片放到图床或后台图库，再传地址过来
- 字段白名单外的字段会被**静默丢弃**，传错字段名不会报错
- 下线已有内容：产品置 `is_hidden=1`、文章置 `is_draft=1`，列表和官网都不再显示。
  **案例没有开关** —— 只能改内容，或者让客户在后台删
