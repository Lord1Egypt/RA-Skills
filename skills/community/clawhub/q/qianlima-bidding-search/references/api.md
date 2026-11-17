# 千里马 API 与脚本响应

## 认证与事实

默认生产地址 `https://skills.qianlima.com`，可通过既有 `QIANLIMA_BASE_URL` 配置。正式查询认证请求头是 `qianlimaApiKey`，每次值来自当前 `QIANLIMA_API_KEY`；JSON 请求使用 `Content-Type: application/json`。Key 只放在本次初始接口请求头，HTTP 重定向不转发。查询状态不选择或替换凭据；换 Key 不使原查询失效，由当前业务 API 最终鉴权。不自创认证头，不打印、记录或回显密钥，不写入快照。

正式账号能力真实联调前 `GET /api/user/verify` 确认账号与 Skill 权限；成功 data 的 `username` 仅供账号核对，不主动展示。此验证不是普通每次搜索的额外前置请求，也不作为匿名免费查询的前置。免费接口约定见下节。

查询 API 通用外层是 `code/msg/data/success`，以 code 200 判断业务成功，其他业务码按 API 返回处理。Skill 不按 data 的字段、类型、空值或对象编号再次判断成败。字段为空或 null 表示信息未公示，0 和 false 保留原意。

## 免费接口

免费普通标讯的请求、响应和错误处理见[免费搜索接口](api-free-search.md)，身份选路、费用意愿及任务衔接见[游客规则](guest-access.md)。匿名免费查询不以账号校验为前置；有 Key 免费查询不因携带 Key 自动变成积分查询。免费接口错误不能直接套用正式接口的全部错误码，不因错误自动改用收费接口。

## 按能力读取

| 能力 | 参考 |
| --- | --- |
| 免费普通标讯搜索 | [免费搜索协议](api-free-search.md)、[游客行为](guest-access.md) |
| 正式项目搜索、详情 | [普通项目](api-projects.md) |
| 正文、附件、时间线、来源链接 | [项目资源](api-project-resources.md) |
| 采购意向搜索、详情 | [采购意向](api-purchase-intentions.md) |
| 临期项目搜索、详情 | [临期项目](api-expiring-projects.md) |
| 公司搜索、8 类企业分析/电话 | [企业情报](api-enterprise-intel.md) |
| 当前积分、原文月度用量 | [积分权益](api-entitlement.md) |
| 搜索 ID 与枚举 | [枚举](enums.md) |

## 脚本 JSON

`scripts/qianlima_skill.py` 返回给 Agent；面向用户翻译成任务结论，不平铺字段。

| 字段 | 用途 |
| --- | --- |
| `ok/user_message/warnings` | API 业务结果与展示说明；展示/状态异常不覆盖已取得的业务结果 |
| `api_responses` | 每次调用的 path 与原始 response，完整保留状态、消息、未知字段、值和类型；连接/解析异常单列 transport_error |
| `total_count/returned_count` | 当前查询总数、本批数量；不合并独立分支总数 |
| `effective_query/request_query` | 实际生效、发送条件，核对原意未丢失 |
| `cards` | 三类项目的当前列表 |
| `rows` | 公司候选或企业分析结果 |
| `detail/full_detail` | 单条请求字段/完整支持详情 |
| `partial_success/retry_fields` | 多资源按各自 API 结果交付；详情与来源任一失败均保留另一项成功数据，不重放成功调用 |
| `full_text` | 普通项目正文对象 |
| `attachments/timeline` | 附件/进展节点数组 |
| `resolution` | 唯一对象定位结果 |
| `follow_up` | 保存 session_id/result_set_id、有效期、允许动作 |
| `area_expansion` | 支持区县筛选地区的零结果扩大建议；用户同意前不得执行 |
| `retry_policy` | 状态异常为 `restore_explicit_context_or_clarify_missing_fields`：先恢复明确上下文，只澄清缺项，不自动重查 |
| `balancePoints/frozenPoints/availablePoints/sourceUrlUsage` | 积分命令顶层事实 |

展示字段服务当前用户任务，不替代原始响应；不向用户平铺原始 JSON。展示或保存失败时依据 api_responses 交付已有数据，不重复成功调用。字段空值只表达“未公示”，不解释为“未返回”“接口未提供”或不存在。只有接口明确失败才保留失败；连接/解析异常表示未取得可解析响应。页码或定位信息不足时限制对应后续操作，不猜测、不修改本次成功状态。

