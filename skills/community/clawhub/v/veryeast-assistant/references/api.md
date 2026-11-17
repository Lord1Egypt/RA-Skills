# veryeast 助手工具参考

调用前必读。**本文件决定每个工具的参数名、格式、必填项、码表——不猜、不试。** SKILL.md 讲编排与话术，本文件只讲参数。

## 基本信息

- **调用方式**：统一 `node scripts/veryeast-client.js '<参数json>' [工具名]`
- **认证**：所有工具都需要 api_key（登录凭证）。已配置后调用时自动带，**无需手动传**。
- **怎么传值**：参数**全传中文/自然值**，不要传 code/码值。**唯一例外：`search_job` 的六个筛选参数（`area`/`company_industry`/`education`/`room_board`/`work_mode`/`position`）同时接受中文和反查拿到的准确 code，两种都识别**——推荐直接传中文（省一次反查）。薪资、年份、月份也**传字符串**（如 `"6000"`、`"2022"`）——只有 `search_job.page` 是数字、`apply_job.confirm` 是布尔。传了无法识别的值会被拒并提示，不会悄悄丢弃。
- **分页**：`page` 默认 1，每页固定 20 条；响应 `page_size` 即本页实际条数（server 已重写），翻页用 `page`。

## 工具总表

| 工具 | 干什么 | 需要 api_key |
|------|--------|------|
| `search_job` | 搜索职位 | ✅ |
| `resolve_area` | 地点中文 → 地点 code | ✅ |
| `resolve_option` | 小类目中文 → code | ✅ |
| `resolve_job` | 职位分类 → code | ✅ |
| `get_resume` | 读完整简历（改简历前先读拿 id） | ✅ |
| `update_base` | 改基本信息（**birthday 必填，年-月**） | ✅ |
| `update_job_status` | 改求职状态（**影响简历曝光**；离职-随时到岗/在职-月内到岗/在职-考虑机会/在职-暂不考虑） | ✅ |
| `update_description` | 改自我介绍 | ✅ |
| `add_intention` / `update_intention` | 加/改求职意向（**company_industry 必填**） | ✅ |
| `add_work` / `update_work` | 加/改工作经历（**company_name、begin_year、begin_month、salary、company_industry 必填**） | ✅ |
| `add_edu` / `update_edu` | 加/改教育经历 | ✅ |
| `apply_job` | 投递职位（**需 confirm**） | ✅ |

---

## 搜索

### search_job

