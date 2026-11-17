# 建站 MCP 工具参考

本文档记录建站 MCP 服务提供的工具。工具作用于当前 MCP 连接对应的站点；调用前必须确认 MCP 地址和 Bearer Token。

> 适用范围：本文件是 MCP 工具的权威参数参考（参数、返回值、限制、推荐调用顺序）。模板侧 `FnGet*` 系列函数的返回字段由平台提供，不在本文件范围内。

> 本技能实际调用的工具（其余为完整参考，Agent 可按需查阅）：`test`、`list_page`、`get_page_info`、`list_custom_form`、`add_custom_form`、`edit_custom_form`、`get_enquiry_form_id`、`list_enquiry_records`、`get_product_list`、`get_product_info`、`edit_product`、`upload_product_image`、`save_ai_page`、`clear_site_cache`。

## MCP 前置要求

任何 MCP 工具调用前，必须先向用户确认当前目标站点的 MCP 完整地址和 Bearer Token。

- 未提供地址和 Token 时，不调用 `test` 或任何其他工具。
- 不得猜测、复用示例地址或沿用其他站点的 Token。
- 切换站点后，必须重新获取新站点的地址和 Token。
- Token 仅由 MCP 客户端放入 `Authorization: Bearer <token>` 请求头，不作为工具参数传入。
- 当新的 MCP 链接成功后，请清除 agent 智能体记忆里关于旧的MCP的相关内容，避免记忆混乱导致使用了不正确的MCP。

## 通用连接规则

- 协议：JSON-RPC 2.0。
- 认证请求头：`Authorization: Bearer <token>`。
- Token 不作为任何工具参数传入。
- 工具调用前先使用 `test` 检查连通性。
- 所有工具只作用于当前连接对应的站点，不要混用不同站点的 ID。
- 切换到其他站点时，必须重新获取并确认新站点的 MCP 地址和 Bearer Token，不得沿用上一站点的连接信息或资源 ID。
- 查询工具可以在认证成功后直接调用。
- 写入工具必须在执行前向用户展示目标和影响并取得确认。

## 工具总览

| 工具 | 类型 | 主要用途 |
| --- | --- | --- |
| `test` | 查询/诊断 | 测试 MCP 连通性并回显请求参数 |
| `list_custom_form` | 查询 | 列出当前站点普通自定义表单 |
| `add_custom_form` | 写入 | 新增普通自定义表单及字段 |
| `edit_custom_form` | 写入 | 修改普通自定义表单、字段或删除字段 |
| `list_news_class` | 查询 | 列出完整新闻分类树 |
| `list_page` | 查询 | 分页列出首页和自定义页面 |
| `get_page_info` | 查询 | 获取当前站点 AI 自定义页面的页面信息和源码 |
| `list_product_class` | 查询 | 列出完整产品分类树 |
| `get_news_info` | 查询 | 获取单篇文章详情 |
| `get_news_list` | 查询 | 分页查询已发布文章 |
| `get_product_info` | 查询 | 获取单个产品基础详情 |
| `get_product_list` | 查询 | 分页查询已发布产品 |
| `get_enquiry_form_id` | 查询/可能写入 | 获取当前站点在线询盘表单 ID |
| `list_enquiry_records` | 查询 | 分页列出当前站点在线询盘记录（含表单字段值与询盘产品） |
| `add_news` | 写入 | 新增一篇文章，可创建草稿或立即发布 |
| `add_news_class` | 写入 | 新增一个文章分类 |
| `edit_news` | 写入 | 部分更新一篇文章 |
| `add_product` | 写入 | 新增并立即发布一个精简产品 |
| `add_product_class` | 写入 | 新增一个产品分类 |
| `edit_product` | 写入 | 部分更新一个产品 |
| `upload_file` | 写入 | 上传站点资源库文件 |
| `upload_product_image` | 写入 | 上传产品主图素材 |
| `save_ai_page` | 写入 | 新建或更新单个自定义 HTML 页面 |
| `clear_site_cache` | 维护操作 | 清理当前站点缓存 |