本手册中的 current_query 指原成功输出的完整 effective_query；current_result_set 是指定结果的当前列表；focus_project 是最近唯一定位的项目。公司候选、时间线和项目列表不是同一组序号，按各自 follow_up 绑定。状态错误的 `requires_user_confirmation` 为 false、`needs_clarification` 为 true；先检查对话能否补全，不以缓存问题要求确认重搜。

三源搜索 API 列表返回 rowCount/pageCount/list；公司候选返回 total/currentPage/pageSize/list。总数只按接口总数字段说明，本批条数按实际返回列表说明；缺总数字段时不把本批条数当作总数。来源链接与详情页不同，只有明确索要才取来源链接。详情字段按当前源，支持位置检索不能推导详情新增字段。

金额为元，可转换为万元显示；空值未披露，数值 0 不是空值。附件状态保留 true/false/null；候选、分类、标的物等数组保持结构，不转字符串。

## 错误码


- `200`：成功。
- `401`：未认证。
- `429`：请求过于频繁。
- `10001`：API Key 无效。
- `10004`：接口参数异常。
- `10005`：详情不存在。
- `10006`：详情已撤回。
- `10007`：无权查看详情。
- `10010`：用户无权限查看该数据。
- `10011`：原文链接不存在。
- `10028`：地区权限不足。
- `10030`：积分余额不足。
- `10031`：积分扣除失败，请稍后重试。
- `10032`：积分账户未初始化或正在初始化。
- `10036`：原始公告来源链接本月获取次数已用完。
- `10037`：积分结算已超时，请重试。
- `10038`：请求正在处理中，请稍后重试。
- `10039`：价格版本已变化，请刷新权益后重试。
- `10040`：请求标识冲突，请重新发起请求。
- `10041`：项目完整正文未采集或为空。

错误码用于判断错误类别，面向用户时可转换为友好的中文提示，例如密钥问题、数据权限、积分余额、
月度次数、结算状态、请求频率、参数问题或数据暂不可用。

原业务错误原因始终保留，权益诊断最多补充一次积分/原文用量事实，不能覆盖错误。余额正常不证明地区权限可用或存在数据。正常零结果不诊断，网络或结算状态不明不自动重放计费调用。

状态缺失、过期、损坏时，已知公告 ID 可独立读取；原查询可由完整上下文恢复。明确结果集可跨会话引用，无需会话编号。不能准确恢复对象、源、全部条件或页码时只澄清缺项，不回退别的结果。多资源部分成功时交付成功部分，清理或保存故障不覆盖 API 成功、不触发重放。账号入口与故障反馈见 [账号](account-access.md)、[FAQ](faq.md)。

## 完整查询上下文

普通标讯恢复时，除 `result_type`、完整 `effective_query` 及精确分页外，保留已知的 `total_count`（用于识别不足整页的末页）及最近 `follow_up` 中的 `access_mode`（guest/authenticated）、`access_mode_source`（default/explicit）、`viewable_page_count`、`max_viewable_rows`、`delivered_position`、`seen_ids` 和 `pending_cards`。这些是上下文元数据，不能放入 API 查询体。`--access-mode` 显式选择优先于历史模式；default 表示自动选路，登录后可转正式，explicit 才是列表的主动选择。

`delivered_position` 是同条件结果序列已处理到的位置（从 0 起），`seen_ids` 为已交付公告 ID，`pending_cards` 为已取得但尚未交付的顺序记录。脚本返回整页时视为整页已交付；Agent 只展示部分时，下一次用 `--context-json` 传入调整后的实际位置、已展示 ID 和剩余卡片，不能使用未调整的结果引用跳过剩余内容。待展示记录优先从缓存交付，切免费时限制字段；缓存不是新接口权限或最新详情的证明。没有可靠进度时不猜、不重新播放历史页。

免费 `page_count` 是真实总页数，续查受 `viewable_page_count` 与 `max_viewable_rows` 限制。免费模式或分页异常会输出 `protocol_issues`、`continuation_blocked=true`，不生成可续查状态；原业务成功与原始响应仍保留。`link_notice` 为实际返回的免费列表公告详情入口的积分提示，官网入口不提示点击扣费，`access_facts` 为费用和限制事实；会话提示去重、接入意愿及授权由 Agent 按[游客规则](guest-access.md)处理。


`next/refine/search-company --next` 可用 `--context-json` 恢复明确原查询。`result_type` 必须已知；`effective_query` 完整复制上一轮成功输出，保留所有有效条件、准确 `currentPage` 和页大小，不使用原始简略输入或补猜默认。项目页大小是 `numPerPage`，公司是 `pageSize`，并保留 `companyName`。已知 `page_count` 可附带；0 或已到末页不多调，未知总页数但当前页准确可继续。