```bash
node scripts/veryeast-client.js '{"keyword":"酒店前台","area":"杭州","work_mode":"全职"}'
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | ✅ | 职位关键词 |
| page | number | 否 | 页码，默认 1 |
| area | string | 否 | 地区，中文（如 "杭州"） |
| company_industry | string | 否 | 行业，中文（如 "酒店业"） |
| education | string | 否 | 学历，中文（如 "本科"） |
| room_board | string | 否 | 食宿，中文（如 "提供食宿"） |
| work_mode | string | 否 | 性质，中文（全职/兼职/实习/临时） |
| salary_min / salary_max | string | 否 | 薪资区间，纯数字字符串（如 `"6000"`） |
| position | string | 否 | 职位类别（仅按求职意向推荐时传） |

返回：职位列表，每条含职位名/薪资/地点/公司/经验学历要求 + `job_detail_url`（职位详情链接）+ `company_url`（企业主页链接）。

---

## 反查（中文/模糊输入 → code）

| 工具 | 参数 | 返回 | 用法 |
|------|------|------|------|
| `resolve_area` | `query`：地点中文/拼音 | 匹配结果或候选列表 | "杭州" → 拿 area code |
| `resolve_option` | `key` + `query` | 匹配结果或候选列表 | `key="degree" query="本科"` → 拿 degree code |
| `resolve_job` | `query`：职位中文 | 匹配/候选（一对多） | "大堂副理" → 多候选 |

- `resolve_option` 的 `key` 取值：`gender` / `degree` / `work-year` / `job-status` / `salary-mode` / `desired-salary` / `currency` / `work-mode` / `company-industry-v1` / `major` / `language` / `accommodation`
- `resolve_job` 一对多（"总经理" → 总裁/总经理、副总裁/副总经理…）：**多候选必须让用户选**，禁止自作主张
- 反查拿到的 code 可直接用于**搜索筛选**（`search_job` 六个筛选参数都同时接受中文和 code）；简历写操作的参数一律传中文，不传 code

---

## 简历读

### get_resume

```bash
node scripts/veryeast-client.js '{}' get_resume
```

返回完整简历。**所有写操作的 `id` 都从这里拿**。section 名和字段名以返回的实际结果为准，不要假定。

---

## 简历写

### update_base — 基本信息

```bash
node scripts/veryeast-client.js '{"true_name":"林念清","gender":"女","birthday":"2003-01","current_location":"杭州"}' update_base
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| true_name | string | **✅** | 姓名 |
| gender | string | **✅** | "男"/"女" |
| **birthday** | string | **✅** | **格式 年-月，如 `2003-01`**；传 `2003-01-01` 会被拒 |
| current_location | string | **✅** | 现居地，中文地点 |
| wechat | string | 否 | 微信 |
| work_date | string | 否 | **格式 年-月**，如 `2020-01`；**影响工龄**——有工作经历时填**最早工作的开始年月**，否则工龄算"应届生"；应届生（graduate_student="是"）时不传 |
| graduate_student | string | 否 | 是否应届：`"是"` / `"否"`（或 `"0"` / `"1"`） |

> ⚠️ **改基本信息 = 全量覆盖**：true_name / gender / birthday / current_location **四者必填**，漏了会被拒。改前先 `get_resume` 拿到当前值带上。
> ⚠️ **birthday 和 work_date 都只收 年-月**。`2003-01-01`、`2003/01/01`、`2003年01月01日` 都会被拒。

### update_job_status — 求职状态

```bash
node scripts/veryeast-client.js '{"status":"在职-考虑机会"}' update_job_status
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | **✅** | `离职-随时到岗` / `在职-月内到岗` / `在职-考虑机会` / `在职-暂不考虑`（或对应 code 1/4/2/3） |

> ⚠️ 求职状态是 profile 顶部公开标识，**招聘方可见，直接影响简历曝光**——改动要谨慎，确认用户意图再执行。

### update_description — 自我介绍

```bash
node scripts/veryeast-client.js '{"content":"我的自我介绍…"}' update_description
```

`content` 必填，≤2000 字符；**不支持清空**（空白/纯空格会被明确拒绝）——想清掉只能官网/App，或覆盖写成新内容。

### add_intention / update_intention — 求职意向

```bash
node scripts/veryeast-client.js '{"position":"前厅部经理","work_mode":"全职","locations":"杭州","desired_salary":"3001-5000元","company_industry":"酒店业"}' add_intention
# 修改：id + 没改的必填项带当前值（全量覆盖）
node scripts/veryeast-client.js '{"id":"51483836","position":"前厅部经理","work_mode":"兼职","locations":"杭州","company_industry":"酒店业"}' update_intention
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| position | string | **✅** | 意向职位，中文（如 "前厅部经理"） |
| work_mode | string | 否 | 全职/兼职/实习/临时 |
| locations | string | **✅** | 意向地点，逗号分隔（"杭州,北京"） |
| desired_salary | string | 否 | 期望薪资，档位文本（如 `"3001-5000元"`）或档位 code，见档位表 |
| **company_industry** | string | **✅** | 意向行业，中文，**≤5 个**，逗号分隔（"酒店业,餐饮业"） |

> ⚠️ **position / locations / company_industry 必填**。修改（update_intention）同——全量覆盖，改前先 `get_resume` 拿到当前值带上。
> 意向行业一律用 `company_industry`（中文，≤5 个）。薪资类型/币种/是否面议**不要传**——更新意向时你网页端设的年薪/外币/面议会保留；新增则默认 月薪/人民币/不面议。