## `test`

用途：测试 MCP 服务连通性，返回工具名和请求参数。

参数：

```json
{
  "message": "string，必填，需要回显的测试文本",
  "count": "integer，可选，测试次数，最小值为 1，默认值为 1",
  "options": "object，可选，附加测试参数，允许任意属性"
}
```

要求：

- `message` 必须提供。
- `count` 不得小于 1。
- 首次连接时建议使用简短、不含敏感信息的测试文本。

## `list_custom_form`

用途：列出当前站点的普通自定义表单。

参数：无参数。输入对象必须为空，不接受额外属性。

使用规则：

- 当模型判断页面需要表单时，应优先调用本工具，不直接生成独立静态表单。
- 将返回的表单 `ID` 和 `Name` 展示给用户，并等待用户明确选择。
- 用户选择前不得猜测表单 ID 或生成绑定到任意表单的最终代码。
- 用户已经提供表单 ID 时，也应调用本工具验证该 ID 属于当前站点。
- 用户选定后，在页面模板中使用 `FnGetCustomForm(表单ID)` 接入系统动态表单。
- 返回列表为空时，提示用户先在站点后台创建表单；除非用户明确要求，否则不降级为静态表单。

返回：

- 仅返回 `FormType` 为 `CustomForm` 的 `tbl_form` 记录。
- 按 `ID` 倒序排列。
- 每项仅包含 `ID` 和 `Name`。
- 不返回询盘表单、产品留言表单或其他类型表单。

## `add_custom_form`

用途：为当前站点新增一个普通自定义表单，并可在同一次调用中新增字段。工具固定写入 `FormType=CustomForm`，不能创建在线询盘表单、产品留言表单或其他特殊表单。

这是写入工具。调用前必须向用户展示表单名称、字段列表、通知配置、支付配置及可能的副作用，并取得明确确认。

参数：

```json
{
  "name": "报名表",
  "intro": "请填写报名信息",
  "enableEmailNotification": 0,
  "enableSmsNotification": 0,
  "receivedEmail": "",
  "isPay": 0,
  "payAmount": 0,
  "payTips": "",
  "payType": 0,
  "calculations": "",
  "fields": [
    {
      "id": "NewName",
      "name": "姓名",
      "fieldType": 1,
      "isRequire": 1,
      "validateType": 1,
      "placeholder": "请输入姓名"
    }
  ]
}
```

参数说明：

- `name`：必填，表单名称，1 至 50 个字符。
- `intro`：可选，表单介绍，最多 200 个字符。
- `enableEmailNotification`、`enableSmsNotification`、`isPay`、`payType`：可选，只能为 `0` 或 `1`，默认值为 `0`。
- `receivedEmail`：可选，邮件通知接收地址。启用邮件通知时必填；多个地址使用换行、分号或逗号分隔，最多 10 个。
- `payAmount`：可选，非负数字。
- `payTips`：可选，支付提示语。
- `calculations`：可选，表单计算配置字符串，可引用字段 ID 或字段临时 ID。
- `fields`：可选，字段对象数组，数组顺序决定 `ShowOrder`；默认空数组。

字段参数：

