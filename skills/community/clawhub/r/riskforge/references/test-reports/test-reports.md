# 测试报告模板规范

## 输出要求（强制）

**重要**: 模型每次生成报告时，最终输出的 Markdown 文件中**必须同时包含以下两部分**，缺一不可：

1. **Markdown 报告主体** - 人类可读的测试报告（章节、问题列表、建议）
2. **JSON 数据块** - 包裹在 ```json ... ``` 代码围栏中的结构化数据，置于报告末尾

> 注意：JSON 数据块**不是可选项**，而是报告文件的**必备组成部分**。它会被上传脚本解析以提取结构化字段。如果缺失 JSON 块，报告将被视为不合规，必须重新生成。

### 自检清单（生成报告前必须逐项确认）

- [ ] 报告文件以 `# 测试报告:` 开头
- [ ] 包含元信息（日期、测试人员、版本、代码库地址、文件路径）
- [ ] 包含"测试范围"章节
- [ ] 包含"发现"章节，按严重程度分类列出问题
- [ ] 包含"建议"章节，按优先级排序
- [ ] **报告末尾包含 ```json 代码围栏开始的 JSON 数据块**
- [ ] **JSON 数据块中所有占位符都已替换为真实数据**
- [ ] **JSON 中 `riskStatistics` 各项计数与 Markdown 中 `发现` 章节问题数量完全一致**
- [ ] **JSON 中 `issues` 数组长度等于 `riskStatistics.totalIssues`**

---

## 完整报告模板（Markdown + JSON 必须一起输出）

下方整个代码块即为模型应输出的**完整报告文件内容结构**，包括末尾的 JSON 数据块。

```markdown
# 测试报告: {{FUNCTION_NAME}}

**远程记录地址**: {{REMOTE_REPORT_URL}}
**日期**: {{REPORT_DATE}}
**测试人员**: {{TESTER_NAME}}
**版本**: {{VERSION_INFO}}
**代码库地址**: {{CODEBASE_URL}}

## 涉及分析文件
- **文件路径**: {{FILE_PATH}}

## 测试范围
{{TEST_SCOPE_ITEMS}}

## 发现

### [关键] {{CRITICAL_ISSUE_TITLE}}
- **位置**: {{CRITICAL_ISSUE_LOCATION}} (行号: {{CRITICAL_ISSUE_LINE}})
- **重现步骤**:
  {{CRITICAL_ISSUE_STEPS}}
- **期望**: {{CRITICAL_ISSUE_EXPECTED}}
- **实际**: {{CRITICAL_ISSUE_ACTUAL}}
- **影响**: {{CRITICAL_ISSUE_IMPACT}}
- **修复**: {{CRITICAL_ISSUE_FIX}}

### [高] {{HIGH_ISSUE_TITLE}}
- **位置**: {{HIGH_ISSUE_LOCATION}} (行号: {{HIGH_ISSUE_LINE}})
- **描述**: {{HIGH_ISSUE_DESCRIPTION}}
- **影响**: {{HIGH_ISSUE_IMPACT}}
- **修复**: {{HIGH_ISSUE_FIX}}

### [中] {{MEDIUM_ISSUE_TITLE}}
- **详情**: {{MEDIUM_ISSUE_DETAILS}}

### [低] {{LOW_ISSUE_TITLE}}
- **详情**: {{LOW_ISSUE_DETAILS}}

## 建议

{{PRIORITIZED_RECOMMENDATIONS}}

---

## 结构化数据 (供程序解析，请勿删除)

​```json
{
  "testerName": "{{TESTER_NAME}}",
  "versionInfo": "{{VERSION_INFO}}",
  "reportDate": "{{REPORT_DATE}}",
  "functionName": "{{FUNCTION_NAME}}",
  "codebaseUrl": "{{CODEBASE_URL}}",
  "filePath": "{{FILE_PATH}}",
  "testScopeItems": ["项目1", "项目2"],
  "issues": [
    {
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "title": "问题标题",
      "location": "问题位置",
      "steps": "重现步骤",
      "expected": "期望结果",
      "actual": "实际结果",
      "description": "问题描述",
      "details": "问题详情",
      "impact": "影响说明",
      "fix": "修复建议"
    }
  ],
  "riskStatistics": {
    "criticalCount": 0,
    "highCount": 0,
    "mediumCount": 0,
    "lowCount": 0,
    "totalIssues": 0
  },
  "prioritizedRecommendations": ["建议1", "建议2"]
}
​```
```

> 提示：上方模板中 ```json 前后的 `​`(零宽字符) 仅为防止当前文档嵌套围栏冲突而添加的视觉占位。**模型实际输出报告时，必须使用标准的三反引号** ```json ... ``` **作为 JSON 围栏，不得包含任何零宽字符或转义符号**。

---

## 模板变量说明

- `{{FUNCTION_NAME}}` - 被测试的功能名称
- `{{REMOTE_REPORT_URL}}` - 远程记录地址（报告上传成功后由服务端返回，生成时可填写"待上传"）
- `{{REPORT_DATE}}` - 报告生成日期 (YYYY-MM-DD格式)
- `{{TESTER_NAME}}` - 测试人员姓名
- `{{VERSION_INFO}}` - 版本信息 (分支及版本号)
- `{{CODEBASE_URL}}` - 代码库地址（git remote url 或本地路径）
- `{{FILE_PATH}}` - 被分析文件的绝对路径
- `{{TEST_SCOPE_ITEMS}}` - 测试范围项目列表，格式为"- [x] 项目名称"，每行一个
- `{{CRITICAL_ISSUE_*}}` / `{{HIGH_ISSUE_*}}` / `{{MEDIUM_ISSUE_*}}` / `{{LOW_ISSUE_*}}` - 各严重级别问题字段；若某级别无问题，删除对应整段，不要保留空标题
- `{{CRITICAL_ISSUE_LINE}}` / `{{HIGH_ISSUE_LINE}}` - 各严重级别问题对应的行号（必须提供具体数字）
- `{{PRIORITIZED_RECOMMENDATIONS}}` - 按优先级排序的建议列表，格式为"1. **优先级**: 建议内容"

## JSON 数据块字段约束

- `severity` 取值必须严格为：`CRITICAL`、`HIGH`、`MEDIUM`、`LOW` 之一（大写）
- `riskStatistics.totalIssues` 必须等于 `criticalCount + highCount + mediumCount + lowCount`
- `issues` 数组中每个对象的字段必须与 Markdown 中"发现"章节的问题一一对应
- 不存在的字段填写空字符串 `""`，不要使用 `null` 或省略键
- 数组类字段（`testScopeItems`、`issues`、`prioritizedRecommendations`）不得为 `null`，至少为空数组 `[]`

## 使用说明

1. 所有模板变量必须被实际数据替换，**不能保留 `{{...}}` 占位符**
2. 严重程度标签必须使用标准定义：CRITICAL、HIGH、MEDIUM、LOW
3. 建议必须按优先级排序：立即、高优先级、中优先级、低优先级
4. **JSON 数据块必须位于报告文件末尾，且与 Markdown 主体内容保持完全一致**
5. 如果某严重级别下没有问题，Markdown 中删除对应章节，JSON 中对应 count 设为 0，并在 issues 数组中省略相关条目