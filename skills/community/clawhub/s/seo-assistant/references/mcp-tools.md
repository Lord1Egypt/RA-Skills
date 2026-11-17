# SEO Skill MCP 工具参考（限定范围）

本文档是 yun-zhi-seo skill 的 **MCP 工具参数参考**，仅收录与 SEO 体检/优化回写直接相关的工具：**`list_page`、`get_page_info`**、名称含 `seo` 的工具（`get_site_seo`、`edit_site_seo`、`get_seo_list`、`edit_seo`、`edit_seo_batch`），以及用于「SEO 相关页面源码改写」的 **`save_ai_page`**（受 SEO 约束，见其章节）。

> 范围约束：本 skill **仅使用上述工具**，不调用也不文档化其它 MCP 工具（产品/文章/相册/表单/SQLite/批量导入等一律不在本 skill 范围内）。其中 `save_ai_page` 仅用于「SEO 相关的页面源码改写」，严禁改动 `{{}}` / `{%%}` 数据标签及其上下文逻辑；**仅修改 TDK 时必须优先用 `edit_seo`/`edit_site_seo`，不得用 `save_ai_page` 只改标题/关键词/描述**。

工具作用于当前 MCP 连接对应的站点；调用前必须确认 MCP 地址和 Bearer Token。

## MCP 前置要求

任何 MCP 工具调用前，必须先向用户确认当前目标站点的 MCP 完整地址和 Bearer Token。

- 未提供地址和 Token 时，不调用 `test` 或任何其他工具。
- 不得猜测、复用示例地址或沿用其他站点的 Token。
- 切换站点后，必须重新获取新站点的地址和 Token。
- Token 仅由 MCP 客户端放入 `Authorization: Bearer <token>` 请求头，不作为工具参数传入。

## 通用连接规则

- 协议：JSON-RPC 2.0。
- 认证请求头：`Authorization: Bearer <token>`。
- Token 不作为任何工具参数传入。
- 工具调用前先使用 `test` 检查连通性。
- 所有工具只作用于当前连接对应的站点，不要混用不同站点的 ID。
- 切换到其他站点时，必须重新获取并确认新站点的 MCP 地址和 Bearer Token，不得沿用上一站点的连接信息或资源 ID。
- 查询工具可以在认证成功后直接调用。
- 写入工具必须在执行前向用户展示目标和影响并取得确认。

## 工具详情（仅限 SEO 相关）

以下章节逐工具给出参数、返回值、限制与推荐调用顺序，供 SEO 体检 → 分析 → 回写流程直接使用。
## `list_page`

用途：按站点后台页面列表的相同范围，列出当前站点的首页和AI自由页。

参数：

```json
{
  "keyword": "string，可选，匹配页面 Title 或 ID，默认空字符串",
  "page": "integer，可选，从 1 开始，默认值为 1",
  "pageSize": "integer，可选，最小值 1，最大值 500，默认值为 20"
}
```

限制和返回：

- 仅包含当前站点、站点类型的首页和AI自由页。
- 仅返回 `PageType` 为 `1` 和 `99` 的页面。
- 排除城市分站页面和扩展页面。
- 按 `PageType`、`ID` 升序排列。
- 返回 JSON 包含 `success`、`curpage`、`pagesize`、`pagecount` 和 `list`。
- `list` 每项仅包含 `ID`、`PageType`、`PageName`、`Title` 和 `Url`。

## `get_page_info`

用途：获取当前站点 AI 页面信息和源码。修改既有 AI 页面前必须先调用本工具读取原始 `SourceCode`，不得盲目覆盖。

参数：

```json
{
  "pageId": "integer 或正数字符串，必填"
}
```

限制：

- `pageId` 必须是当前站点页面 ID，最小值为 1。
- 仅支持 `EnableCustomTpl=1` 的AI自由页。
- 非 AI 页面会返回“此页面不是AI页面，不支持获取信息”。
- 输入对象不接受额外属性。

成功返回：仅包含以下五个字段：

- `ID`
- `PageName`
- `Url`
- `SourceCode`
- `codePath`

使用规则：