- `id`：可选。新增字段只能使用 `New` 开头的临时 ID，例如 `NewName`；不能使用已有数字 ID。临时 ID 可被 `fieldValuesRel`、`calculationsItem` 和 `calculations` 引用，保存后会替换为真实字段 ID。
- `name`：必填，字段名称，1 至 50 个字符。
- `intro`、`placeholder`、`icon`、`extendName`：可选字符串。
- `fieldType`：可选，`1` 单行文本、`2` 多行文本、`3` 单选、`4` 下拉、`5` 多选、`6` 图片上传、`7` 中国国内地区、`8` 时间、`9` 文件上传、`10` 多图上传、`11` 静态文本、`12` 国际地区。
- `fieldValues`：可选，单选、下拉、多选的选项，使用 `|` 或换行分隔；保存时会规范为 `|` 分隔。
- `isRequire`、`isShow`、`isSmsValidate`、`isShowTitle`、`pcShowType`、`mobileShowType`：可选，只能为 `0` 或 `1`。
- `validateType`：可选，`0` 不验证、`1` 文本、`2` 数字、`3` 手机、`4` 固话、`5` 固话或手机、`6` 邮箱、`7` 身份证；仅文本字段和多行文本字段有效，其他字段必须为 `0`。
- `isSmsValidate=1` 仅适用于 `fieldType=1` 且 `validateType=3` 的手机号字段，并会自动设置为必填。
- `fieldValuesRel`、`calculationsItem`：可选，可传 JSON 字符串、对象或数组，用于选项联动和字段计算。

返回：

```json
{
  "success": true,
  "FormID": 123,
  "Name": "报名表",
  "FormType": "CustomForm",
  "fieldCount": 1,
  "fields": [
    {
      "ID": 456,
      "Name": "姓名",
      "FieldType": 1,
      "ShowOrder": 0
    }
  ]
}
```

限制：

- 表单创建、字段写入不是跨调用事务；调用失败时已经创建的表单或字段不会自动回滚，失败后应重新查询确认实际状态。
- 不得把 Token 放入工具参数；认证由 MCP 客户端通过请求头完成。
- 创建后页面接入仍须使用 `list_custom_form`/用户选择的表单 ID 和 `FnGetCustomForm(表单ID)`，不得猜测 ID。

## `edit_custom_form`

用途：修改当前站点一个普通自定义表单的主体配置，新增或更新字段，以及按需删除字段。仅支持已有 `FormType=CustomForm` 的表单。

这是写入工具。调用前必须向用户展示当前站点、表单 ID、表单名称、拟修改字段、删除字段及通知/支付影响，并取得明确确认。

参数：

```json
{
  "formId": 123,
  "name": "更新后的报名表",
  "intro": "新的说明",
  "fields": [
    {
      "id": 456,
      "name": "姓名",
      "fieldType": 1,
      "isRequire": 1
    },
    {
      "id": "NewPhone",
      "name": "手机",
      "fieldType": 1,
      "validateType": 3,
      "isRequire": 1
    }
  ],
  "deleteFieldIds": [789]
}
```

参数说明：

- `formId`：必填，当前站点普通自定义表单 ID，必须是正整数或正数字符串。
- `name`、`intro`、`enableEmailNotification`、`enableSmsNotification`、`receivedEmail`、`isPay`、`payAmount`、`payTips`、`payType`、`calculations`：可选，仅提交需要修改的表单主体字段。
- `fields`：可选。带数字 `id` 的字段表示更新已有字段；带 `New` 开头临时 ID 或不带 `id` 的字段表示新增字段。字段数组顺序决定本次提交字段的 `ShowOrder`；未列出的已有字段保持不变。
- `deleteFieldIds`：可选，要删除的当前表单字段 ID 数组。字段不能同时出现在 `fields` 和 `deleteFieldIds` 中。

字段配置、字段类型、校验类型和临时 ID 规则与 `add_custom_form` 相同。

删除语义：

- `NoDel=1` 的字段禁止删除。
- 表单没有提交记录时，字段会物理删除。
- 表单已有提交记录时，字段不会物理删除，而是设置 `IsShow=0` 隐藏，以保留历史数据。
- 未显式列入 `deleteFieldIds` 的字段不会被删除。

返回：

```json
{
  "success": true,
  "FormID": 123,
  "Name": "更新后的报名表",
  "FormType": "CustomForm",
  "fieldCount": 2,
  "fields": [
    {
      "ID": 456,
      "Name": "姓名",
      "FieldType": 1,
      "ShowOrder": 0
    },
    {
      "ID": 790,
      "Name": "手机",
      "FieldType": 1,
      "ShowOrder": 1
    }
  ]
}
```

