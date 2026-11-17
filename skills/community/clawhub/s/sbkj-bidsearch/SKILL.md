---
name: sbkj-bidsearch
description: 面向世舶科技（武汉）有限公司“保标招标”产品的招投标数据接口业务 Skill。用于根据自然语言查询招中标项目、把 AI 重写条件转换为普通搜索参数、处理搜索列表到项目详情的调用链、获取正文与官方结构化数据、查询附件和采集源网址、查询合同、分析企业画像、检索拟在建项目，以及使用行业推理、分类推理和正文结构化接口。涉及保标招标接口调用、Python脚本联调、API客户端封装、参数排查或业务流程说明时使用。
---

# 保标招标接口业务助手

## 使用前置条件

- 外部接口调用必须配置 API Key。优先从环境变量 `BAOBIAO_ZTB_API_KEY` 或项目现有安全配置读取，禁止把真实 Key 写入代码、Skill、日志、示例或提交记录。
- API 网关基地址为 `https://gate.gov-bid.com/outer-gateway/bid`，请求地址按参考文档拼接 `?key={API_KEY}`。
- 如果当前环境没有 HTTP/MCP/API Client 能力，只能生成调用方案、请求示例、测试样例或排查建议，不要声称已经调用成功。
- 当前 Skill 的品牌上下文是：公司“世舶科技（武汉）有限公司”，产品“保标招标”。对外宣传、产品介绍或用户可见文案中使用完整名称“世舶科技（武汉）有限公司保标招标”，不夸大接口能力，不虚构客户、数据规模或效果。

## 总体工作方式

1. 先识别用户意图和业务场景，不要按接口名称机械选择。
2. 自然语言检索优先执行“AI 重写条件 → 状态完成 → 转换普通搜索参数 → 普通搜索列表”。
3. 搜索记录必须保存 `projectId/id + publishTime`，二者是后续项目详情调用的联合身份。
4. 区分列表摘要、正文详情、官方结构化详情、附件和采集源网址；根据用户需要选择单接口或组合调用。
5. 多个项目的正文、结构化详情和附件查询可并行；单个项目详情页也可并行获取互不依赖的数据。
6. 成功判断同时检查 HTTP 状态、响应 `code` 和业务 `subCode`；不要只根据 HTTP 200 判断成功。
7. 输出中区分官方字段、接口原始字段和 AI 推断字段，不能把 AI 推断结果伪装成官方结构化结果。
8. 详细参数和字段定义按需读取 `references/` 下对应文件，不要一次性加载全部接口资料。

## Agent执行优先级

按照以下优先级执行，减少 Agent 在底层接口和实现语言之间反复判断：

1. 用户要求“查询、测试、联调、调用接口”时，优先使用 Python 脚本；先检查 `BAOBIAO_ZTB_API_KEY`，再调用脚本。
2. 用户要求“把 AI 条件转换成普通搜索参数”时，优先运行 `scripts/compile_search_condition.py`，不要手工重写 JSON。
3. 用户要求“直接调用某个接口”时，使用 `scripts/invoke_baobiao_api.py`，通过 `--endpoint` 和 JSON 请求体调用，不要在回答中拼接含 Key 的 URL。
4. 用户要求实现正式项目功能时，根据目标项目实际技术栈实现；不要默认假设使用 .NET、Java 或其他特定语言。
5. 用户只要求解释方案或分析接口时，不调用外部接口，读取对应 `references/` 并给出调用链和参数说明。
6. 脚本返回非零退出码时，先解释参数错误、网络错误、权限错误或业务错误，再决定是否需要修改请求；不要把失败包装成成功。

### 脚本调用模板

```powershell
$env:BAOBIAO_ZTB_API_KEY = "从安全渠道取得的Key"
python scripts/invoke_baobiao_api.py `
  --endpoint searchProjectApi `
  --data-file request.json
```

