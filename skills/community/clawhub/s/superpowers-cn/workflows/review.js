/**
 * 超能力 CN - 审核阶段
 * 
 * 验证执行结果是否符合需求
 */

/**
 * 审核检查清单
 */
export const reviewChecklist = [
  { item: '功能完整性', passed: false },
  { item: '代码质量', passed: false },
  { item: '错误处理', passed: false },
  { item: '文档完整性', passed: false },
  { item: '测试覆盖', passed: false }
];

/**
 * 执行代码审核
 * @param {object} context - 执行上下文
 */
export async function reviewCode(context) {
  const { files, requirements } = context;
  const results = [];
  
  for (const file of files) {
    const report = {
      file: file.path,
      issues: [],
      suggestions: []
    };
    
    // 检查基本质量问题
    if (file.content.length > 1000) {
      report.suggestions.push('文件较长，考虑拆分');
    }
    
    if (!file.content.includes('error') && !file.content.includes('Error')) {
      report.issues.push('缺少错误处理');
    }
    
    results.push(report);
  }
  
  return results;
}

/**
 * 生成审核报告
 * @param {object} executionResult - 执行结果
 * @param {object} requirements - 原始需求
 */
export function generateReviewReport(executionResult, requirements) {
  const passedItems = reviewChecklist.filter(item => item.passed);
  const failedItems = reviewChecklist.filter(item => !item.passed);
  
  return `
## 🔍 审核报告

### 通过项 ✓
${passedItems.length > 0 
  ? passedItems.map(i => `- ${i.item}`).join('\n')
  : '无'}

### 未通过项 ✗
${failedItems.length > 0
  ? failedItems.map(i => `- ${i.item}`).join('\n')
  : '无'}

### 执行摘要
- 完成步骤: ${executionResult.completed}
- 失败步骤: ${executionResult.failed}

${failedItems.length > 0 
  ? '⚠️ 有未通过项，建议修复后再交付' 
  : '✅ 所有检查项通过，可以交付'}
  `.trim();
}