限制：

- 更新表单、字段和删除字段不是跨调用事务；中途失败时已完成的修改不会自动回滚，失败后应使用 `list_custom_form` 或后台查询确认实际状态。
- 修改页面中的表单代码前，仍需先按表单规则读取并确认当前表单，不能用静态表单替代系统表单。
- 这两个工具都不能修改在线询盘表单；在线询盘表单使用 `get_enquiry_form_id`。

## `list_news_class`

用途：列出当前站点完整的新闻分类树。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：分类树按后台显示顺序返回。每个分类仅包含：

- `ClassID`
- `ParentID`
- `ShowOrder`
- `Name`
- `sublist`：该分类的子分类列表

## `add_news_class`

用途：为当前站点新增一个文章分类。

参数：

```json
{
  "name": "string，必填，分类名称，长度至少为 1",
  "parentId": "integer 或数字字符串，可选，默认 0"
}
```

限制和返回：

- 每次调用只新增一个分类。
- `parentId=0` 表示新增一级分类。
- 非零 `parentId` 必须属于当前站点。
- 成功返回新分类的 `ClassID`、`Name`、`ParentID` 和 `Url`。

调用前确认分类名称和父分类；非一级分类必须先使用 `list_news_class` 核对父分类 ID。

## `add_news`

用途：为当前站点新增一篇文章。`content` 使用原始 HTML，不需要 Base64 编码。

参数：

```json
{
  "title": "string，必填，长度至少为 1",
  "content": "string，必填，原始 HTML，长度至少为 1",
  "classIds": "array，可选，当前站点文章分类 ID，默认 [0]",
  "status": "integer，可选，0=草稿，1=立即发布，默认 1",
  "publishTime": "string，可选，可被 PHP strtotime 识别的发布时间",
  "previewImage": "string，可选，文章缩略图 URL",
  "author": "string，可选，文章作者",
  "source": "string，可选，文章来源",
  "seoTitle": "string，可选，SEO 标题",
  "keywords": "string，可选，SEO 关键词",
  "description": "string，可选，SEO 描述",
  "showOrder": "integer，可选，最小值 0，默认 0"
}
```

限制和返回：

- `classIds` 的每项可为不小于 0 的整数或仅包含数字的字符串。
- `classIds` 不能重复。
- 默认分类为 `[0]`；`0` 表示未分类，不能与其他分类同时使用。
- 非零分类必须属于当前站点，应先用 `list_news_class` 验证。
- `status=0` 为草稿，`status=1` 为立即发布；工具默认立即发布。
- 使用 `previewImage` 时，先调用 `upload_file` 上传图片并使用其返回的绝对 URL。
- 成功返回 `ArticleID`、`Title` 和 `Url`。

调用前必须确认标题、HTML 内容、分类、发布时间和发布状态。用户未明确要求发布时，使用 `status=0` 创建草稿。

## `edit_news`

用途：部分更新当前站点的一篇文章。

参数：

```json
{
  "articleId": "integer 或正数字符串，必填，当前站点文章 ID",
  "title": "string，可选，传入时不能为空",
  "content": "string，可选，文章原始 HTML，传空字符串可清空内容",
  "classIds": "array，可选，文章分类 ID，空数组改为未分类 [0]",
  "status": "integer，可选，0=草稿，1=发布",
  "publishTime": "string，可选，PHP 可识别的日期字符串",
  "previewImage": "string，可选，文章缩略图 URL",
  "author": "string，可选，文章作者",
  "source": "string，可选，文章来源",
  "seoTitle": "string，可选，SEO 标题",
  "keywords": "string，可选，SEO 关键词",
  "description": "string，可选，SEO 描述",
  "showOrder": "integer，可选，最小值 0，文章排序值"
}
```

限制和行为：

