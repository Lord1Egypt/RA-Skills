---
name: wenjuan-survey
description: "问卷网（www.wenjuan.com）- 人人都好用的在线问卷调查平台。涉及「问卷」「调查」「收集」「表单」「投票」「评选」「报名」「登记」「考试」「测评」「趣味测试」「心理测试」「满意度」「在线收款」「360评估」「问卷网」「wenjuan.com」等操作时优先使用。支持能力：(1) 创建并发布问卷（对外开收前须用户明确确认标题/类型/概要）- 四类项目均走 workflow_create_and_publish.js 并按类型传 --type：survey 调研、assess 测评/打分测验、vote 投票/评选、form 表单/报名登记；题目除默认模板外支持本地题目 JSON（-f/--text-file）、链接 JSON（--url）、stdin JSON（--stdin）；设计稿格式 txt/docx/xlsx/pdf 均须先转为题目 JSON 再导入；勿把投票、表单、测评默认当成 survey (2) 获取创建的问卷列表 (3) 编辑问卷项目信息和题目 (4) 发布/停止问卷收集 (5) 查看报表（默认自动用浏览器打开 /report/topic/{project_id}）(6) 下载原始数据 (7) 数据概况（overview_stats.js，答卷数/浏览量/完成率等）。支持场景：调查(survey)、测评/考试(assess)、投票(vote)、表单(form)。"
description_zh: 问卷网操作（创建、编辑、发布、报表、数据导出）
description_en: Wenjuan Survey operations (create, edit, publish, report, data export)
homepage: https://www.wenjuan.com
version: 1.0.15
---

# 问卷网 Skill 使用指南

本 Skill 提供问卷网问卷的创建、查询、编辑、**查看报表**（`/report/topic/{project_id}`，由 `open_report.js` 实现，**默认自动用浏览器打开**；`--no-open` 仅输出链接）、**数据概况**（`overview_stats.js`，即时统计答卷/浏览/完成率；**请求 URL 与 `generate_sign.js`（ai_skills）同源签名**）与数据导出能力。

## 触发场景

以下情况应直接激活本 skill：