原结果集仍可用时最短调用如下，可省略或更换会话：

```bash
python3 scripts/qianlima_skill.py next --result-set-id RESULT
python3 scripts/qianlima_skill.py refine --result-set-id RESULT --query-json '{"hasAnnex":0}'
```

例如原免费查询已完整交付第 1 页的 30 条记录，完整上下文需复制实际输出，而不是只摘取筛选条件：

```json
{"result_type":"project","effective_query":{"keywordGroups":[{"keywords":["物业"],"matchScopes":[2,9]}],"beginTime":"2026-11-01 00:00:00","endTime":"2026-11-15 23:59:59","currentPage":1,"numPerPage":30},"page_count":20,"total_count":600,"access_mode":"guest","access_mode_source":"explicit","viewable_page_count":10,"max_viewable_rows":300,"delivered_position":30,"seen_ids":["example-1","example-2","example-3","example-4","example-5","example-6","example-7","example-8","example-9","example-10","example-11","example-12","example-13","example-14","example-15","example-16","example-17","example-18","example-19","example-20","example-21","example-22","example-23","example-24","example-25","example-26","example-27","example-28","example-29","example-30"],"pending_cards":[]}
```

示例 ID 为结构占位，实际调用用真实已交付 ID；全部 `effective_query` 字段及状态值复制原成功输出。将完整对象作为 `--context-json` 的值传给 `next`；`refine` 传同一对象并加 `--query-json` 的变化字段。只有原页已全部交付且没有待展示缓存时，同页大小下一页才直接加 1。部分展示时，例如只交付前 10 条，位置为 10、`seen_ids` 为这 10 条 ID、`pending_cards` 为剩余 20 条原始卡片（保留 URL）；下次先交付缓存，不跳页。