- `articleId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- `articleId` 必须属于当前站点。
- 未传入的字段保留原值。
- 至少需要提交一个实际更新字段，不能只提交 `articleId`。
- `classIds` 传空数组会改为未分类 `[0]`；`0` 不能与其他分类同时使用。
- 文章分类 ID 应先通过 `list_news_class` 验证。
- `title` 传入时不能为空。
- `content` 传空字符串会清空文章内容。

调用前应先使用 `get_news_info` 读取当前文章，向用户展示将修改的字段并获得确认。涉及 `status=1` 时，明确提示文章会发布。

## `get_news_info`

用途：获取当前站点一篇文章的详情。

参数：

```json
{
  "articleId": "integer 或正数字符串，必填，文章 ID"
}
```

限制和返回：

- `articleId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- 仅允许查询当前站点。
- 文章不存在时返回工具错误。
- 成功返回 `SiteDataAdapter::getOneNews()` 提供的原始文章字段及 `ClassList`，不改名、不额外裁剪字段。

## `get_news_list`

用途：查询当前站点已发布文章列表。

参数：

```json
{
  "classId": "integer 或数字字符串，可选，默认 0",
  "keyword": "string，可选，按文章标题搜索，默认空字符串",
  "page": "integer，可选，从 1 开始，默认 1",
  "pageSize": "integer，可选，最小 1，最大 100，默认 20",
  "sortField": "UpTime | CrTime | PublishTime | ShowOrder | ArticleID，可选，默认 UpTime",
  "sort": "asc | desc，可选，默认 desc"
}
```

限制和返回：

- `classId=0` 表示全部分类，并包含子分类文章。
- `classId` 必须为不小于 0 的整数或数字字符串。
- `pageSize` 最大为 100。
- `sortField` 只能使用 `UpTime`、`CrTime`、`PublishTime`、`ShowOrder` 或 `ArticleID`。
- `sort` 只能使用 `asc` 或 `desc`。
- 返回 `SiteDataAdapter::getNews()` 产生的文章记录，不改名、不额外裁剪字段。

## `list_page`

用途：按站点后台页面列表的相同范围，列出当前站点的首页和自定义页面。

参数：

```json
{
  "keyword": "string，可选，匹配页面 Title 或 ID，默认空字符串",
  "page": "integer，可选，从 1 开始，默认值为 1",
  "pageSize": "integer，可选，最小值 1，最大值 500，默认值为 20"
}
```

限制和返回：

- 仅包含当前站点、站点类型的首页和自定义页面。
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
- 仅支持 `EnableCustomTpl=1` 且 `PageType=99` 的自定义 AI 页面。
- 非 AI 页面会返回“此页面不是AI页面，不支持获取信息”。
- 输入对象不接受额外属性。

成功返回：仅包含以下四个字段：

- `ID`
- `PageName`
- `Url`
- `SourceCode`

使用规则：

- 先通过 `list_page` 查询并确认目标页面 ID。
- 再使用本工具判断目标是否为可读取的 AI 页面，并读取现有 `SourceCode`。
- 基于读出的源码生成修改方案，再向用户展示更新目标和影响，得到确认后才调用 `save_ai_page`。
- 若工具提示页面不是 AI 页面，不得使用 `save_ai_page` 直接覆盖；应说明限制并改用合适的页面编辑方式或请求用户提供可编辑的 AI 页面。

## `list_product_class`

用途：列出当前站点完整的产品分类树。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：分类树按后台显示顺序返回。每个分类仅包含：

- `ClassID`
- `ParentID`
- `ShowOrder`
- `Name`
- `sublist`：该分类的子分类列表

## `add_product_class`

用途：为当前站点新增一个产品分类。

参数：

```json
{
  "name": "string，必填，分类名称，长度至少为 1",
  "parentId": "integer 或数字字符串，可选，默认 0"
}
```

限制和返回：

- 每次调用只新增一个分类。
- `parentId=0` 表示新增一级分类。
- 非零 `parentId` 必须属于当前站点，应先用 `list_product_class` 验证。
- 本工具仅支持设置分类名称和父分类，不支持分类图片或独立页面。
- 成功返回分类 ID、名称、父分类 ID 和前台分类 URL。