脚本输出约定：正常 JSON 输出到 stdout，错误输出到 stderr；退出码 `0` 表示成功，`1` 表示调用或输入错误，`2` 表示缺少 API Key 或参数错误，`3` 表示接口返回业务失败。API Key 只在当前进程临时提供，不写入 Skill 或项目文件。

## 业务路由

| 用户意图 | 标准处理 |
| --- | --- |
| 自然语言搜索招中标项目 | 读取 `natural-language-search-workflow.md`，AI 重写后调用普通搜索 |
| 已有结构化筛选条件搜索 | 读取 `search-condition-mapping.md` 和 `api-reference.md`，直接调用普通搜索 |
| 根据项目编号查项目 | 调用项目编号搜索，再按 `projectId + publishTime` 进入详情链路 |
| 查看公告全文 | 调用正文详情 |
| 提取预算、中标金额、联系人、投标企业 | 调用官方结构化详情 |
| 下载或查看附件 | 调用附件列表；正文详情中的附件概要不能替代下载接口 |
| 跳转原始来源 | 优先使用结构化详情的 `collectUrl`，缺失时调用采集源网址 |
| 查询合同 | 读取 `contract-workflow.md`，调用合同搜索，必要时进入项目详情链路 |
| 查询企业基本情况、联系人、客户、供应商 | 读取 `company-workflow.md`，按需调用企业画像接口组 |
| 查询拟在建项目 | 读取 `planned-project-workflow.md`，使用拟在建项目独立模型 |
| 推理行业、分类或从正文抽取字段 | 读取 `ai-workflow.md`，明确标记 AI 推断结果 |

## 自然语言搜索硬规则

将 `aiSearchSubmitPolling` 视为普通搜索的条件编译器，不要让 Agent 直接凭空拼装复杂普通搜索参数。

1. 提交 `userQuery`，取得 `requestKey`。
2. 按接口契约轮询处理状态；只有 `status=completed` 才继续。
3. `processing`、`search_rewrite_done`、`area_code_done`、`industry_done` 表示仍在处理，不能提前搜索。
4. `failed` 必须返回 `errorMsg` 或可定位的失败原因。
5. 将 `searchCondition`、`areaCode` 和 `industryCodes` 转换成普通搜索请求。
6. 开始日期补 `00:00:00`，结束日期补 `23:59:59`。
7. 多个 `subjects` 默认按 OR 语义使用英文竖线连接；如果用户明确要求同时出现，改用空格并说明语义。
8. `enterpriseName` 映射到 `companyName`；`projectClassIds` 映射到 `projectClassID`；`purchaseTypeId` 映射到 `purchaseTypeID`。
9. 行业编码按一级、二级、三级分别合并去重。
10. `subcontractFlag` 在普通搜索接口没有明确对应字段，必须提示“未透传”，不能静默丢弃。
11. 普通搜索中的 `inCludeKW` 拼写必须保持接口原名。
12. 普通搜索 `pageNumber` 不超过 50；需要总数时使用接口约定的 `pageNumber=0`，并说明不会返回完整记录。

如果文档没有明确轮询请求如何携带 `requestKey`，先标记接口契约待确认；不要猜测参数名，也不要伪造“已完成”。

## 列表到详情的业务关系

- 搜索列表接口只负责发现和展示摘要，不是完整内容来源。
- 正文详情接口 `getZTBProjectDetail` 负责 HTML 原文、标题、展示字段和正文附件概要。
- 结构化详情接口 `getZTBStructreDetail` 负责项目编号、标段、预算、中标金额、时间、地点、主体联系人和投标企业等官方业务字段。
- 附件列表接口 `getZTBProjectFiles` 负责下载 URL、后缀、大小和处理状态。
- 采集源网址接口 `getCollectUrl` 负责原始来源跳转；结构化详情已有 `collectUrl` 时优先使用它。
- 完整项目详情页通常并行获取正文、官方结构化详情和附件；只有用户要求原始来源或 `collectUrl` 缺失时才补充采集源网址。
- 正文金额是展示值，结构化预算/中标金额是分析值；两者不能无提示混用。

