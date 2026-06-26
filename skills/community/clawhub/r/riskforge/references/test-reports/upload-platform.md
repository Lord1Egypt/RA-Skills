# 测试报告上传平台指南

本指南描述了如何将生成的测试报告上传到指定平台。

## 上传机制

测试报告生成后，通过以下方式上传到平台：

### 自动上传

当skill分析完成时，系统会自动检测并上传所有待处理的报告。

### 手动上传

可以手动触发报告上传：

## API接口

上传功能通过HTTP POST请求发送到以下接口：

- **URL**: `http://ai-testcase.jd.com/aiCase/api/riskforge/saveCodeRiskReports`
- **方法**: POST
- **Content-Type**: application/json

### 请求参数

```json
{
  "reportMessage": "{{REPORT_CONTENT}}",
  "testerName": "{{TESTER_NAME}}",
  "versionInfo": "{{VERSION_INFO}}",
  "reportDate": "{{REPORT_DATE}}",
  "functionName": "{{FUNCTION_NAME}}",
  "codebaseUrl": "{{CODEBASE_URL}}",
  "filePath": "{{FILE_PATH}}",
  "testScopeItems": "{{TEST_SCOPE_ITEMS}}",
  "issues": [
    {
      "severity": "CRITICAL",
      "title": "{{CRITICAL_ISSUE_TITLE}}",
      "location": "{{CRITICAL_ISSUE_LOCATION}}",
      "steps": "{{CRITICAL_ISSUE_STEPS}}",
      "expected": "{{CRITICAL_ISSUE_EXPECTED}}",
      "actual": "{{CRITICAL_ISSUE_ACTUAL}}",
      "impact": "{{CRITICAL_ISSUE_IMPACT}}",
      "fix": "{{CRITICAL_ISSUE_FIX}}"
    },
    {
      "severity": "HIGH",
      "title": "{{HIGH_ISSUE_TITLE}}",
      "location": "{{HIGH_ISSUE_LOCATION}}",
      "description": "{{HIGH_ISSUE_DESCRIPTION}}",
      "impact": "{{HIGH_ISSUE_IMPACT}}",
      "fix": "{{HIGH_ISSUE_FIX}}"
    },
    {
      "severity": "MEDIUM",
      "title": "{{MEDIUM_ISSUE_TITLE}}",
      "details": "{{MEDIUM_ISSUE_DETAILS}}"
    },
    {
      "severity": "LOW",
      "title": "{{LOW_ISSUE_TITLE}}",
      "details": "{{LOW_ISSUE_DETAILS}}"
    }
  ],
  "riskStatistics": {
    "criticalCount": "{{CRITICAL_COUNT}}",
    "highCount": "{{HIGH_COUNT}}",
    "mediumCount": "{{MEDIUM_COUNT}}",
    "lowCount": "{{LOW_COUNT}}",
    "totalIssues": "{{TOTAL_ISSUES}}"
  },
  "prioritizedRecommendations": "{{PRIORITIZED_RECOMMENDATIONS}}"
}
```

**参数说明**：
- `reportMessage`: 完整的Markdown格式测试报告内容
- `testerName`: 测试人员姓名（对应ERP字段）
- `versionInfo`: 版本信息（分支及版本号）
- `reportDate`: 报告生成日期（YYYY-MM-DD格式）
- `functionName`: 被测试的功能名称
- `codebaseUrl`: 代码库URL
- `filePath`: 被分析文件的绝对路径
- `testScopeItems`: 测试范围项目列表
- `issues`: 问题列表数组，包含以下字段：
  - `severity`: 问题严重程度（CRITICAL/HIGH/MEDIUM/LOW）
  - `title`: 问题标题
  - `location`: 问题位置（CRITICAL/HIGH级别）
  - `steps`: 重现步骤（CRITICAL级别）
  - `expected`: 期望结果（CRITICAL级别）
  - `actual`: 实际结果（CRITICAL级别）
  - `description`: 问题描述（HIGH级别）
  - `details`: 问题详情（MEDIUM/LOW级别）
  - `impact`: 问题影响（CRITICAL/HIGH级别）
  - `fix`: 修复建议（CRITICAL/HIGH级别）
- `riskStatistics`: 风险数据统计，包含以下字段：
  - `criticalCount`: 关键问题数量
  - `highCount`: 高优先级问题数量
  - `mediumCount`: 中优先级问题数量
  - `lowCount`: 低优先级问题数量
  - `totalIssues`: 问题总数
- `prioritizedRecommendations`: 按优先级排序的建议列表

### 响应处理

- **成功**: 状态码 200-299，返回远程报告访问地址：
  ```json
  {
    "code": 200,
    "message": "http://ai-testcase.jd.com/#/risk-analysis/detail/{reportId}",
    "data": null
  }
  ```
- **失败**: 状态码 >= 300，返回错误信息：
  ```json
  {
    "code": 500,
    "message": "错误描述",
    "data": null
  }
  ```

**响应说明**：
- 成功时，`message`字段包含完整的远程报告访问URL
- 报告URL格式：`http://ai-testcase.jd.com/#/risk-analysis/detail/{reportId}`
- `reportId`为数据库中保存的报告记录唯一标识

## 报告验证

在上传前，系统会对报告内容进行验证：

1. **内容完整性检查**：确保报告包含实际的测试数据
2. **非零测试检查**：验证是否有非零的测试数量
3. **信息提取**：从Markdown报告中提取测试人员、版本、日期和功能名称等信息

## 错误处理

- **网络错误**：记录错误日志，不影响其他报告处理
- **API错误**：记录状态码和响应内容，继续处理其他报告
- **验证失败**：跳过无效报告的上传

## 使用示例

```javascript
const { uploadReportToAPI } = require('./generate-test-report');

// 上传单个报告
const reportContent = fs.readFileSync('path/to/report.md', 'utf8');
const reportInfo = extractReportInfo(reportContent);

uploadReportToAPI(reportContent, reportInfo)
  .then(response => {
    if (response.code === 200) {
      console.log('报告上传成功');
      console.log('远程报告地址:', response.message);
      
      // 将远程地址添加到原始报告文件
      addRemoteReportUrl('path/to/report.md', response.message);
    } else {
      console.error('报告上传失败:', response.message);
    }
  })
  .catch(error => {
    console.error('上传过程中发生错误:', error);
  });
```