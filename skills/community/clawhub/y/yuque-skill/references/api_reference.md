# 语雀开放API速查表

本文档汇总本Skill中使用到的语雀v2 API端点。完整规范见 [https://www.yuque.com/yuque/developer/api](https://www.yuque.com/yuque/developer/api)。

## 鉴权

所有请求都必须带 `X-Auth-Token` 头。Token在 [https://www.yuque.com/settings/tokens](https://www.yuque.com/settings/tokens) 创建,具备如下scope时才能完整使用本skill:

| Scope | 必要操作 |
|-------|---------|
| `doc:read` | 读取文档/列表 |
| `doc:write` | 创建/更新/删除文档 |
| `repo:read` | 列出知识库 |
| `repo:write` | 创建知识库、修改TOC |
| `group:read` | 团队相关 |

## 用户与团队

| Method | Path | 说明 |
|---|---|---|
| GET | `/user` | 当前token对应的用户 |
| GET | `/users/:login` | 公开用户信息 |
| GET | `/groups/:login` | 团队信息 |
| GET | `/users/:login/groups` | 用户加入的团队 |

## 知识库(Repo / Book)

| Method | Path | 说明 |
|---|---|---|
| GET | `/users/:login/repos` | 用户的知识库 |
| GET | `/groups/:login/repos` | 团队的知识库 |
| POST | `/users/:login/repos` | 创建用户知识库 |
| POST | `/groups/:login/repos` | 创建团队知识库 |
| GET | `/repos/:namespace` | 单个知识库详情 |
| PUT | `/repos/:namespace` | 更新知识库 |
| DELETE | `/repos/:namespace` | 删除知识库 |

`namespace` 形如 `username/repo-slug`。创建repo常用字段:

```json
{"name": "我的笔记", "slug": "notes", "description": "...",
 "public": 0, "type": "Book"}
```

`type` 取值:`Book`(知识库),`Sheet`(数据表),`Thread`(讨论)。

## 文档(Doc)

| Method | Path | 说明 |
|---|---|---|
| GET | `/repos/:namespace/docs` | 文档列表(支持`limit`&`offset`分页) |
| GET | `/repos/:namespace/docs/:slug` | 单篇文档(`raw=1` 获取原始Markdown) |
| POST | `/repos/:namespace/docs` | 创建文档 |
| PUT | `/repos/:namespace/docs/:id` | 更新文档(必须用数字id,不接受slug) |
| DELETE | `/repos/:namespace/docs/:id` | 删除文档 |

创建/更新常用字段:

```json
{"title": "标题", "slug": "auto-or-custom", "format": "markdown",
 "body": "Markdown正文", "public": 0,
 "_force_asl": 1}
```

`public` 取值:`0` 私密、`1` 公开、`2` 仅登录用户可见。

## 目录(TOC)

| Method | Path | 说明 |
|---|---|---|
| GET | `/repos/:namespace/toc` | 当前目录扁平结构 |
| PUT | `/repos/:namespace/toc` | 提交一个或多个 action |

action对象常见字段:

```json
{
  "action": "appendNode|prependNode|editNode|removeNode|moveNode",
  "action_mode": "child|sibling|prevSibling|nextSibling",
  "type": "DOC|TITLE|LINK",
  "title": "...",
  "doc_ids": [123],
  "target_uuid": "母节点或锚点uuid",
  "node_uuid": "被操作节点uuid(edit/remove/move 时用)",
  "delete_doc": false
}
```

## 搜索

| Method | Path | 说明 |
|---|---|---|
| GET | `/search?type=doc&q=...&scope=user` | 全文搜索文档 |
| GET | `/search?type=book&q=...` | 搜索知识库 |

## 速率限制

语雀公有云默认 5000 req/h。`yuque_client.py._request` 已对 `429/5xx` 自动指数退避(2/4/8s)。批量任务建议:

* 每秒不超过 5 个写操作
* 每批写完 `time.sleep(0.2)`
* 大量导入用 `batch.py import`,内部会串行避免风暴

## 常见错误码

| Status | 含义 | 处理建议 |
|---|---|---|
| 400 | 参数错误 | 检查必填字段、JSON正确性 |
| 401 | Token无效或过期 | 重新生成Token |
| 403 | 无权限 | 检查Token的scope或资源所有者 |
| 404 | namespace或slug不存在 | 先 list-repos / list-docs 验证 |
| 409 | slug冲突 | 换一个slug或省略由后端生成 |
| 422 | 内容含禁用HTML/Markdown | `format_helpers.sanitize()` 清洗 |
| 429 | 限流 | 自动退避,无需人工干预 |
