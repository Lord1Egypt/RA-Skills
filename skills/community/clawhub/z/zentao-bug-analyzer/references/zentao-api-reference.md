# 禅道 API 参考

> 企业版 12.1 实例：`http://zentao.gxatek.com:20080/`
> 本文件为 API 字段/参数/错误码参考。实现示例见 `TOOLS.md`。

## 认证方式

企业版 12.1 不支持 Bearer Token（`POST /api.php/v1/tokens` 不可用）。所有操作统一通过 Playwright 登录获取 session cookie，后续请求在 `page.evaluate` 中用 `credentials: 'include'` 发起。

## Bug 详情

```
GET /api.php/v1/bugs/{bugId}
```

返回关键字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | Bug ID |
| title | string | 标题（HTML） |
| description | string | 详细描述（HTML） |
| severity | int | 严重程度 1~4 |
| priority | int | 优先级 1~4 |
| product | object | `{ id, name }` |
| project | object | `{ id, name }` |
| module | object | `{ id, name }` |
| status | string | active / resolved / closed |
| openedBy | object | `{ id, account, name }` |
| assignedTo | object | `{ id, account, name }` |
| steps | string | 复现步骤（HTML） |
| files | array | 附件列表 `[{ id, title, extension, size }]` |
| comments | array | 评论列表 `[{ id, author, comment, date }]`，author 为 account 字符串 |

## Bug 列表

```
GET /api.php/v1/bugs?product={productId}&assignedTo={account}&limit=20&status=active
```

常用过滤参数：

| 参数 | 说明 |
|------|------|
| product | 产品 ID |
| assignedTo | 指派人账号 |
| status | active / resolved / closed |
| severity | 1~4 |
| limit | 分页条数 |
| offset | 分页偏移 |

## 产品列表

```
GET /api.php/v1/products
```

## 写评论

通过 `scripts/zentao-post-comment.js` 完成。POST `{zentao_url}/action-comment-bug-{bugId}.html`，Content-Type: `application/x-www-form-urlencoded`，body: `comment={URL-encoded HTML}`。传入原始 HTML 即可，脚本自动编码。

## 附件下载

附件 URL: `{zentao_url}/file-download-{fileId}.json`。下载通过 `scripts/zentao-download-files.js` 完成（内部使用 page.evaluate + exposeFunction 分块传输，支持 160MB+ 大文件）。

## 错误码

| 状态码 | 含义 | 处理 |
|--------|------|------|
| 200 | 成功 | — |
| 401 | Session 过期 | 重新 Playwright 登录 |
| 404 | 资源不存在 | 通知用户检查 ID |
| 500 | 服务端错误 | 通知用户检查禅道状态 |