调用前确认分类名称和父分类。

## `upload_product_image`

用途：上传当前站点的产品主图素材。该工具不会自动将图片绑定到产品。

参数：

```json
{
  "fileName": "string，必填，包含扩展名的图片文件名，不能包含目录路径",
  "fileBase64": "string，可选，纯 Base64 或 Data URI",
  "sourceUrl": "string，可选，HTTP/HTTPS 远程图片地址"
}
```

限制和返回：

- 仅支持 `webp`、`png`、`jpg`、`jpeg`，文件最大为 5 MiB。
- `fileBase64` 与 `sourceUrl` 必须且只能提供一个。
- `sourceUrl` 必须以 `http://` 或 `https://` 开头。
- 成功返回产品大图文件名 `fileName`、产品小图文件名 `SmallFileName` 及对应 URL。

后续调用 `add_product` 时，将返回的 `fileName` 和 `SmallFileName` 原样传入 `mainImage`；不得自行构造文件名。

## `add_product`

用途：在当前站点新增并立即发布一个精简产品。

参数：

```json
{
  "name": "string，必填，产品名称，长度至少为 1",
  "classIds": "array，可选，当前站点产品分类 ID，默认 [0]",
  "mainImage": {
    "fileName": "string，upload_product_image 返回的大图文件名",
    "SmallFileName": "string，upload_product_image 返回的小图文件名"
  },
  "price": "非负数字或数字字符串，可选，默认 0",
  "seoTitle": "string，可选，SEO 标题",
  "keywords": "string，可选，SEO 关键词，写入 ProKeyword",
  "seoDescription": "string，可选，SEO 描述",
  "summary": "string，可选，产品简介，写入 ProDesc",
  "content": "string，可选，单一产品详情的原始 HTML"
}
```

限制：

- `classIds` 每项可为不小于 0 的整数或仅包含数字的字符串。
- 默认分类为 `[0]`；`0` 表示未分类，不能与其他分类同时使用。
- 非零分类必须属于当前站点，应先用 `list_product_class` 验证。
- `mainImage` 可省略；提供时必须同时包含 `fileName` 与 `SmallFileName`，且二者都必须来自当前站点产品图片目录。
- `price` 必须为非负数。
- `content` 会以“产品详情”为标题保存为单项详情。
- 本工具会立即发布产品。
- 不支持 SKU、规格、标签、会员权限、筛选、附件、定时发布等高级后台字段。

调用前必须确认产品名称、分类、价格、主图、SEO、简介和详情内容，并明确告知产品将立即发布。

## `edit_product`

用途：部分更新当前站点的精简产品。

参数：

```json
{
  "productId": "integer 或正数字符串，必填，当前站点产品 ID",
  "name": "string，可选，传入时不能为空",
  "classIds": "array，可选，产品分类 ID，空数组改为未分类 [0]",
  "mainImage": "object、null 或空对象，可选，产品主图",
  "price": "非负数字或数字字符串，可选",
  "seoTitle": "string，可选，SEO 标题",
  "keywords": "string，可选，SEO 关键词",
  "seoDescription": "string，可选，SEO 描述",
  "summary": "string，可选，产品简介",
  "content": "string，可选，产品详情 HTML，空字符串可清空详情"
}
```

`mainImage` 对象结构：

```json
{
  "fileName": "string，产品大图文件名",
  "SmallFileName": "string，产品小图文件名"
}
```

限制和行为：