- 先通过 `list_page` 查询并确认目标页面 ID。
- 再使用本工具判断目标是否为可读取的 AI 页面，并读取现有 `SourceCode`。
- 基于读出的 `SourceCode` 做离线 SEO 分析；如需回写页面级改动，走本 skill 限定的 `seo*` 写工具（见各 seo 工具章节），并遵循写操作确认基线。
- 若工具提示页面不是 AI 页面，说明该限制并请求用户提供可读取的 AI 自由页，不要尝试覆盖非 AI 页面。

## `get_site_seo`

用途：获取当前站点的整站 SEO 信息，用于生成首页、全站公共头部元信息或核对当前整站标题与描述。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：成功返回 `success=true` 和以下字段：

- `SeoTitle`：整站 SEO 标题。
- `SeoKeyword`：整站 SEO 关键词。
- `SeoDescription`：整站 SEO 描述。
- `SiteName`：当前站点名称。

如果对应字段未配置，返回空字符串。

## `edit_site_seo`

用途：部分更新当前站点的整站 SEO。未提交的字段保持原值，显式传入空字符串可以清空字段。

这是写入工具。调用前应先用 `get_site_seo` 读取当前值，向用户展示当前站点、拟修改字段、原值和新值，并取得明确确认。整站 SEO 变更会清理当前站点缓存。

参数：

```json
{
  "title": "示例企业官网 - 专业企业网站建设",
  "keywords": "示例企业,企业建站,网站建设",
  "description": "示例企业官网为企业提供网站建设服务。"
}
```

参数说明：

- `title`：可选，整站 SEO 标题。
- `keywords`：可选，整站 SEO 关键词。
- `description`：可选，整站 SEO 描述。
- 三个字段至少提交一个，且都必须是字符串。
- 标题始终可以更新。
- 关键词和描述受当前版本 SEO 功能许可限制；无 SEO 许可时，即使提交也不会写入这两个字段。
- 显式传入空字符串可清空对应字段；未提交字段保持原值。

返回：成功返回 `success=true`、`SeoTitle`、`SeoKeyword`、`SeoDescription` 和 `SiteName`，字段值表示保存后的实际状态。

## `get_seo_list`

用途：分页查询当前站点的 SEO 列表。产品、文章、分类和页面使用不同的目标 ID，编辑前应先使用本工具核对 `seoType`、ID、当前 TDK 和独立分类页面状态。

参数：

```json
{
  "seoType": "product",
  "page": 1,
  "pageSize": 20
}
```

参数说明：

- `seoType`：必填，只能为 `product`、`article`、`productClass`、`articleClass` 或 `page`。
- `page`：可选，正整数，从 1 开始，默认 1。
- `pageSize`：可选，正整数，默认 20，最大 100。

各类型的列表语义：

- `product`：产品列表。`ID` 为 `ProductID`，包含 `Name`、`Title`、`Keywords`、`Description` 和后台编辑地址 `Url`；按产品 ID 倒序。
- `article`：文章列表。`ID` 为 `ArticleID`，`Name` 为文章标题，包含 `Title`、`Keywords`、`Description` 和后台编辑地址 `Url`；按文章 ID 倒序。
- `productClass`：产品分类列表。按分类树顺序和层级返回 `RecID`、`ClassID`、`ClassParentID`、`Level`、`Name`、`EnableCust`、`Title`、`Keywords`、`Description`；`ID` 为当前站点类型关联的独立分类页面 ID，调用 `edit_seo` 时仍使用 `ClassID`。
- `articleClass`：文章分类列表，字段含义与 `productClass` 相同。
- `page`：系统页和自定义页列表。每项包含 `ID`、`Name`、`Title`、`Keywords`、`Description` 和 `Url`；自定义页额外带 `IsCustom=true`。

返回结构：

- 顶层返回 `success`、`list`、`curpage`、`pagesize`、`pagecount` 和 `totalcount`。
- 空字段会被规范为空字符串。
- 分类启用了独立分类页面时，返回的 SEO 来自关联页面当前值；未启用独立页面时，返回分类自身保存的 SEO。
- 页面类型为自定义模板页面时，工具会从当前页面 HTML 的 `<title>`、keywords meta 和 description meta 中读取值。