### add_work / update_work — 工作经历

```bash
node scripts/veryeast-client.js '{"company_name":"阿里","position":"前厅部经理","begin_year":"2022","begin_month":"1","is_current":"true","salary":"8000","company_industry":"酒店业"}' add_work
# 修改：id + 没改的必填项带当前值（全量覆盖）
node scripts/veryeast-client.js '{"id":"10938855","company_name":"阿里","begin_year":"2022","begin_month":"1","salary":"8000","company_industry":"酒店业"}' update_work
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| company_name | string | **✅** | 公司名 |
| position | string | 否 | 职位名，**纯文本**（支持自定义） |
| job_responsibilities | string | 否 | 工作内容 |
| **begin_year** / **begin_month** | string | **✅**（两个都必填） | 开始年/月，纯数字字符串（如 `"2022"` / `"1"`）——**漏 begin_month 写后读回会发现 begin_year/is_current 不对**，必填 |
| end_year / end_month | string | 否 | 结束年/月，纯数字字符串（`is_current="true"` 时不要传） |
| **is_current** | string | 否 | `"true"` = 工作到至今；`"false"` = 已离职。**传字符串，别传裸布尔**。**不传默认"在职"**——已结束的历史经历要显式传 `"false"` + 结束年/月，否则会落成在职 |
| **salary** | string | **✅** | 月薪，纯数字（如 `"8000"`） |
| **company_industry** | string | **✅** | 行业，中文 |

> ⚠️ **company_name / begin_year / begin_month / salary / company_industry 必填**（begin_year 必须配 begin_month）。修改（update_work）同——全量覆盖，改前先 `get_resume` 拿到当前值带上。
> 薪资类型/币种/是否展示**不要传**——薪资类型与币种平台强制 月薪/人民币，是否展示固定为 **公开**（简历薪资默认对外展示，无法改为保密）。

### add_edu / update_edu — 教育经历

```bash
node scripts/veryeast-client.js '{"school":"浙江大学","major":"酒店管理","degree":"本科","begin_year":"2018","begin_month":"9","end_year":"2022","end_month":"6"}' add_edu
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| school | string | **✅** | 学校名 |
| major | string | **✅** | 专业名（必填） |
| degree | string | **✅** | 学历，中文（初中/高中/大专/本科/硕士/博士…） |
| **begin_year** / begin_month | string | **✅**（begin_year） | 入学年/月，纯数字字符串 |
| **end_year** / end_month | string | **✅**（end_year） | 毕业年/月，纯数字字符串 |

> ⚠️ **school / major / degree / begin_year / end_year 必填**。修改（update_edu）同——全量覆盖，改前先 `get_resume` 拿到当前值带上。

---

## 投递

### apply_job