- `productId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- `productId` 必须属于当前站点。
- 未传入的字段保留原值。
- 至少需要提交一个实际更新字段，不能只提交 `productId`。
- `classIds` 传空数组会改为未分类 `[0]`；`0` 不能与其他分类同时使用。
- 产品分类 ID 应先通过 `list_product_class` 验证。
- `name` 传入时不能为空。
- 省略 `mainImage` 表示保留原图。
- `mainImage=null` 或空对象表示清空主图。
- 更新主图时应使用 `upload_product_image` 返回的两个文件名，不得自行拼接。
- `price` 必须为非负数。

调用前应先使用 `get_product_info` 读取当前产品，向用户展示将修改的字段并获得确认。

## `get_product_info`

用途：获取当前站点一个产品的基础详情。

参数：

```json
{
  "productId": "integer 或正数字符串，必填，产品 ID"
}
```

限制和返回：

- `productId` 最小值为 1，可传整数或匹配 `^[1-9]\d*$` 的数字字符串。
- 仅允许查询当前站点。
- 产品不存在时返回工具错误。
- 成功返回 `SiteDataAdapter::getOneProductBase()` 提供的原始产品字段及 `ClassList`，不改名、不额外裁剪字段。

## `get_product_list`

用途：查询当前站点已发布产品列表。

参数：

```json
{
  "classId": "integer 或数字字符串，可选，默认 0",
  "keyword": "string，可选，按产品名称搜索，默认空字符串",
  "page": "integer，可选，从 1 开始，默认 1",
  "pageSize": "integer，可选，最小 1，最大 100，默认 20",
  "sortField": "CrTime | UpTime | ShowOrder | ProductID | Price | SalesCount，可选，默认 CrTime",
  "sort": "asc | desc，可选，默认 desc"
}
```

限制和返回：

- `classId=0` 表示全部分类，并包含子分类产品。
- `classId` 必须为不小于 0 的整数或数字字符串。
- `pageSize` 最大为 100。
- `sortField` 只能使用 `CrTime`、`UpTime`、`ShowOrder`、`ProductID`、`Price` 或 `SalesCount`。
- `sort` 只能使用 `asc` 或 `desc`。
- 返回 `SiteDataAdapter::getProduct()` 产生的产品记录，不改名、不额外裁剪字段。

## `upload_file`

用途：向当前站点资源库上传一个文件。

参数：

```json
{
  "fileName": "string，必填，包含扩展名的文件名，不能包含目录路径",
  "fileBase64": "string，可选，纯 Base64 或 Data URI",
  "sourceUrl": "string，可选，HTTP/HTTPS 远程文件地址",
  "type": "string，可选，auto、image 或 file，默认 auto",
  "folderId": "integer 或正数字符串，可选，当前站点资源文件夹 ID",
  "watermark": "boolean，可选，仅 image 类型生效，默认 false"
}
```

限制和返回：

- `fileBase64` 与 `sourceUrl` 必须且只能提供一个。
- `sourceUrl` 必须以 `http://` 或 `https://` 开头。
- `type=auto` 时按扩展名自动识别图片或普通文件。
- 未提供 `folderId` 时，系统自动使用或创建默认文件夹。
- `watermark` 仅对 `image` 类型生效。
- 成功返回资源 ID、名称、绝对 URL、相对 URL、文件类型、扩展名、大小和文件夹 ID。

调用前确认文件名、唯一来源、类型、目标文件夹和是否加水印。需要作为文章缩略图时，使用返回的绝对 URL。

## `save_ai_page`

用途：保存当前站点的一张自定义 HTML 页面。

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
- `pageId` 为正数：更新已有自定义页面。
- `pageId` 可传整数或只包含数字的字符串。
- `html` 必须是完整 HTML 源码。
- 远程图片 URL 和支持的内联 Base64 资源会按站点后台编辑器规则处理。
- `urlPath` 为普通自定义页面的可选友好 URL，例如 `about.html` 或 `products/list.html`；开头斜杠会被规范化，不安全路径会被拒绝。
- `autoSetIndex=true` 仅在 `pageId=0`、`urlPath=index.html` 且当前站点存在可替换首页时生效，默认值为 `false`。

返回和失败行为：

- 成功返回 JSON 文本，包含 `success`、`mode=html`、`isHome`、`pageId` 和 `url`。
- 参数校验或保存失败时返回带 JSON 错误信息的 MCP 工具错误。

