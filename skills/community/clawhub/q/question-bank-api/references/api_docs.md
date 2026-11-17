# 题库 API 接口参考（供应商）

所有接口 `POST`，统一鉴权头 `X-API-Key: <key>`。请求/响应均为 `application/json`。
响应顶层通常含 `errorCode`（成功为 `"0"`）、`data`，部分接口另有 `dataCount`。

> 根地址 `QB_API_BASE`（环境变量或 `--base`）需指向供应商网关，例如
> `https://your-api-host.example.com`，**不含末尾 `/`**。各路径均以 `/api/v1/...` 开头。

## gradeId 速查表（年级，不分上下学期）

| gradeId | 年级 | gradeId | 年级 |
|---------|------|---------|------|
| 110 | 一年级 | 200 | 七年级 |
| 120 | 二年级 | 300 | 八年级 |
| 130 | 三年级 | 400 | 九年级 |
| 140 | 四年级 | 500 | 高一 |
| 150 | 五年级 | 600 | 高二 |
| 160 | 六年级 | 700 | 高三 |

## 典型调用链路

```
1.1 subjectEditionApi  → 学段/年级/学科/版本 code
1.2 getOtherBasic      → qtypes / paperTypes / diffTypes 的 id
   ├─ 2.3 knowledgeApi  → 知识点树（取第三级 oldId 作 knowledgeId）
   │     └─ 2.1 getQuestions        → 按知识点取题
   ├─ 1.3 chapterApi    → 章节树（取 id 作 chapterId）
   │     └─ 2.6 getQidByChapterId   → 按章节取题（语文/英语等）
   ├─ 2.4 search        → 全文检索（取 md52）
   └─ 3.1 getPaperList / 3.3 paperSearch → 试卷列表/搜索（取 id）
          └─ 3.2 getPaperQues        → 按试卷取题
2.2 getAnswer          → 以上各取题结果用 md52 取答案解析
4.1 json2word          → 结构化题目渲染成 docx
```

---

## 一、基础数据

### 1.1 `POST /api/v1/subjectEditionApi` — 学段/年级/学科/版本树
参数：无。返回 `data[]`，每项为 `{id,name,pid,code,child[]}`，逐级为
学段→年级学期→学科→版本。`code` 字段供其他接口作 `pharseId`/`subjectId`/`editionId`/`gradeId`。

### 1.2 `POST /api/v1/getOtherBasic` — 题型/试卷类型/难易度字典
参数：无。返回 `qtypes[]`（`{id,subjectId,pharseId,typeName}`）、
`paperTypes[]`（`{id,name}`）、`diffTypes[]`（`{id,name}`）。其 `id` 供筛选参数使用。

### 1.3 `POST /api/v1/chapterApi` — 章节知识点树
参数：`pharseId`(必), `subjectId`(选), `editionId`(选), `gradeId`(选)，值均来自 1.1 的 `code`。
返回 `data[]` 树，`child` 嵌套。取目标章节的 `id` 作为 2.6 的 `chapterId`。

---

## 二、试题数据

### 2.1 `POST /api/v1/getQuestions` — 按知识点取题
参数：`knowledgeId`(必，来自 2.3 的 `oldId`)、`qtypeId`(选)、`paperType`(选)、
`diff`(选)、`gradeId`(选，仅年级，见速查表)、`year`(选，如 `2018` 或 `2022,2018`)、
`page`(必，默认1)。
返回 `data[]`，题目字段含 `title`/`option_a..e`/`qtpye`/`diff`/`year`/`source`/
`subjectName`/`gradeName`/`paperName`/`md52`/`id`/`knowledgeMore[]`。

### 2.2 `POST /api/v1/getAnswer` — 按 md52 取答案
参数：`qid`(必，来自题目 `md52`，支持逗号分隔多题 `a,b,c`)。
返回 `data[]`，含 `answer1`/`answer2`/`parse`/`children[]`（子题）。多题消耗多次额度。

### 2.3 `POST /api/v1/knowledgeApi` — 知识点树
参数：`pharseId`(必), `subjectId`(选)，值来自 1.1 的 `code`。
返回 `data[]` 三级树，遍历到第三级取 `oldId` 作为 2.1 的 `knowledgeId`。

### 2.4 `POST /api/v1/search` — 全文检索
参数：`keyword`(必，中文需 urlencode)、`gradeId`(必)、`subjectId`(选)。
`title` 为完整内容，`timu` 为带高亮的可能截断内容。取 `md52` 到 2.2 取答案。

### 2.5 `POST /api/v1/getQuestionsByGrade` — 按年级科目取题（已弃用）
现改走 2.1（科目+知识点+年级）。不要在新流程中使用。

### 2.6 `POST /api/v1/getQidByChapterId` — 语文/英语按章节取题
参数：`chapterId`(必，来自 1.3 的 `id`)、`qtypeId`(选)、`paperType`(选)、
`diff`(选)、`year`(选)、`page`(必，默认1)。

---

## 三、试卷数据

### 3.1 `POST /api/v1/getPaperList` — 试卷列表
参数：`subjectId`(选)、`gradeId`(必)、`paperTypeId`(选)、`term`(选,0全/1上/2下)、
`areaId`(选，区域 unique_code)。返回 `data[]`，含 `paperName`/`id`/`year`/`area`/`paperType`。

### 3.2 `POST /api/v1/getPaperQues` — 试卷详情（含全部试题）
参数：`paperId`(必，来自 3.1 的 `id`)。返回 `data[]`，题目字段同 2.1。

### 3.3 `POST /api/v1/paperSearch` — 试卷搜索
参数：`keyword`(必)。返回 `data[]`，含 `id`/`paperName`/`subjectName`/`paperType`/`gradeName`/`year`/`area`。

---

## 四、Word 工具

### 4.1 `POST /api/v1/json2word` — 结构化题目 → docx
Header：`X-API-Key`、`Content-Type: application/json`。
Body：`{ docType, answerType, fontSize, paperSizeType, paperData }`，其中 `paperData` 为
包含 `questionsTypeList`/`mainTitle`/`subTitle` 的 JSON 字符串。
**返回二进制 docx 文件流**（脚本用 `--out` 保存到本地文件）。

---

## 错误码参考
- `errorCode` 非 `"0"`：业务错误，读取 `message`/`data` 反馈。
- HTTP `401`：key 无效/缺失。HTTP `429`：限流（脚本已退避重试）。HTTP `5xx`：服务端异常。
