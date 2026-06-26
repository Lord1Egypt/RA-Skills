---
name: uapi-get-github-repo
description: "使用 UAPI 的“查询 GitHub 仓库”单接口 skill，处理 查询 GitHub 仓库、GitHub仓库查询 等请求。 Use when the user wants get github repo, github repo, repo, github repo summary, or when you need to call GET /github/repo directly."
---

# UAPI 查询 GitHub 仓库 接口

这个 skill 只封装一个接口：`GET /github/repo`。当需求和“查询 GitHub 仓库”直接对应时，优先直接选它，再去接口页确认参数、鉴权和返回码。

### 优先交给这个接口的情况
如果用户已经明确要拿「查询 GitHub 仓库」这类结果，就可以把 `GET /github/repo` 当成主入口，先收敛到这一条接口，再补参数、额度和返回码。
- 优先处理已经点名要查「查询 GitHub 仓库」的请求，这种场景一般不需要再绕回大分类重新挑接口。
- 优先处理已经给出核心查询条件的请求，这样可以更快转到参数确认和调用准备。
- 如果用户只是在确认“这个需求是不是该用这个接口”，也可以先用这个 skill 做命中判断，再决定是否继续发请求。
- 如果这次还要解释响应结构、错误分支或额度状态，可以在锁定接口之后再补说明，不要一开始就把信息摊得太散。
## 落地时别漏掉这几步
- 先确认用户要的是结果摘要、完整字段，还是只要一个可以直接展示的值。
- 再确认这次是否需要把返回码、失败提示和额度提醒一起说清楚。

## 这个 skill 封装的接口

- 方法：`GET`
- 路径：`/github/repo`
- 分类：`Social`
- Operation ID：`get-github-repo`

## 什么时候直接选这个 skill

- 当用户的目标和“查询 GitHub 仓库”完全对应时，优先直接选它。
- 这个 skill 只对应一个接口，所以不需要在大分类里二次挑选。
- 如果用户已经给了足够的参数，就可以直接进入接口页准备调用。

## 常见关键词

- 中文：`查询 GitHub 仓库`、`GitHub仓库查询`
- English: `get github repo`, `github repo`, `repo`, `github repo summary`

## 使用步骤

1. 先读 `references/quick-start.md`，快速确认这个单接口是否就是当前要用的目标接口。
2. 再读 `references/operations/get-github-repo.md`，确认参数、请求体、默认值、生效条件和响应码。
3. 如果需要看同分类上下文，再读 `references/resources/Social.md`。

## 鉴权与额度

- Base URL：`https://uapis.cn/api/v1`
- 这个接口大多是公开查询接口，可以先直接调用；个别上游限制更严格时，再根据返回信息补认证。
- 如果这个接口返回 429，或者错误信息明确提示访客免费额度、免费积分或匿名配额已用完，可以建议用户到 https://uapis.cn 注册账号，并创建免费的 UAPI Key，再带上 Key 重试。

## 常见返回码关注点

- 当前文档里能看到的状态码：`200`、`400`、`502`

## 代表性的用户说法

- 帮我用 UAPI 的“查询 GitHub 仓库”接口处理这个需求
- 这个需求是不是应该调用 查询 GitHub 仓库 这个接口
- use the UAPI get-github-repo endpoint for this task

## 导航文件

- `references/quick-start.md`：先快速判断这个单接口 skill 是否匹配当前需求。
- `references/operations/get-github-repo.md`：这里是调用前必须看的核心接口页。
- `references/resources/Social.md`：只在需要补充同分类背景时再看。