调用前确认：

- 新建还是更新。
- 更新时的页面 ID。
- 页面名称和友好 URL。
- 是否可能替换首页。

## `clear_site_cache`

用途：清理当前 MCP 端点对应站点的站点缓存。

参数：无参数。输入对象必须为空，不接受额外属性。

返回：缓存清理完成后返回当前站点 ID。

调用前必须说明该操作会清理当前站点缓存并获得用户确认。

## `list_enquiry_records`

用途：分页列出当前站点的**在线询盘记录**。用于分析历史询盘（Lead）阶段——反推转化漏斗漏点、定位高频空字段、统计产品询盘占比、评估线索审核/响应效率等。

参数：

```json
{
  "keyword": "string，可选，默认空；按表单提交数据关键字搜索",
  "status": "integer | string，可选，默认 -1；审核状态：-1 全部 / 0 未审核 / 1 已审核",
  "page": "integer | string，可选，默认 1；页码，从 1 开始",
  "pageSize": "integer | string，可选，默认 20，最大 100；每页数量"
}
```

参数规则：

- `keyword`：可选，默认 `""`；按表单提交数据关键字搜索（模糊匹配提交内容）。
- `status`：可选，默认 `-1`；审核状态 `-1` 全部、`0` 未审核、`1` 已审核。支持整数（`-1`/`0`/`1`）或字符串（`"-1"`/`"0"`/`"1"`）两种写法。
- `page`：可选，默认 `1`；页码，从 1 开始，最小 1。
- `pageSize`：可选，默认 `20`，最大 `100`；每页返回条数。
- `additionalProperties: false`：仅接受上列四个参数，不得传入其他属性。

返回结构（每条记录）：

- `form_info`：包含 `ID`、`Status`、`CrTime`（提交时间），以及当前询盘表单**可见字段**的「字段名称: 提交值」键值对。
- `product_list`：本次询盘关联的产品数组，保留产品名称、图片、规格、数量等原始字段。

排序：结果按提交时间（`CrTime`）**倒序**排列（最新提交在前）。

分析用法（详见 `references/funnel-framework.md` 分析面 F）：

- 拉取全量样本：传 `status=-1`，逐页翻完（`page` 从 1 递增，直到某页返回不足 `pageSize` 条）以覆盖全部历史询盘。
- 统计字段空置率：解析每条记录 `form_info` 的可见字段，找出最常留空的字段（= 用户抵触点），优化时优先删/后置该字段或改为选填。
- 统计产品询盘占比：汇总 `product_list`，看哪些产品被高频询盘，指导产品页 CTA 与询盘表单的产品预填（`EnquiryProduct`）。
- 结合 `status` 看审核/跟进状态，评估线索沉淀与销售响应效率。

> 该工具为**只读查询**，仅用于分析阶段；不修改任何数据。有 MCP 且 `test` 通过后即可在认证后直接调用。

## 推荐调用顺序

1. 准备当前站点 MCP 地址和 Bearer Token。
2. 使用 `test` 验证认证和连通性。
3. 使用 `list_page`、`list_news_class` 或 `list_product_class` 查询实际 ID；如果页面需要表单，优先使用 `list_custom_form` 列出已有表单并让用户选择。
4. 查询文章或产品时，使用 `get_news_list` 或 `get_product_list`；编辑具体内容前，使用 `get_news_info` 或 `get_product_info` 读取详情。
5. 新增文章或产品前，确认分类；需要素材时先调用 `upload_file` 或 `upload_product_image`。
6. 修改已有 AI 页面时，使用 `get_page_info` 获取页面信息和 `SourceCode`。
7. 生成或检查页面 HTML、文章或产品内容。
8. 对写操作展示变更摘要并取得确认；文章和产品需要单独确认发布状态。
9. 调用对应写入或维护工具。
10. 根据工具返回的成功信息或错误信息报告结果。