注意：本工具主要是查询工具，但 `page` 类型按后台内置页面范围读取；许可允许的扩展系统页记录缺失时，读取过程可能补齐缺失的系统页记录。应在调用前向用户说明该查询可能触发系统页初始化。

## `edit_seo`

用途：设置当前站点指定对象的 SEO 标题、关键词和描述。三个文本字段都必填，但允许传空字符串清空。

这是写入工具。调用前应先用 `get_seo_list` 读取目标对象当前 SEO，向用户展示对象类型、ID、名称、URL 和完整 TDK 新值，并取得明确确认。

参数：

```json
{
  "seoType": "product",
  "id": 123,
  "title": "产品名称 - 网站名称",
  "keywords": "产品名称,关键词",
  "description": "产品详细介绍摘要"
}
```

参数说明：

- `seoType`：必填，只能为 `product`、`article`、`productClass`、`articleClass` 或 `page`。
- `id`：必填，正整数或正数字符串。不同类型对应不同 ID：
  - `product`：当前站点 `ProductID`。
  - `article`：当前站点 `ArticleID`。
  - `page`：当前站点页面 ID。
  - `productClass` 或 `articleClass`：当前站点分类 `ClassID`，不要传列表返回的 `RecID`。
- `title`、`keywords`、`description`：必填字符串，允许为空字符串。
- 本工具是整体覆盖 TDK，不是部分更新；三个字段都必须提供。

行为和影响：

- 只能编辑当前站点的产品、文章、分类和页面；目标不存在或属于其他站点时返回工具错误。
- 修改产品时写入产品 SEO 字段，修改文章时写入文章 SEO 字段。
- 修改分类时始终更新分类自身 SEO；如果当前站点类型已启用独立分类页面，并且分类关联了有效页面，会同步更新关联页面的 SEO。
- 修改 `EnableCustomTpl=1` 的AI自由页或独立分类页面时，除更新页面数据外，还会同步替换自定义 HTML 文件中的 `<title>`、keywords meta 和 description meta。如果 HTML 缺少 head 或对应标签，系统会按规则补入。
- 清空 TDK 只清空目标对象字段和自定义 HTML 对应标签，不会自动生成默认 SEO。
- 修改成功后会清理当前站点缓存。

返回：成功返回 `success=true` 和 `msg=操作成功`。

## `edit_seo_batch`

用途：保存当前站点的 SEO 批量规则，用于统一控制产品、文章页面 SEO 标题、关键词和描述的生成。

这是写入工具。调用前应先用 `get_seo_list` 或整站 SEO 查询了解当前状态，向用户展示启用状态、自动填充状态、标题分隔符、产品规则、文章规则及对后续 SEO 的影响，并取得明确确认。

参数：

```json
{
  "state": true,
  "isAutoFill": false,
  "titleSymbol": "-",
  "product": {
    "title": "{{Name}} - {{SiteName}}",
    "keywords": "{{Name}},{{SiteName}}",
    "description": "{{Name}},{{Class}},{{Label}}"
  },
  "article": {
    "title": "{{Name}} - {{SiteName}}",
    "keywords": "{{Name}},{{SiteName}}",
    "description": "{{Name}},{{Class}},{{Label}}"
  }
}
```

参数说明：

- `state`：必填，是否启用批量 SEO，可传布尔值、`0`/`1` 或 `0`/`1` 字符串。
- `isAutoFill`：必填，是否自动填充 SEO，可传布尔值、`0`/`1` 或 `0`/`1` 字符串。
- `titleSymbol`：必填，标题拼接分隔符，只能是英文逗号 `,`、下划线 `_`、短横线 `-`、竖线 `|` 或中文顿号 `、`。
- `product`：必填对象，包含 `title`、`keywords`、`description` 三个产品规则字符串。
- `article`：必填对象，包含 `title`、`keywords`、`description` 三个文章规则字符串。
- 规则可使用后台支持的变量。常用示例包括 `{{Name}}`、`{{SiteName}}`、`{{Class}}`、`{{Label}}`；实际可用变量以返回的 `defaultData` 为准。

返回：成功返回 `success=true` 和当前完整配置：