```bash
node scripts/veryeast-client.js '{"job_id":"1114318","confirm":true}' apply_job   # 用户明确同意后直接投出
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| job_id | string | **✅** | 职位 id（从 search_job 结果取；**本文档示例 id 仅演示**——旧 id 可能失效报"职位无效"，一律以实际搜索返回为准） |
| confirm | boolean | 否 | `true` 才真正投递；**默认 false = 不会投**，返回 `pending_confirm` 提示补 confirm |

> **投递门控**：必须先向用户展示职位信息并取得明确同意，再带 `confirm:true` 调用（一次投出）。若漏带 confirm（响应返回 `pending_confirm`），补上 `confirm:true` 重调即可。**禁止未征得同意就投。**

---

## 易错字段（最高优先级）

| 字段 | 正确格式 | 常犯错误 |
|------|----------|----------|
| `birthday` / `work_date` | **`年-月`**，如 `2003-01` / `2020-01` | `2003-01-01` / `2003/01/01` / `2003年01月01日` 全拒 |
| `update_base` | true_name / gender / birthday / current_location **四者必填** | 漏任一会被拒；改 base 前先 get_resume 拿到当前值带上 |
| `is_current` | 字符串 `"true"` / `"false"` | **别传裸布尔 `true`**（会被输入校验直接拒）；`"true"` 时不要传结束时间 |
| `salary`（add_work） | 月薪数字 `"8000"` | 漏传 → "工作要月薪" |
| `company_industry`（add_intention） | 中文行业，**≤5 个** | 传 code 或超过 5 个 → 被拒 |
| `desired_salary` | 档位文本 `"3001-5000元"` | 传 `"3001-4000元"`——**这档不存在**，最近档 3001-5000 |
| add_work / add_edu 必填 | work: company_name+begin_year+**begin_month**+salary+company_industry；edu: school+major+degree+begin_year+end_year | 漏传 → 直接报"必填"；work 漏 begin_month → 写后读回会发现 begin_year/is_current 不对 |

## 码表

### 期望薪资档位（desired-salary）

**用户给区间时选「包含该区间的档位」**，并如实告诉用户落档（如 3001-4000 → 落 3001-5000）。

**月薪**（code 2-11）：

| code | 范围 | code | 范围 |
|------|------|------|------|
| 2 | 2001-3000 | 7 | 10001-15000 |
| **3** | **3001-5000** | 8 | 15001-20000 |
| 4 | 4500-6000 | 9 | 20001-30000 |
| 5 | 6001-8000 | 10 | 30001-50000 |
| 6 | 8001-10000 | 11 | 50000以上 |

**年薪**（code 101-112）：101=1-2万，102=2-3万，103=3-5万，104=5-8万，105=8-10万，106=10-20万，107=20-30万，108=30-50万，109=45-60万，110=60-80万，111=80-100万，112=100万以上。

### 公司行业（简历「意向行业/工作行业」用，22 项）

> **注意**：搜索筛选用 `company-industry-v1`（另一套 18 项），两套码表只在 1（酒店业）重合，**不要混用**。

| code | 行业 | code | 行业 |
|------|------|------|------|
| 1 | 酒店业 | 12 | 互联网/电商 |
| 2 | 住房租赁 | 13 | 传媒/文化产业 |
| 3 | 餐饮业 | 14 | 教育/培训 |
| 4 | 休闲娱乐业 | 15 | 家居/日用/服装 |
| 5 | 景区/乐园 | 16 | 食品/饮料 |
| 6 | 旅游交通 | 17 | 商务服务 |
| 7 | 旅游产品/线路 | 18 | 金融/投融资 |
| 8 | 康养 | 19 | 政府/非营利/社会组织 |
| 9 | 医疗健康 | 20 | 其他 |
| 10 | 零售/商超 | 21 | 美业 |
| 11 | 房地产/物业 | 22 | 文旅集团 |

### 其他小类目

| 类目 | code → 值 |
|------|-----------|
| work-mode | 1 全职 · 2 兼职 · 3 实习 · 4 临时 |
| degree | 1 初中 · 2 高中 · 3 中技 · 4 中专 · 5 大专 · 6 本科 · 7 硕士 · 8 博士 |
| accommodation | 1 提供食宿 · 2 不提供食宿 · 3 可提供吃 · 4 可提供住 · 5 食宿面议 |
| currency | 1 人民币 · 2 美元 · 3 英镑 · 4 欧元 |
| gender | 1 男 · 2 女 |
| job-status | 1 离职-随时到岗 · 4 在职-月内到岗 · 2 在职-考虑机会 · 3 在职-暂不考虑 |

## 各模块必填项速查

| 模块 | 必填 |
|------|------|
| update_base | true_name + gender + birthday（年-月）+ current_location（全量覆盖） |
| update_job_status | status（离职-随时到岗/在职-月内到岗/在职-考虑机会/在职-暂不考虑） |
| update_description | content |
| add_intention / update_intention | position + locations + company_industry（≤5） |
| add_work / update_work | company_name + begin_year + **begin_month** + salary（月薪）+ company_industry |
| add_edu / update_edu | school + major + degree + begin_year + end_year |
| apply_job | job_id（+ confirm 确认后） |

## 响应字段速查（实测口径）

**search_job**：`data.count` 总数 · `data.list[]` 职位数组，每条关键字段：

| 字段 | 用途 |
|------|------|
| `job_id` / `job_name` | 职位 id 与名称（投递、对比、话术都用 id） |
| `salary_cn` | 展示文本（如"3千-5千"）；空 → 对用户说"薪资面议" |
| `salary_min` / `salary_max` | 数值上下限（排序/比较用） |
| `exp` / `education` | 经验要求 / 学历要求 |
| `job_area` / `work_place` | 省市 / 具体地点 |
| `label[]` | 福利标签（包吃包住/夜班津贴…），回答福利追问优先看这里 |
| `room_board` | 食宿标注 |
| `company_name` / `company_size` / `company_tag[]` | 公司名 / 规模 / 标签（最佳企业等） |
| `update_time` | 更新日期，**格式不统一**：完整 `年-月-日` / `月-日` / 甚至 `时分` 混出，以返回实际为准（有完整年份才说"多久前"） |
| `is_urgent` | 急招标记（**类型可能混出：数字 `0/1` 或字符串 `"1"`**，判断时按真值 `==1 || =="1"` 都算急招） |
| `job_detail_url` / `company_url` | **平台注入的跳转链接——只透传原值** |

外层：`page_index` 当前页 · `page_size` 本页实际条数 · `company.{count,list}` 命中公司 · 顶层 `suggestion` 仅 0 结果时出现。

**get_resume** 返回的 section：`get_base`（基本信息）、`get_intention`（求职意向数组）、`get_work_exps`、`get_edu_exps`、`self_description.content`、以及**只在 App 可编辑的展示类 section**：`get_certificates` / `get_languages` / `get_skills` / `get_training_exps` / `get_gallery` / `get_ihma`、附件标记 `is_attachment` / `is_upload`。

`get_base` 口径要点：`completeness` 完整度（0-100，展示即可；投递无硬性门槛，但完整度低时投递前友好提醒）· `work_year` 工龄（负值/空=未填或应届，非 bug）· `hidden_mobile` 手机号已打码 · `has_resume` 基本信息完整才为 true · `birthday` 回读带日补零（存 年-月，显示按需截断）。

**写操作成功** 统一 `{msg:"ok", code:200}`；**业务澄清** `{error:{field,hint[,candidates]}}` 或 `{pending_confirm:true}`；`get_work_exps[].is_current` 回读是**布尔**（true=在职）。

> **写后注意 `readback_warning`**：写操作成功后响应可能带 `readback_warning`，说明有字段没存上——**有 warning 就按提示用 get_resume 核对并重试**，不要当作完全成功。已知触发点：`add_work`/`update_work` 缺 `begin_month` 或 `is_current=false` 缺结束时间（会被明确拒绝，不会出现）。

## 错误处理

| 错误 | 处理 |
|------|------|
| 401 / "重新生成 api_key" / 登录态失效 | 登录过期 → 引导重新授权（`https://login.veryeast.cn/skill/auth`），获取新授权码并写入后重试 |
| `{error:{field,hint}}`（无 candidates） | 缺信息/必填校验错 → 按 hint 补齐必填项重调，**不是技术错误，别重试**（重试永远失败） |
| `{error:{candidates}}` | 业务澄清 → 候选展示给用户选，选完重调 |
| `{pending_confirm:true}` | 投递确认 → 用户同意后 `confirm:true` |
| 其他 `isError` / 超时 / 不可达 | 技术错误 → 人话化提示，重试或联系平台侧 |
| ECONNREFUSED / Request failed | 读操作稍后重试；**写操作（投递/改简历）结果不明时不得直接重试**——先读回核对是否真的存上，投递无法核对就如实说"结果不确定，建议去 App 投递反馈确认"，确认没存上再重试，避免重复投/重复写 |
| method not found | 版本不匹配，重试；持续出现联系平台侧 |