## 统一项目身份与结果模型

使用以下逻辑模型组织结果：

```text
BidProjectView
├── identity: projectId, publishTime
├── summary: 搜索列表摘要
├── content: 正文详情和 HTML
├── structured: 官方结构化详情
├── attachments: 可下载附件
└── source: collectUrl, sbkjBidUrl
```

当项目 ID、发布时间、详情数据或附件数据缺失时，保留缺失状态并说明原因，不用其他字段猜补。

## 响应、兼容和安全规则

- 兼容文档中字段大小写差异，例如 `costtime/costTime`、`startdate/startDate`。
- `data` 可能是数组、对象或分页对象，按具体接口解析。
- 标题和正文可能包含 HTML 高亮标签；同时保留原文版和清洗后的展示版更安全。
- 金额可能是“16.8万”等带单位字符串，不能直接按数字解析。
- `null`、空数组、无附件和接口失败要区分处理。
- 记录真实请求时脱敏 URL 中的 `key`，日志不得打印完整 Key。
- 对外输出时优先使用产品名称“保标招标”，技术说明中可注明其所属公司“世舶科技（武汉）有限公司”。

## Skill脚本：Python 3 封装约定

当用户要求直接运行接口联调脚本、验证接口参数或生成普通搜索请求时，使用 `scripts/` 下的 Python 3 脚本，不要把脚本逻辑复制到项目 Controller 中。

- 使用 Python 3.10+ 语法和标准库优先，避免为简单 HTTP/JSON 调用引入额外依赖。
- 使用 `argparse` 提供命令行参数，使用 `json` 处理请求和响应，使用 `urllib` 完成基础 HTTP 调用。
- API Key 只能从环境变量或显式安全配置读取，默认使用 `BAOBIAO_ZTB_API_KEY`；禁止写入脚本、示例、日志和错误信息。
- 脚本入口使用 `main()` 和 `if __name__ == "__main__"`，通过明确退出码表示成功、参数错误、接口错误和业务失败。
- 对公共函数、关键转换函数和异常兜底路径编写中文 docstring，说明参数、返回值和失败原因。
- 请求 JSON 使用 UTF-8；输出 JSON 时保留中文，错误信息输出到 stderr，正常结果输出到 stdout。
- 脚本只负责确定性的接口调用、参数转换和离线验证；复杂业务编排、持久化、权限和正式 API 对外能力应放在调用方的正式业务服务中。
- AI 重写轮询参数未在接口文档中明确时，脚本不能自行猜测轮询协议；应先输出待确认契约或等待用户提供接口约定。

## 参考资料导航

- 总接口、枚举和字段：`references/api-reference.md`
- 自然语言条件重写与普通搜索：`references/natural-language-search-workflow.md`
- 列表、正文、结构化、附件和来源关系：`references/project-detail-workflow.md`
- 合同搜索：`references/contract-workflow.md`
- 企业画像：`references/company-workflow.md`
- 拟在建项目：`references/planned-project-workflow.md`
- AI 行业、分类和正文结构化：`references/ai-workflow.md`
- 枚举、响应兼容和异常：`references/enums-and-response-rules.md`
- 品牌、产品介绍和运营宣传口径：`references/brand-and-promotion.md`

## 可执行脚本

- `scripts/invoke_baobiao_api.py`：从环境变量读取 API Key，安全调用指定保标招标 POST 接口。
- `scripts/compile_search_condition.py`：将 AI 重写接口返回的 JSON 转换为普通搜索接口请求 JSON；支持从文件或标准输入读取。

调用脚本前先配置 `BAOBIAO_ZTB_API_KEY`。脚本不会把 Key 写入输出或错误信息。AI 重写轮询接口的具体请求格式在原始文档中未完全明确，因此脚本只负责提交和条件编译，不擅自猜测轮询请求参数。
