// 示例：如何在项目中使用测试报告上传工具

const { uploadSingleReport, uploadMultipleReports } = require('../scripts/generate-test-report');

// 示例1：上传单个报告
async function uploadSingleTestReport() {
  try {
    const result = await uploadSingleReport('UserController-test-report.md');
    if (result.success) {
      console.log('✅ 报告上传成功');
    } else {
      console.log('❌ 报告上传失败:', result.message);
    }
    return result;
  } catch (error) {
    console.error('上传错误:', error);
    throw error;
  }
}

// 示例2：批量上传多个报告
async function uploadMultipleTestReports() {
  const reportPaths = [
    'UserController-test-report.md',
    'ProductService-test-report.md',
    'OrderController-test-report.md'
  ];
  
  try {
    const results = await uploadMultipleReports(reportPaths);
    
    const successCount = results.filter(r => r.result && r.result.success).length;
    console.log(`批量上传完成: ${successCount}/${results.length} 个报告上传成功`);
    
    return results;
  } catch (error) {
    console.error('批量上传错误:', error);
    throw error;
  }
}

// 示例3：在CI/CD流程中使用
async function uploadReportsInCICD() {
  // 假设测试报告已经生成在reports目录下
  const fs = require('fs');
  const path = require('path');
  
  const reportsDir = './reports';
  if (!fs.existsSync(reportsDir)) {
    console.log('报告目录不存在，跳过上传');
    return;
  }
  
  const reportFiles = fs.readdirSync(reportsDir)
    .filter(file => file.endsWith('.md'))
    .map(file => path.join(reportsDir, file));
  
  if (reportFiles.length === 0) {
    console.log('没有找到测试报告文件，跳过上传');
    return;
  }
  
  console.log(`找到 ${reportFiles.length} 个测试报告，开始上传...`);
  return await uploadMultipleReports(reportFiles);
}

// 导出示例函数
module.exports = { 
  uploadSingleTestReport, 
  uploadMultipleTestReports, 
  uploadReportsInCICD 
};