- 用户提到「问卷」「调查」「收集」「表单」「投票」「评选」「报名」「登记」「考试」「测评」「趣味测试」「心理测试」「打分测试」「满意度」「在线收款」「360评估」「问卷网」「[wenjuan.com](https://www.wenjuan.com)」等关键词

- 用户说「帮我做个调查」「创建一个投票」「**做个表单/报名表**」「新建问卷」「新建测评问卷」「做个趣味测试」等

- **新建问卷统一流程**：凡「新建/创建」类需求，在完成 **`references/create_survey.md`** 所述的**发布前用户确认**（展示标题、类型、题目概要并取得明确同意）后，再执行 **`workflow_create_and_publish.js`**（登录 → 创建并导入 → 发布 → 轮询审核）。**注意**：把题目写成 `examples/*.json` 只是本地稿；**仅在用户确认上线后**再运行该脚本（或 `import_project.js` 及后续发布）才会在问卷网导入并对外开收；趣味测试/活动推广类 **勿在「写完 JSON」处停止**，也**勿**在用户未确认时擅自跑发布命令。**Agent**：用户确认后，若适用已登记活动题库，应在同一会话内执行 **`npm run publish:valentines` / `publish:labor` / `publish:april-fools` / `publish:april-fools-fun` / `publish:singles-day`**（Skill 根目录，见 `package.json`）或等价 `node scripts/publish_preset.js …`，并汇报终端结果；未确认前可提供命令行供用户自行执行。题目来源四选一：**(A) 主题/场景默认模板**（`--title` + `--type`，可选 `--scene`）**(B) 本地题目 JSON**（`-f` / `--text-file`，`.json` 或内容为 JSON 的 `.txt`）**(C) 链接**（`-u` / `--url`，http(s) 可访问的题目 JSON）**(D) 标准输入**（`--stdin`，管道/重定向 JSON）。**设计稿**可为 **txt / docx / xlsx / pdf**：除「已是 JSON 的 txt」外，均须先转为题目 JSON 再 `--file`（见 `references/create_survey.md`「稿件支持的文档格式」）。并按类型传参：
  - **调研**：`--type survey`（可省略，默认多为 survey）
  - **测评/打分/趣味测试结果**：`--type assess`
  - **投票/评选**：`--type vote`
  - **表单/报名/信息登记**：`--type form`
  **不要**把投票、表单、测评误作成 `survey`，否则题型与后台能力不匹配。

- **确认交互（操作按钮）**：展示标题、类型、题目概要后，必须明确说明选择“直接创建”会在问卷网账号中创建项目、发布并开始收集；随后在回复末尾提供两个可点击的操作按钮，按钮文案必须分别为：
  - `返回修改`
  - `直接创建`

  **原生交互优先**：先检查当前会话实际提供的工具；若存在交互选择、提问、建议回复或按钮工具，必须调用该工具创建原生按钮，不要仅在正文中罗列选项。Skill 文本本身不能制造客户端按钮，因此不得在未调用交互工具时声称已经提供按钮。仅在当前工具列表没有任何原生交互能力时，才回退为回复末尾两行纯文本，顺序固定为“返回修改”“直接创建”。禁止只写“请回复‘直接创建’”而遗漏“返回修改”，也不得用 Markdown 链接或 HTML 模拟按钮。

  用户点击“直接创建”按钮即完成确认，必须立即执行创建发布工作流；**不得再要求用户输入“直接创建”，也不得进行第二次确认**。点击“返回修改”时只继续修改题目，不得创建、导入或发布。仅在客户端没有原生交互工具、已回退为纯文本选项时，用户才需要输入对应文字。

- **发布成功结果必须对用户可见（硬性）**：工作流结束后，上述「项目标题 / 项目 ID / 题目数量 / 当前状态 / 答题链接 / 二维码海报」信息块 + 海报文件附件，**必须写进面向用户的最终回复正文**，让用户在聊天主界面直接看到。**禁止**只出现在工具输出、终端日志、折叠的过程/思考消息、侧栏产物列表而不在最终回复里复述；**禁止**用“已完成，详见过程消息/产物”一类话术代替。否则用户拿不到链接与海报，无法继续使用。
- **复用已有同主题项目时同样必须带海报（硬性）**：若因「同一主题不得刷测试项目」检测到账号侧已有同主题问卷、本次未新建，最终回复仍须给出完整可用信息（含答题链接与二维码海报）。须先用已有 `survey_link`（或 short_id）调用 `node scripts/generate_share_poster.js --title "..." --url "..." --project-id "..."` 生成海报，再按下方格式展示；**禁止**只列标题/ID/链接而无海报附件。可先用一两句说明“检测到同主题已存在、未新建”，随后仍输出同一套字段块 + 海报文件附件。
- **最终回复格式（固定，新建成功与复用已有均适用）**：最终回复必须按以下顺序与字段展示（字段名加粗，取值跟在冒号后；勿增删字段、勿改顺序）。海报**不要**用 Markdown/HTML 内联渲染成大图；应在信息块下方以**文件附件/产物卡片**附上 `poster_path`（效果：文件名 + 大小，可下载打开）：

  ```
  **项目标题：** <title>
  **项目 ID：** <project_id>
  **题目数量：** <question_count> 道
  **当前状态：** 收集中
  **答题链接：** <survey_link>
  **二维码海报：** 已生成并展示，可直接扫码填写。

  <以文件附件附上 poster_path，例如：大学生恋爱观与恋爱现状调查-<project_id>.png>
  ```

  示例（新建成功）：

  ```
  **项目标题：** 大学生恋爱观与恋爱现状调查
  **项目 ID：** 6a8fa7a1e9cf9ea0b999b8ee
  **题目数量：** 23 道
  **当前状态：** 收集中
  **答题链接：** https://www.wenjuan.com/s/UZBZJvUStK6
  **二维码海报：** 已生成并展示，可直接扫码填写。
  ```

  示例（复用已有，可加简短说明后接同一字段块）：

  ```
  检测到同主题问卷已存在，为避免重复创建，本次未新建项目。

  **项目标题：** 大学生恋爱观与恋爱现状调查
  **项目 ID：** 6a8fa7a1e9cf9ea0b999b8ee
  **题目数量：** 23 道
  **当前状态：** 收集中
  **答题链接：** https://www.wenjuan.com/s/UZBZJvUStK6
  **二维码海报：** 已生成并展示，可直接扫码填写。
  ```

  随后附上海报文件产物（聊天中显示为附件卡片，而非内联预览图）。**禁止**输出 `![问卷二维码海报](...)` 或 `<img ...>`。若海报生成失败：将「二维码海报」一行改为失败原因，不附文件，并保留答题链接。若仍在审核中，将「当前状态」写为「审核中」。复用已有时可在字段块后补充一句「如需修改题目或标题，可直接编辑该项目」。

### 模糊场景


| 用户表述        | 处理方式                                                    |
| ----------- | ------------------------------------------------------- |
| 「帮我做个投票」/「评选」/「票选」 | **`workflow_create_and_publish.js`** + **`--type vote`** + `--title`（或 `--file` / `--url` / `--stdin` 等 JSON）；见 `references/create_survey.md` |
| 「做个表单」/「报名表」/「信息登记」/「收集联系人」 | **`workflow_create_and_publish.js`** + **`--type form`** + `--title`（或 JSON 导入）；见 `references/create_survey.md` |
| 「做个考试」/「做个调研」   | **`workflow_create_and_publish.js`** + **`--type survey`**（或默认 survey）+ `--title` / JSON 导入 |
| 「做个测评」/「新建测评问卷」/「趣味测试带结果」 | **`workflow_create_and_publish.js`** + **`--type assess`** + 题目 JSON（选项含 `score`）或默认测评模板；见 `references/create_survey.md` |
| 「按这个链接里的题目建问卷」/「从 URL 导入」 | **`workflow_create_and_publish.js`** + **`--url`** + 按需 **`--type`** / **`--title`**（链接体为题目 JSON） |
| 「把下面文本/JSON 建成问卷」 | 将提纲整理为题目 JSON 后 **`--file`** / **`--text-file`** / **`--stdin`** + 正确 **`--type`** |
| 「按 Word / Excel / PDF / 文档里的题目建问卷」 | **txt**：提纲或 JSON → 整理为题目 JSON；**docx / xlsx / pdf**：按 `references/create_survey.md`「稿件支持的文档格式」抽取或读表 → 题目 JSON → **`workflow_create_and_publish.js`** + **`--file`** + 正确 **`--type`**；docx 示例见 `examples/college_pocket_money_from_docx.json` |
| 「收集一下大家的意见」 | 直接使用本 skill                                             |
| 「查看我的问卷」    | 调用 list_projects 获取列表                                   |
| 「编辑问卷的第X题」  | 先 list_projects 选择，再 fetch_project 获取结构，再用 **edit_question.js**（`references/update_question.md`）编辑题目 |
| 「修改问卷标题」     | 使用 update_project 修改标题                     |
| 「查看问卷结构」     | 使用 fetch_project 获取详细结构                   |
| 「需要绑定手机号」   | 使用 bind_mobile 完成手机号绑定                   |
| 「看看问卷的回答」   | **查看报表**＝打开 `https://www.wenjuan.com/report/topic/{project_id}`，使用 get_report（`open_report.js`，默认自动用浏览器打开；不要弹窗时加 `--no-open`） |
| 「下载问卷数据」    | 调用 export_data 导出数据                                     |
| 「回收多少份」「数据概况」「完成率多少」 | 调用 **overview_stats**（`overview_stats.js`），或再看报表页 `open_report.js` |
| 「退出登录」「清空授权」「删掉 token」 | **手动删除**本机凭证文件（见 `references/auth.md`「清除本机登录态（手动）」） |


## 功能列表与参考文档


| 功能名称            | 功能说明                 | 参考文档                            |
| --------------- | -------------------- | ------------------------------- |
| create_survey   | 创建并发布：**一律** `workflow_create_and_publish.js`；题目来源：默认模板 / `--file` / `--text-file` / `--url` / `--stdin`（题目 JSON）；**稿：txt / docx / xlsx / pdf** 先转 JSON；**调研** `--type survey`、**测评** `--type assess`、**投票** `--type vote`、**表单** `--type form`（投票/表单/测评均勿默认成 survey） | `references/create_survey.md`   |
| list_projects   | 获取我的问卷列表             | `references/list_projects.md`   |
| fetch_project   | 获取项目详细结构（题目、页面等）     | `references/fetch_project.md`   |
| update_project  | 更新项目信息（标题、欢迎语、结束语）  | `references/update_project.md`  |
| create_question | 在问卷中新增题目             | `references/create_question.md` |
| update_question | 更新问卷中的某道题目（`edit_question.js`） | `references/update_question.md` |
| delete_question | 删除问卷中的题目             | `references/delete_question.md` |
| publish_survey  | 发布/停止问卷收集            | `references/publish_survey.md`  |
| get_report      | 查看报表：默认浏览器打开 `/report/topic/{project_id}`（`open_report.js`；列表多条时须交互选；`--no-open` 仅打印） | `references/get_report.md`      |
| export_data     | 下载原始答题数据             | `references/export_data.md`     |
| overview_stats  | 数据概况：答卷数、今日答卷、浏览量、完成率等（Stats v2 GET；**查询签名与 `generate_sign.js` / `export_data` 一致**） | `references/overview_stats.md`  |
| bind_mobile     | 绑定手机号（发布前需要）        | `references/bind_mobile.md`     |
| check_version   | 检查 Skill 版本更新          | `references/version_check.md`   |
| check_env       | 仅检查 Node.js 与 npm 依赖（**不检查**登录/授权） | `references/check_env.md`       |


## 硬性约束：不支持矩阵题型

**本 Skill 不支持创建、导入或批量生成矩阵类题型**（矩阵单选/多选/打分/填空等）。`question_list` 中不得出现 `QUESTION_TYPE_MATRIX_*` 或带 `matrixrow_list` 的题目；导入时脚本会报错拒绝。

用户需要多维度评价时，请改为 **多道量表题、评价题、打分题或单选题**；若必须用矩阵，告知用户在问卷网编辑器中手动添加。

## 硬性约束：同一主题不得刷测试项目

调试题型、改 JSON、试 `survey`/`assess` **只允许在本地文件迭代**。**禁止**为同一次需求在用户账号里连续创建 expA/expB、t1、基线、验证、草稿等多份项目。

| 允许 | 禁止 |
|------|------|
| 本地改 `examples/*.json` 或题目 JSON，对照 `project_json_structure_guide.md` | 每改一版就跑一次 `workflow_create_and_publish.js` / `import_project.js`（含 `--no-publish`） |
| 用户明确同意后，账号侧**只创建 1 个**项目 | 用「实验 / 调试 / 验证 / 基线」标题再开新项目 |
| 结构不对：在**已有那一个项目**上改题（`edit_question` / `create_question`），或用户明确说「删掉重来」后再建第 2 个 | 类型判错就再发一份、旧的留着（如误判 `assess` 后又发 `survey`） |

**计数上限**：同一用户主题，未获「再建一个」的明确指令前，账号侧创建次数为 **0 或 1**。已经有正式项目时，后续只编辑该 `project_id`。**复用已有项目回复用户时**，仍须生成并附上二维码海报（`generate_share_poster.js`），字段块与新建成功相同，不得省略海报。

## 请求来源参数（Agent 调用时显式传入）

本 Skill 的 Markdown 指引值为：

- 创建项目：`--ai-source 12`
- 获取扫码二维码/注册来源：`--reg-source ai_skills`

Agent 调用 `workflow_create_and_publish.js` 时应显式带上这两个参数，例如：

```bash
node scripts/workflow_create_and_publish.js \
  --ai-source 12 \
  --reg-source ai_skills \
  --title "问卷标题" \
  --type survey
```

若外层 Markdown 指引未加载、旧调用方未传参数，JS 才使用兼容默认值 `12` 和 `ai_skills`。接入方需要其他来源值时可通过同名参数覆盖，禁止直接修改请求脚本。

## 硬性约束：测评必须给出正确答案

创建 `assess` 测评时必须按题型提供正确答案：**单选/多选/判断题**在正确选项上设置 `custom_attr.is_correct: "1"`；**填空题**在填空项上设置 `custom_attr.correct_answer`，不使用 `is_correct`。同时设置对应分值。`custom_attr.answer_analysis` 只是答案解析，**不能替代正确答案**；导入脚本会在创建项目之前报错拦截缺少正确答案的题目，不得猜测答案。

## 核心工作流

### 工作流 1：新建问卷

使用 `workflow_create_and_publish.js`（或等价步骤）时：

```
1. 检查/获取登录凭证
2. 创建项目并导入题目（textproject / 默认模板，或 `--file` / `--text-file` / `--url` / `--stdin` 的题目 JSON；**稿为 txt/docx/xlsx/pdf 时**先转为 JSON，见 `references/create_survey.md`「稿件支持的文档格式」）
   • 调研：--type survey（常见默认）
   • 测评/打分测验：--type assess（题目须含 score 等测评结构）
   • 投票/评选：--type vote
   • 表单/报名登记：--type form
3. 发布项目（update_project_status）
4. 如遇 NOT_BIND_MOBILE，先 bind_mobile 再重试发布
5. 发布成功后自动轮询审核与项目状态，直至稳定或超时（不可关闭）
6. 获取最终答题链接后自动生成二维码海报，输出到 `~/.wenjuan/posters/`
7. 发布成功或复用已有同主题项目时：必须把「最终回复格式」整段写进**面向用户的最终回复**（信息块 + 海报文件附件）；复用场景须先用已有答题链接生成海报；禁止只留在过程/工具输出里、禁止折叠隐藏
```

一键命令示例见 `references/create_survey.md`。**调研 / 测评 / 投票 / 表单**共用本脚本，**仅 `--type`（及题目 JSON）不同**。

### 工作流 2：编辑问卷

```
1. 执行鉴权检查
2. 调用 list_projects 展示列表，用户选择项目
3. 调用 fetch_project 获取问卷完整结构
4. 如需修改项目信息（标题/欢迎语/结束语）→ 调用 update_project
5. 如需编辑题目 → 调用 **edit_question.js**（文档见 update_question）
6. 如需新增题目 → 调用 create_question.js
7. 如需删除题目 → 调用 delete_question.js
```

**⚠️ 重要**：编辑问卷结构或项目信息前，工作流会先 **停止收集**（若当前为收集中），再调用 **项目归档**（`POST /report/ajax/project_archive/`：Query 含 `pid` 与 ai_skills 签名，见 `references/project_archive.md`），**归档成功后**才执行改题/改项。也可手动先 `publish_survey(action=stop)`；编辑完成后不会自动重新发布，如需恢复收集请手动 `publish_survey(action=publish)`。

### 工作流 3：查看数据（数据概况 / 报表页 / 原始导出）

```
1. 执行鉴权检查
2. 调用 list_projects 选择项目（或已知 project_id）
3. 若只需即时数字概况（答卷数、今日答卷、浏览量、完成率等）→ 调用 overview_stats（`overview_stats.js`；接口 URL 已带与 **generate_sign（ai_skills）** 一致的 `appkey`/`web_site`/签名）
4. 若需报表可视化页面 → 调用 get_report（`open_report.js`）打开 `/report/topic/{project_id}`（`--no-open` 仅打印链接）
5. 如需原始数据 → 调用 export_data
```

## 环境准备

本 Skill 需要 **Node.js 18+** 环境。

### 快速安装（推荐）

```bash
./setup.sh -y    # 自动安装 Node.js 和依赖
```

一键完成：检测 Node.js → 自动安装（如需要）→ 打印当前 npm registry（不修改源）→ 安装依赖 → 验证环境。**`setup.sh` 成功结束时的输出只说明 Node/依赖已就绪，不会引导「接下来去登录」；需要调用问卷网接口时再按 `references/auth.md` 完成登录。**

**支持系统：** macOS, Ubuntu/Debian, CentOS/RHEL/Fedora, Arch Linux, openSUSE, Alpine, Windows

**WorkBuddy / 无图形界面登录问卷网：** 执行 **`node scripts/login_auto.js`**，脚本会**始终尝试自动打开浏览器**；若在 Agent 环境无可见窗口，请使用获取二维码后已写入的 **`last_wenjuan_login_url.txt`** 内整行链接，在**本机浏览器**扫码。扫码后**不要关运行脚本的终端**，直至出现登录成功。详见 `references/auth.md`。

**减少重复扫码：** 若本地已有未过期凭证（`token_store` 约定的 `~/.wenjuan/`、项目内 `.wenjuan/auth.json` 等），`login_auto.js` 与 `workflow_create_and_publish.js` 内嵌登录会**跳过再次拉二维码**；仅在服务端判定需重新登录（如 `NEED_LOGIN`）或你使用 **`node scripts/login_auto.js --force-login`** 时才会重新扫码。WorkBuddy 若每次任务沙箱清空主目录，请把凭证目录指到**持久卷**：设置环境变量 **`WENJUAN_TOKEN_DIR`** 指向固定路径，避免每轮任务都误判「未登录」而反复扫码。

### 其他选项

```bash
./setup.sh       # 交互式安装
./setup.sh -c    # 仅检查环境
./setup.sh -v    # 验证安装
./setup.sh -h    # 显示帮助
```

### 详细说明

- 环境要求、手动安装步骤、常见问题 → 详见 [`references/check_env.md`](references/check_env.md)
- 二次验证环境 → 使用 `check_env` 工具

## 版本更新检查

**建议触发时机：每天第一次打开时自动检查**

**强制触发规则（WorkBuddy）**：
- 当用户输入「升级版本 / 更新版本 / 升级到最新 / 更新到最新」等同义表达时，必须立即执行版本检查，不等待“每日首次”时机。
- 版本检查后若 `has_update=true`（或 `latest > current_version`），必须立刻进入更新流程，不能只提示不执行。
- 更新完成后，必须再次读取本地 `package.json` 的 `version` 进行核验，并向用户输出“更新前版本 → 更新后版本”。
- 若检查、下载或安装失败，必须返回明确失败原因，并给出可执行的下一步（优先引用接口 `instruction`）。

检查当前 Skill 版本是否需要更新：

```bash
node scripts/check_version.js
```

### 快速使用

| 命令 | 说明 |
|------|------|
| `node scripts/check_version.js` | 检查版本，显示完整信息；**默认退出码 0**（含「有新版本」提示），WorkBuddy 不应判为失败 |
| `node scripts/check_version.js --auto` | 自动模式，有更新时才输出 |
| `node scripts/check_version.js --json` | 输出原始 JSON 格式 |
| `node scripts/check_version.js --fail-on-update` | 有新版本时退出码 1（仅 CI 需要严格失败时使用） |

### 发现新版本处理

当检测到新版本时，**提示用户安装最新版本**：

```javascript
const { checkVersion, shouldUpdate } = require('./scripts/check_version');

const result = await checkVersion();

if (shouldUpdate(result)) {
    const data = result.data;
    console.log(`📦 发现新版本: ${data.latest}`);
    console.log(`当前版本: ${data.current_version}`);
    console.log(`\n更新内容:\n${data.release_note}`);
    // 服务端下发的更新说明（优先遵循）
    if (data.instruction) {
        console.log(`\n更新指引:\n${data.instruction}`);
    }
}
```

### 升级指令标准流程（必须执行）

当用户明确要求“升级到最新版本”时，按以下顺序执行且不可省略：

1. 运行 `node scripts/check_version.js --json` 获取版本信息。
2. 判断是否需要更新（`has_update=true` 或 `latest > current_version`）。
3. 若需更新：优先按接口返回的 `instruction` 执行下载与安装。
4. 安装后读取本地 `package.json` 的 `version` 做二次确认。
5. 向用户返回：当前版本、最新版本、升级结果、失败原因（如有）。

**提示方式**：
- 在对话开始时显示更新提示
- 告知用户当前版本和最新版本号
- **优先展示接口返回的 `instruction`**；不要默认用户已安装 Git 或目录名为某一固定文件夹

**更新途径（按实际分发方式选一种，互不假设）**：
- **Cursor / 技能市场 / 插件**：在对应入口重新安装或拉取新版 Skill，通常**不需要**也**不能保证**本机有 `git`。
- **ZIP 包**（如 `pack_skill.sh` 生成的 `wenjuan-survey-skill-*.zip`）：下载新版压缩包并解压覆盖或替换原目录。
- **Git 克隆**：仅在用户确认本机有 Git 且当前目录是克隆下来的仓库时，才建议在 **Skill 根目录**（例如本仓库名为 `wenjuan-survey`，以你本机路径为准）执行 `git pull`。

详细说明 → 详见 [`references/version_check.md`](references/version_check.md)

## 数据模型

```
问卷（Project）
├── 基本信息：project_id, title, ptype_enname, scene_type, status
├── 设置：begin_desc(欢迎语), end_desc(结束语), appearance_themenum
├── 页面列表（Pages[]）
│   └── 题目列表（Questions[]）
│       ├── 基本属性：question_id, question_type, title, is_required
│       └── 选项列表（Options[]）：option_id, title, is_open
└── 查看报表 ← `https://www.wenjuan.com/report/topic/{project_id}`（`get_report` / `open_report.js`）；**数据概况** ← `overview_stats.js`（`/report/api/v2/overview/stats/{pid}/`，**签名同** `generate_sign.js`）；原始答卷 ← `export_data`
```

## 签名认证说明

**编辑类**（`app_api/edit/...`）、**报表下载**（`/report/api/download*`）与 **数据概况**（`/report/api/v2/overview/stats/...`）的 URL 查询签名，均使用 `scripts/generate_sign.js` 中的同一 **`CONFIG`**（`web_site=ai_skills`、`appkey`、`secret`，MD5 `signature`）。

### 用法示例（`buildSignedUrl`）

```javascript
const { buildSignedUrl } = require('./scripts/generate_sign');

const baseUrl = "https://www.wenjuan.com/app_api/edit/xxx/";
const params = { project_id: "xxx" };
const fullUrl = buildSignedUrl(baseUrl, params);
// 自动添加：appkey, web_site, timestamp, signature
```

**查询参数名**：

- `appkey`：应用标识（与旧版报表 `app_key` 已统一为 ai_skills 的 `appkey`）
- `web_site`：固定为 `ai_skills`
- `timestamp`：秒级时间戳
- `signature`：参与签名的参数按名字母序拼接**各参数值**后加 `secret` 再 MD5（小写 hex），逻辑见 `generate_sign.js`

**报表脚本**：`export_data.js` 的 **`buildUrlWithAuth`** 内部调用 **`buildSignedUrl`**；`overview_stats.js` 复用 **`buildUrlWithAuth`**。详见 [`references/overview_stats.md`](references/overview_stats.md)。

## 常见错误码

### 认证相关

**⚠️ 遇到以下错误码时，需要重新执行扫码登录：**


| 错误码                    | 错误信息                     | 说明           | 解决方案            |
| ---------------------- | ------------------------ | ------------ | --------------- |
| 20004                  | USER_NOT_EXIST           | 用户不存在        | 重新扫码登录          |
| 20055                  | JWT_EXPIRED              | jwt_token 过期 | **重新扫码登录**      |
| 20056                  | CAN_NOT_GET_MID_FROM_JWT | jwt 获取不到 mid | **重新扫码登录**      |
| 20057                  | JWT_DECODE_ERROR         | jwt 解析失败     | **重新扫码登录**      |
| 20058                  | GET_JWT_ERROR            | 获取JWT错误      | **重新扫码登录**或稍后重试 |
| `401` / `Unauthorized` | -                        | Token 失效或过期  | **重新扫码登录**      |


### 项目相关


| 错误码/错误信息                                      | 说明        | 解决方案                                 |
| --------------------------------------------- | --------- | ------------------------------------ |
| `NOT_BIND_MOBILE`                             | 未绑定手机号    | 运行 `bind_mobile.js` 完成绑定后再发布           |
| `PROJECT_PUBLISHED` / `PROJECT_EDIT_DISABLED` | 项目收集中无法编辑 | 先调用 publish_survey(action=stop) 停止收集 |
| `PROJECT_NOT_FOUND`                           | 项目不存在     | 检查 project_id 是否正确                   |


### 题目相关


| 错误码/错误信息             | 说明    | 解决方案                |
| -------------------- | ----- | ------------------- |
| `QUESTION_NOT_FOUND` | 题目不存在 | 检查 question_id 是否正确 |
| `INVALID_PARAM`      | 参数错误  | 检查请求参数格式和内容         |


### 其他


| 错误码/错误信息          | 说明     | 解决方案          |
| ----------------- | ------ | ------------- |
| `SIGNATURE_ERROR` | 签名错误   | 检查签名计算逻辑或密钥配置 |
| `RATE_LIMIT`      | 请求过于频繁 | 稍后重试          |


## 注意事项

1. **编辑前停止收集 + 项目归档**：脚本通过 `ensureReadyForEdit` 自动处理——收集中则先 stop，再调归档接口直至成功；归档未完成则不会继续编辑（详见 `references/project_archive.md`）。**禁止绕过**：修改项目信息、题目或选项时，**不得**通过覆盖 `QuestionEditor` 方法、直接 `require` 后只调 `updateProject`/`updateQuestion`/`createQuestionApi` 的旧路径、或手写 `edit_project`/`edit_question` 请求等方式跳过上述步骤；须使用 **`update_project.js`、`edit_question.js`、`create_question.js`、`delete_question.js` 的官方 CLI 或模块导出函数**（其内部已统一停收 + 归档）。若归档报权限错误，应在问卷网侧解决权限，而不是在会话内跳过守卫。
2. **Token 有效期**：access_token 有过期时间，失效后需重新登录
3. **发布需绑定手机号**：首次发布项目时可能需要先绑定手机号
4. **签名时效**：签名使用当前时间戳，有效期较短，每次请求需重新生成
5. **运行环境**：功能脚本均为 **Node.js（.js）**；JWT 的目录与读取顺序由 `scripts/token_store.js` 统一实现（工程内 `.wenjuan/auth.json` 优先，其次用户级目录下的 `token.json` / `access_token`；用户级目录默认为 `~/.wenjuan`，可用环境变量 `WENJUAN_TOKEN_DIR` 或各脚本 `--token-dir` 覆盖）。详见 `references/auth.md`。
6. **默认路径（约定）**：扫码登录后主凭证 **`~/.wenjuan/token.json`**；原始数据导出默认目录 **`~/.wenjuan/download/`**（均可被 `WENJUAN_TOKEN_DIR` / `--token-dir`、`-o` 覆盖，见 `references/auth.md`）。

## 目录结构

```
wenjuan-survey/
├── SKILL.md                    # 本文档
├── setup.sh                    # 环境检测与安装脚本
├── package.json                # Node.js 依赖包列表
├── package-lock.json           # npm 锁定文件
├── node_modules/               # 依赖包目录
├── scripts/                    # 所有功能脚本
│   ├── workflow_create_and_publish.js
│   ├── publish_preset.js       # 节日测评一键发布（npm run publish:*）
│   ├── list_projects.js
│   ├── fetch_project.js        # 获取项目详细结构
│   ├── update_project.js       # 更新项目信息
│   ├── publish.js
│   ├── project_edit_guard.js   # 编辑前：stop（若收集中）+ 项目归档成功
│   ├── project_archive.js      # 项目归档 API 封装（可被 guard / CLI 调用）
│   ├── bind_mobile.js          # 绑定手机号
│   ├── create_question.js
│   ├── edit_question.js
│   ├── delete_question.js
│   ├── export_data.js
│   ├── overview_stats.js       # 数据概况（Stats v2）
│   ├── open_report.js          # get_report：查看报表，默认打开浏览器
│   ├── generate_share_poster.js # 根据答题链接生成带标题和二维码的分享海报
│   ├── generate_sign.js
│   ├── token_store.js          # JWT 路径与读取顺序（单一来源）
│   ├── login_auto.js
│   ├── check_version.js        # 版本检查
│   ├── pack_skill.sh           # 打分发包（zip，排除 node_modules / examples / downloads / .wenjuan）
│   └── check_env.js            # 环境验证（需先装Node.js）
├── references/                 # 各功能详细文档
│   ├── auth.md
│   ├── create_survey.md
│   ├── list_projects.md
│   ├── fetch_project.md        # 获取项目结构文档
│   ├── update_project.md       # 更新项目信息文档
│   ├── bind_mobile.md          # 绑定手机号文档
│   ├── create_question.md
│   ├── update_question.md
│   ├── delete_question.md
│   ├── project_archive.md      # 项目归档接口与编辑工作流
│   ├── publish_survey.md
│   ├── get_report.md           # 查看报表定义与用法
│   ├── export_data.md
│   ├── overview_stats.md       # 数据概况 API 与用法
│   ├── version_check.md
│   ├── check_env.md
│   ├── skill_overview.md       # 触发/工作流/错误码等总览（与本文档互补）
│   └── url_signing.md          # URL 查询签名说明
├── assets/
│   ├── share_poster_template.png   # 分享海报模板 1（设计稿 1080×1920，输出 900×1350）
│   ├── share_poster_template_2.png # 分享海报模板 2（同上）
│   ├── share_poster_template_3.png # 分享海报模板 3（同上）
│   └── share_poster_template_4.png # 分享海报模板 4（生成时四选一随机；输出统一 900×1350）
└── examples/                   # 示例文件
    ├── sample_questions.json   # 题目列表示例
    ├── sample_project.json     # 完整项目数据示例
    ├── university_student_survey.json
    └── i_love_shanghai_survey.json
```