- `defaultData`：产品与文章批量 SEO 可用的默认变量列表。
- `State`：启用状态。
- `IsAutoFill`：自动填充状态。
- `TitleSymbol`：标题分隔符。
- `Product`：产品规则详情。
- `Article`：文章规则详情。

若站点还没有批量 SEO 配置，首次保存时会创建该配置。

## `save_ai_page`

用途：保存当前站点的一张自定义 HTML 页面。**本 skill 仅将它用于「SEO 相关的页面源码改写」**（如补充 `<meta>`、JSON-LD、图片 alt、canonical、`viewport`/`lang` 等），严禁改动 `{{...}}` / `{%...%}` 数据标签及其上下文逻辑，只改 SEO 内容。

参数：

```json
{
  "pageId": "integer 或数字字符串，可选，默认 0",
  "html": "string，必填，需要保存的完整 HTML 源码",
  "name": "string，可选，新建或更新页面名称，默认空字符串",
  "urlPath": "string，可选，友好 URL 路径，默认空字符串",
  "autoSetIndex": "boolean，可选，默认 false"
}
```

参数规则：

- `pageId=0`：新建页面。
- `pageId` 为正数：更新已有 AI 自由页。
- `pageId` 可传整数或只包含数字的字符串。
- `html` 必须是完整 HTML 源码（即 `get_page_info` 读出的 `SourceCode` 之上做最小化 SEO 改动后的完整内容）。
- `urlPath` 为普通 AI 自由页的可选友好 URL，例如 `about.html` 或 `products/list.html`；开头斜杠会被规范化，不安全路径会被拒绝。
- `autoSetIndex=true` 仅在 `pageId=0`、`urlPath=index.html` 且当前站点存在可替换首页时生效，默认值为 `false`。

返回和失败行为：

- 成功返回 JSON 文本，包含 `success`、`mode=html`、`isHome`、`pageId` 和 `url`。
- 参数校验或保存失败时返回带 JSON 错误信息的 MCP 工具错误。

调用前确认（SEO 约束）：

- **仅修改 TDK（标题/关键词/描述）时不得使用本工具**，必须改用 `edit_seo` / `edit_site_seo`。
- 必须先用 `get_page_info` 读出 `SourceCode` 作为基线，**只做最小化 SEO 改动**；`html` 必须回传完整源码，不得在改动中丢失或改写任何 `{{}}` / `{%%}` 标签及其所在逻辑块（循环、条件、数据占位等）。
- 改动前对比差异，确认未触碰数据标签与平台绑定；如有不确定，先询问用户。
- 写前展示目标 + 影响 + 差异摘要，取得确认后调用；写后回读确认并保留修改前快照便于回滚。


## 实测注意事项（81102 站踩坑沉淀，2026-09）

1. **`get_page_info` 成功响应没有 `success` 字段**：直接返回 `ID/PageName/Url/SourceCode/codePath`。判断成功用 `SourceCode` 是否存在，不要判 `success`。
2. **自定义页 SourceCode 可能存在重复 `<head>`/重复 meta**（历史编辑堆叠，曾见单页 2 个 DOCTYPE、3 个 `<head>`、2 份 description meta）。`edit_seo` / `edit_seo_batch` 只替换其中一份，**其余旧 meta 会残留**，搜索引擎可能读到旧值。做法：edit_seo 回写后必须 `get_page_info` 回读，检查 description/title meta 是否多份，多份时保留目标值那份、删除其余，再经 `save_ai_page` 写回，并抓线上验证首个 meta 为目标值。
3. **`save_ai_page` 是整体覆盖**：若先 `edit_seo` 改 TDK、再基于"改 TDK 之前"拉取的 SourceCode 做源码改动并 `save_ai_page`，会把新 TDK 覆盖回旧值。源码改动基线必须取 TDK 写入**之后**的最新 SourceCode。
4. **title 可能是模板动态标签**（`<title>` 内含 `{{}}`）：此时不得替换其内容，保持模板绑定，只去重。
5. 平台对 `get_seo_list` 可能返回业务层 `{"success":false,"msg":"验证不通过","needLogin":1}`（CSRF 挑战），带 Cookie 回传仍可能不通过；此时可用整站爬取报告中的渲染值作为 TDK 当前值基线（自定义页 TDK 存于 HTML 文件，两者一致）。
