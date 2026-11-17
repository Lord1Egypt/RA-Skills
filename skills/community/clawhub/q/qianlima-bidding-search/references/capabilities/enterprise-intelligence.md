# 企业情报与企业名称

先区分要公告列表还是企业资料／关系统计：指定采购单位的公告、中标单位的项目、代理机构代理的标讯均走 [普通项目搜索](project-search.md)，通过位置 4／5／6 表达角色，不强制先查公司 ID。以下主体流程只适用于本页的企业能力。

## 公司候选与主体确认

明确登记全称直接 `enterprise`，大学、医院、机关不要求公司后缀；已确认主体复用，不加一次候选查找。明确“找公司”或简称、品牌、集团泛称需要消歧时先 `search-company`，候选在 `rows`，保存独立的 `follow_up`。

```bash
python3 scripts/qianlima_skill.py search-company --query-json '{"companyName":"腾讯","currentPage":1,"pageSize":10}'
python3 scripts/qianlima_skill.py search-company --next --result-set-id RESULT
python3 scripts/qianlima_skill.py search-company --next --context-json '{"result_type":"company_candidates","effective_query":{"companyName":"腾讯","currentPage":1,"pageSize":10}}'
```

明确原结果可省略或更换会话。缓存不可用时，完整复制原成功输出的 `effective_query` 为上下文（样例是名称与分页全部条件）；必须有 `companyName/currentPage/pageSize`，不取最近查询、不猜页码或静默缩小超限页大小。缺项才澄清；不新增用户确认步骤。

搜索支持全称片段、简称和别名；展示候选名称与注册地址，让用户确定单一主体，不按排名、中标次数或招标次数替选，不自动展开集团。次数 0 不证明没有实际业务。候选为空不编造名称。

用户选定后，后续企业分析和电话接口只传确认的 `companyName`，不传候选 `companyId` 或自创确认参数。公司候选分页与项目列表隔离，不使用项目 `next`。完整字段见 [企业 API](../api-enterprise-intel.md)。

## 何时使用

- 查合作供应商、合作甲方/客户、采购地区、中标地区、直接/潜在竞争对手、工商信息或联系人电话。
- 指定单位的采购、中标、代理公告列表走 [普通项目搜索](project-search.md)；“作为投标方”需区分中标方与全量参标意图。

执行动作：`enterprise --kind <kind>`。

## kind 选择

| 用户意图 | kind |
| --- | --- |
| 某甲方合作供应商 | `partners` |
| 某企业采购地区 | `area-distribution` |
| 某供应商合作甲方/客户 | `principals` |
| 某供应商中标地区 | `winning-area-distribution` |
| 同场竞标过的直接对手 | `co-bidder-competitors` |
| 潜在竞争对手 | `potential-competitors` |
| 工商基本信息 | `business-info` |
| 联系人或电话 | `contacts` |

## 参数与连续追问

- `companyName` 必填，只传已核验的正式名称。
- 合作供应商、合作甲方、采购地区和中标地区可传 `beginTime/endTime/sortType`；直接和潜在竞对不得传 `sortType`；工商信息只传 `companyName`；联系电话只传 `companyName/phoneType/currentPage/numPerPage`。
- 关系、地区和竞对能力可传 `beginTime/endTime`；不传时接口默认近一年。
- `sortType: 1` 按次数，`2` 按金额；用户未指定时使用接口默认。
- 工商信息和电话不继承时间条件。
- 切换企业关系能力时，沿用企业名称和仍适用的时间、排序条件。
- 联系人翻页时复用最近确认的企业名称，`currentPage + 1`；不使用项目结果的 `next`。
- 企业与项目同时存在时，“它的联系人”指代不清，先确认要查企业联系人还是项目联系人。

## 结果与空结果

- 关系类结果只代表接口覆盖期内的公告关系，不等同于企业全部客户、供应商或竞对。
- 工商信息按正式字段展示中文名称：企业名称、经营状态、企业类型、法定代表人、注册资本、成立日期、注册号、组织机构代码、统一社会信用代码、行业、营业期限、核准日期、登记机关、注册地址、经营范围。
- 企业联系电话属于高敏付费数据；只在用户明确索要联系人、电话或联系方式时调用，分页和数量按 `query-strategy.md`。
- 空结果先重新核对正式名称；名称正确后再询问是否扩大时间范围，不能直接断言“没有客户/竞对/联系人”。