细化只改 patch 并回第一页。跨模式按实际交付位置换算，见[游客规则](guest-access.md#分页限制与续查)，不能沿用不同页大小的页码。采购意向/临期保留自身全部有效条件，例如：

```json
{"result_type":"purchase_intention","effective_query":{"keywords":["物业"],"startPlanPurchaseDate":"2026-11","endPlanPurchaseDate":"2027-01","currentPage":1,"numPerPage":10}}
```

```json
{"result_type":"expiring_project","effective_query":{"keywords":["物业"],"beginServiceExpireTime":"2026-10-12","endServiceExpireTime":"2027-04-12","currentPage":1,"numPerPage":10}}
```

上述各例仅在与原成功输出全部条件一致时使用；有其他地区、金额、排序等字段须全部复制。公司样例见 [企业能力](capabilities/enterprise-intelligence.md)。原 API `effective_query` 无须追加金额确认字段，已执行金额直接继承；新的/改变的小额由 Agent 自行核对原话单位。完整上下文或缓存页大小超过三源 100/公司 20 时先纠正，不静默缩小改变分页；新查询默认规则不变。

`AREA_SCOPE_UNSUPPORTED`：指定区县目前只能返回更大范围，查询未发出。按 [地区规则](../SKILL.md#地区) 确认实际范围后重试，不自动替换地区编号。


## 账号接口与凭据配置

账号脚本独立使用 `https://ai.qianlima.com`（前端同源 `/api` 契约），不从查询域名推导，不接收对话任意 URL；HTTPS 不跟随重定向。账号响应 `code/message/data/requestId` 的成功码为 0，不套用查询的 200。

| 接口 | 用途 |
|---|---|
| `GET /api/legal?type=TERMS`、`PRIVACY` | 脚本在 verify 内部取得后端必填版本；Agent 无需调用或传回 |
| `POST /api/auth/sms/send` | phone 发码；成功 data 可为 null |
| `POST /api/auth/login` | phone/smsCode/agreementVersion/privacyVersion/sourceCode；新用户注册，老用户登录 |
| `POST /api/api-keys/{keyId}/reveal` | 默认 Key 不完整时用本次 Bearer token 获取；不另行创建、重置、启用 Key |
| `GET /api/points/account` | 同一 token 读取 availablePoints，0 有效；赠送与实际余额分别判断 |
| `POST /api/auth/logout` | Key 和余额请求结束后尽力清理临时 token，失败不撤销 Key |

### 调用和状态

账号命令不选择宿主、不自动读写平台配置。工具返回 Key 后的保存、加载和自动接续统一见[API Key 配置与使用](credential-configuration.md)。

`python3 scripts/qianlima_account.py prepare` 在本地取得唯一引导文案，不发起网络请求；无查询任务加 `--no-query`。`--has-key` 仅在执行侧已确认有 Key 时使用。只有用户明确要求换号或换 Key 才进入更换流程；首次配置不询问替换，不增加网页探测。

`python3 scripts/qianlima_account.py register --input-stdin` 从 stdin 接收 JSON。发码仅需 `action=send`、`phone`，不要求、不比对协议版本，也不重新请求协议接口；后端发码请求仅包含 `phone`。验证登录仅需 `action=verify`、`phone`、`smsCode`。验证码必须是六位 ASCII 数字字符串，保留前导零；兼容 `code` 别名，由脚本统一转换为后端的 `smsCode`。两个字段同时传入且不一致时返回 `code_conflict`，不自行选取。脚本在提交登录前自动获取后端必填的 `agreementVersion` 和 `privacyVersion`，与固定来源码一起填入登录请求；Agent 无需记忆或传回版本，旧调用额外传入的版本字段不参与组装。prepare 不获取版本，verify 不比较版本、不重复获取或自动重试。版本接口失败或返回无效版本时以 `stage=legal` 停止，尚未提交验证码，不登录、不取 Key、不写配置、不重发短信；不得让用户补版本或误报验证码错误。默认无需 `--credential-fd` 或管道。发码成功回执为 `status=sms_sent`、本次提交的完整 `phone` 和 `expires_in_seconds`，不再返回 `phone_masked`；号码可在本次登录对话中原样展示。`consent` 为可选兼容字段：省略或传 JSON 布尔值 `true` 均可；显式传 `false` 返回 `consent_required` 并停止，不自动改为 `true` 重试；字符串、数字或 `null` 返回 `invalid_consent`。Agent 仍须依据本轮用户明确的发码／登录请求执行，用户取消或仅引用历史／示例号码时不调用脚本；该字段不表示已阅读或同意法律协议，不为此追加协议确认。手机号和验证码不写命令行参数。send 与 verify 显式分开，不隐式重发；登录失败按接口实际结果反馈，不将本地参数缺失解释为协议变化。


推荐输入结构（通过 stdin 提交；示例值只用于说明，不触发真实请求）：

```json
{"action":"send","phone":"13800000000"}
```

```json
{"action":"verify","phone":"13800000000","smsCode":"012345"}
```

输入校验失败时，结果包含 `stage=input`、`request_sent=false` 和 `agent_instruction`，表示本次尚未请求账号接口。参数遗漏或别名冲突由 Agent 根据本轮已提供内容修正，不误报为后端验证码错误、不重发短信；用户输入确有缺失或歧义时才澄清。该标记只适用于当前调用，不能推断此前调用未发生。

登录请求的 `sourceCode` 由本主包固定为 `bb3b4102f584028c3830df37`，与网站入口的 `source` 相同。无需用户提供，stdin 中的来源字段不能覆盖包内值。账号流程中仅登录请求带此字段，不写入发码、协议、余额或退出请求；免费搜索的同名来源字段由查询脚本按[免费接口](api-free-search.md#来源传递)独立注入，不放入用户查询参数；不为来源额外请求或自动重试。不能仅凭客户端传参就宣称后台归因成功；老用户不要求来源回填。

默认验证成功返回 `status=credential_available`、完整 `api_key`、`login_completed=true`、`configuration_written=false`、`current_environment_loaded=false`，另返回本次提交的完整手机号 `phone`、新老用户标识、实际余额和退出状态。Agent 在已获保存授权及替换条件满足时立即按用户提供 Key 的同一规则配置；不要等待用户重发 Key 或配置指令。取得 Key 和脚本退出码 0 均不表示已保存或加载。

失败、取消或结果未知时不返回 `api_key`；验证码失败不获取 Key、不保存、不重发。余额或退出失败不否定已取得的 Key，分别按实际字段反馈。脚本不输出验证码、token 或完整认证原响应。显式使用旧 `--credential-fd N` 的调用仍返回不含 Key 的 `credential_ready`，无效管道仍拒绝登录；普通会话不使用此兼容入口。查询端继续读取 `QIANLIMA_API_KEY`，不负责平台配置。

认证响应不进入查询 `api_responses`；临时 token／验证码不持久保存，不做跨调用认证恢复。用户交互见 [账号接入](account-access.md)，失败见 [FAQ](faq.md)。
