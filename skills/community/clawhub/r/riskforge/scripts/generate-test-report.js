const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { execSync } = require('child_process');

/**
 * 测试报告生成和上传工具
 * 基于riskforge技能的风险分析结果生成测试报告并上传到平台
 */

// API配置
const API_CONFIG = {
  baseUrl: 'http://ai-testcase.jd.com',
  endpoint: '/aiCase/api/riskforge/saveCodeRiskReports',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  }
};

/**
 * 获取git配置的用户名，如果git获取不到则使用系统登录的账号名称
 * @returns {string} git用户名、系统用户名或兜底值
 */
function getGitUserName() {
  try {
    const gitUserName = execSync('git config user.name', { encoding: 'utf8', timeout: 5000 }).trim();
    if (gitUserName) {
      return gitUserName;
    }
  } catch (error) {
    console.warn('无法获取git用户名，尝试获取系统用户名:', error.message);
  }

  // 尝试获取系统登录的账号名称
  try {
    const os = require('os');
    const systemUsername = process.env.USER || process.env.USERNAME || os.userInfo().username;
    if (systemUsername) {
      console.log('使用系统用户名:', systemUsername);
      return systemUsername;
    }
  } catch (error) {
    console.warn('无法获取系统用户名:', error.message);
  }

  // 如果都无法获取，使用兜底值
  console.warn('无法获取git用户名和系统用户名，使用兜底值');
  return '未知测试人员';
}

/**
 * 获取代码库地址 - 优先通过git获取远程仓库地址，获取不到则使用工程绝对路径
 * @returns {string} 代码库URL或工程绝对路径
 */
function getCodebaseUrl() {
  try {
    // 尝试获取git远程仓库地址
    const gitRemoteUrl = execSync('git config --get remote.origin.url', { encoding: 'utf8', timeout: 5000 }).trim();
    if (gitRemoteUrl) {
      return gitRemoteUrl;
    }
  } catch (error) {
    console.warn('无法通过git获取远程仓库地址:', error.message);
  }

  // 如果无法获取git远程地址，则返回当前工作目录的绝对路径
  try {
    const absolutePath = process.cwd();
    return absolutePath;
  } catch (error) {
    console.warn('无法获取当前工作目录:', error.message);
    return '未知工程路径';
  }
}

/**
 * 从JSON数据块中提取报告信息（优先解析方式）
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {Object|null} 提取的报告信息，如果无JSON块则返回null
 */
function extractFromJsonBlock(reportContent) {

   // 首先尝试查找完整的JSON数据块（包含结束的```）
   let jsonBlockMatch = reportContent.match(/```json\s*([\s\S]*?)\s*```/);

   // 如果未找到完整的JSON数据块，尝试查找不完整的JSON数据块（可能缺少结束的```）
   if (!jsonBlockMatch) {
     jsonBlockMatch = reportContent.match(/```json\s*([\s\S]*?)(?=\n#{2,3}|\n---|$)/);
   }

  try {
    const jsonData = JSON.parse(jsonBlockMatch[1]);

    return {
      testerName: jsonData.testerName || getGitUserName(),
      versionInfo: jsonData.versionInfo || '',
      reportDate: jsonData.reportDate || new Date().toISOString().split('T')[0],
      functionName: jsonData.functionName || '',
      codebaseUrl: jsonData.codebaseUrl || getCodebaseUrl(),
      filePath: jsonData.filePath || '',
      testScopeItems: Array.isArray(jsonData.testScopeItems) ? jsonData.testScopeItems : [],
      issues: Array.isArray(jsonData.issues) ? jsonData.issues : [],
      riskStatistics: jsonData.riskStatistics || {
        criticalCount: 0,
        highCount: 0,
        mediumCount: 0,
        lowCount: 0,
        totalIssues: 0
      },
      prioritizedRecommendations: Array.isArray(jsonData.prioritizedRecommendations)
        ? jsonData.prioritizedRecommendations.join('\n')
        : (jsonData.prioritizedRecommendations || ''),
      _fromJson: true
    };
  } catch (error) {
    console.warn('解析JSON数据块失败:', error.message);
    return null;
  }
}

/**
 * 从Markdown报告中提取信息（后备解析方式）
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {Object} 提取的报告信息
 */
function extractFromMarkdown(reportContent) {
  const info = {
    testerName: '',
    versionInfo: '',
    reportDate: new Date().toISOString().split('T')[0], // 默认当前日期
    functionName: '',
    codebaseUrl: '',
    filePath: '',
    testScopeItems: []
  };

  // 提取测试人员姓名 - 优先使用git配置的用户名，其次从报告中提取，最后使用兜底值
  info.testerName = getGitUserName();

  // 提取版本信息 - 适配新的报告格式
  const versionMatch = reportContent.match(/\*\*版本\*\*[:：]?\s*([^\n]+)/);
  if (versionMatch) {
    info.versionInfo = versionMatch[1].trim();
  }

  // 提取报告日期 - 适配新的报告格式
  const dateMatch = reportContent.match(/\*\*日期\*\*[:：]?\s*(\d{4}-\d{2}-\d{2})/);
  if (dateMatch) {
    info.reportDate = dateMatch[1];
  }

  // 提取功能名称 - 从标题提取
  const titleMatch = reportContent.match(/#\s+测试报告[:：]?\s*(.+)/);
  if (titleMatch) {
    info.functionName = titleMatch[1].trim();
  }

  // 提取代码库URL - 优先通过git获取，否则使用报告中的地址
  info.codebaseUrl = getCodebaseUrl();

  // 如果git获取失败且报告中有代码库地址，则使用报告中的地址
  if (!info.codebaseUrl || info.codebaseUrl === '未知工程路径') {
    const repoMatch = reportContent.match(/\*\*代码库地址\*\*[:：]?\s*([^\n]+)/);
    if (repoMatch) {
      info.codebaseUrl = repoMatch[1].trim();
    }
  }

  // 提取文件路径 - 从涉及文件部分提取
  const fileMatch = reportContent.match(/##\s+涉及分析文件[\s\S]*?`([^`]+)`/);
  if (fileMatch) {
    info.filePath = fileMatch[1].trim();
  }

  // 提取测试范围 - 适配新的报告格式
  const scopeMatch = reportContent.match(/##\s+测试范围[\s\S]*?\n([\s\S]*?)(?=\n##|\n#|$)/);
  if (scopeMatch) {
    const scopeContent = scopeMatch[1].trim();
    // 提取列表项
    const items = scopeContent.match(/^-\s*(.+)/gm);
    if (items) {
      info.testScopeItems = items.map(item => item.replace(/^-\s*/, '').trim());
    }
  }

  return info;
}

/**
 * 从Markdown报告中提取信息（主入口）
 * 优先从JSON数据块解析，失败则回退到Markdown解析
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {Object} 提取的报告信息
 */
function extractReportInfo(reportContent) {
  // 优先尝试从JSON数据块解析
  const jsonInfo = extractFromJsonBlock(reportContent);
  if (jsonInfo && jsonInfo._fromJson) {
    console.log('✓ 成功从JSON数据块解析报告参数');
    return jsonInfo;
  }
}

/**
 * 解析Markdown报告中的问题
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {Array} 问题列表
 */
function parseIssuesFromReport(reportContent) {
  const issues = [];

  // 按严重程度分割报告内容
  const sections = reportContent.split(/#{2,3}\s+/);

  sections.forEach(section => {
    if (section.includes('关键问题') || section.includes('严重问题')) {
      const criticalIssues = parseCriticalIssues(section);
      issues.push(...criticalIssues);
    } else if (section.includes('高优先级问题')) {
      const highIssues = parseHighIssues(section);
      issues.push(...highIssues);
    } else if (section.includes('中优先级问题')) {
      const mediumIssues = parseMediumIssues(section);
      issues.push(...mediumIssues);
    } else if (section.includes('低优先级问题')) {
      const lowIssues = parseLowIssues(section);
      issues.push(...lowIssues);
    }
  });

  return issues;
}

/**
 * 解析关键问题
 */
function parseCriticalIssues(section) {
  const issues = [];
  const issueBlocks = section.split(/\n(?=#{4}\s+)/);

  issueBlocks.forEach(block => {
    if (block.trim() && !block.startsWith('关键问题') && !block.startsWith('严重问题')) {
      const issue = {
        severity: 'CRITICAL',
        title: extractField(block, '问题'),
        location: extractField(block, '位置'),
        steps: extractField(block, '重现步骤'),
        expected: extractField(block, '期望结果'),
        actual: extractField(block, '实际结果'),
        impact: extractField(block, '影响'),
        fix: extractField(block, '修复建议')
      };

      if (issue.title) {
        issues.push(issue);
      }
    }
  });

  return issues;
}

/**
 * 解析高优先级问题
 */
function parseHighIssues(section) {
  const issues = [];
  const issueBlocks = section.split(/\n(?=#{4}\s+)/);

  issueBlocks.forEach(block => {
    if (block.trim() && !block.startsWith('高优先级问题')) {
      const issue = {
        severity: 'HIGH',
        title: extractField(block, '问题'),
        location: extractField(block, '位置'),
        description: extractField(block, '描述'),
        impact: extractField(block, '影响'),
        fix: extractField(block, '修复建议')
      };

      if (issue.title) {
        issues.push(issue);
      }
    }
  });

  return issues;
}

/**
 * 解析中优先级问题
 */
function parseMediumIssues(section) {
  const issues = [];
  const issueBlocks = section.split(/\n(?=#{4}\s+)/);

  issueBlocks.forEach(block => {
    if (block.trim() && !block.startsWith('中优先级问题')) {
      const issue = {
        severity: 'MEDIUM',
        title: extractField(block, '问题'),
        details: extractField(block, '详情') || extractField(block, '描述')
      };

      if (issue.title) {
        issues.push(issue);
      }
    }
  });

  return issues;
}

/**
 * 解析低优先级问题
 */
function parseLowIssues(section) {
  const issues = [];
  const issueBlocks = section.split(/\n(?=#{4}\s+)/);

  issueBlocks.forEach(block => {
    if (block.trim() && !block.startsWith('低优先级问题')) {
      const issue = {
        severity: 'LOW',
        title: extractField(block, '问题'),
        details: extractField(block, '详情') || extractField(block, '描述')
      };

      if (issue.title) {
        issues.push(issue);
      }
    }
  });

  return issues;
}

/**
 * 从文本块中提取字段值
 */
function extractField(text, fieldName) {
  const patterns = [
    new RegExp(`${fieldName}[:：]\\s*(.+?)(?=\\n#{4}|\\n##|\\n###|$)`, 's'),
    new RegExp(`${fieldName}[:：]\\s*(.+?)(?=\\n\\n|\\n#{2,3}|$)`, 's'),
    new RegExp(`${fieldName}[:：]\\s*(.+)`, 'i')
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[1].trim();
    }
  }

  return '';
}

/**
 * 计算风险统计
 * @param {Array} issues - 问题列表
 * @returns {Object} 风险统计数据
 */
function calculateRiskStatistics(issues) {
  const stats = {
    criticalCount: 0,
    highCount: 0,
    mediumCount: 0,
    lowCount: 0,
    totalIssues: issues.length
  };

  issues.forEach(issue => {
    switch (issue.severity) {
      case 'CRITICAL':
        stats.criticalCount++;
        break;
      case 'HIGH':
        stats.highCount++;
        break;
      case 'MEDIUM':
        stats.mediumCount++;
        break;
      case 'LOW':
        stats.lowCount++;
        break;
    }
  });

  return stats;
}

/**
 * 提取优先建议
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {string} 优先建议列表
 */
function extractRecommendations(reportContent) {
  const recommendations = [];

  // 查找建议部分
  const recommendationsMatch = reportContent.match(/#{2,3}\s+优先建议[\s\S]*?(?=\n#{2,3}|$)/);
  if (recommendationsMatch) {
    const recommendationsSection = recommendationsMatch[0];

    // 提取列表项
    const items = recommendationsSection.match(/\d+\.\s*(.+)/g);
    if (items) {
      items.forEach(item => {
        recommendations.push(item.replace(/^\d+\.\s*/, '').trim());
      });
    }
  }

  return recommendations.join('\n');
}

/**
 * 发送HTTP请求
 * @param {Object} options - HTTP请求选项
 * @param {string} data - 请求数据
 * @returns {Promise} 响应Promise
 */
function sendHttpRequest(options, data) {
  return new Promise((resolve, reject) => {
    const protocol = options.protocol === 'https:' ? https : http;
    const req = protocol.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const parsedData = JSON.parse(responseData);
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            data: parsedData
          });
        } catch (error) {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            data: responseData
          });
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    if (data) {
      req.write(data);
    }

    req.end();
  });
}

/**
 * 上传报告到API
 * @param {string} reportContent - 完整的Markdown报告内容
 * @param {Object} reportInfo - 提取的报告信息（可选）
 * @returns {Promise<Object>} 上传结果
 */
async function uploadReportToAPI(reportContent, reportInfo = null) {
  try {
    // 如果未提供reportInfo，则自动提取
    if (!reportInfo) {
      reportInfo = extractReportInfo(reportContent);
    }

    // 验证报告内容
    if (!validateReportContent(reportContent)) {
      throw new Error('报告内容验证失败：报告内容不完整或无效');
    }

    const params = {
        "reportMessage":reportContent,
         "params":JSON.stringify(reportInfo)
    }
    // 打印请求参数
    console.log('=== 请求参数 ===');
    console.log('URL:', API_CONFIG.baseUrl + API_CONFIG.endpoint);
    console.log('Method:', API_CONFIG.method);
    console.log('Headers:', API_CONFIG.headers);
    console.log('Request Data:', JSON.stringify(params, null, 2));

    // 准备HTTP请求
    const url = new URL(API_CONFIG.baseUrl + API_CONFIG.endpoint);
    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method: API_CONFIG.method,
      headers: {
        ...API_CONFIG.headers,
        'Content-Length': Buffer.byteLength(JSON.stringify(params))
      }
    };

    console.log('正在上传报告到:', API_CONFIG.baseUrl + API_CONFIG.endpoint);

    // 发送请求
    const response = await sendHttpRequest(options, JSON.stringify(params));

    // 打印响应参数
    console.log('=== 响应参数 ===');
    console.log('Status Code:', response.statusCode);
    console.log('Headers:', response.headers);
    console.log('Response Data:', JSON.stringify(response.data, null, 2));

    // 处理响应
    if (response.statusCode >= 200 && response.statusCode < 300) {
      console.log('报告上传成功');
      return response.data;
    } else {
      console.error('报告上传失败，状态码:', response.statusCode);
      throw new Error(`API请求失败: ${response.statusCode} - ${JSON.stringify(response.data)}`);
    }
  } catch (error) {
    console.error('上传报告时发生错误:', error.message);
    throw error;
  }
}

/**
 * 验证报告内容
 * @param {string} reportContent - 报告内容
 * @returns {boolean} 是否有效
 */
function validateReportContent(reportContent) {
  if (!reportContent || reportContent.trim().length === 0) {
    return false;
  }

  // 检查是否包含基本结构 - 标题和发现部分
  if (!reportContent.includes('#') || (!reportContent.includes('问题') && !reportContent.includes('发现'))) {
    return false;
  }

  return true;
}

/**
 * 将远程报告URL添加到原始报告文件
 * @param {string} filePath - 报告文件路径
 * @param {string} remoteUrl - 远程报告URL
 */
function addRemoteReportUrl(filePath, remoteUrl) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');

    // 如果已经存在远程URL，则不重复添加
    if (content.includes('远程报告地址')) {
      return;
    }

    // 在文件末尾添加远程报告地址
    const remoteUrlSection = `\n\n---\n\n## 远程报告地址\n\n[查看在线报告](${remoteUrl})\n`;
    content += remoteUrlSection;

    fs.writeFileSync(filePath, content, 'utf8');
    console.log('已添加远程报告地址到文件:', filePath);
  } catch (error) {
    console.error('添加远程报告地址失败:', error.message);
  }
}

// 导出函数供外部使用
module.exports = {
  extractReportInfo,
  parseIssuesFromReport,
  calculateRiskStatistics,
  uploadReportToAPI,
  addRemoteReportUrl,
  validateReportContent
};

// 如果直接运行此脚本，则执行单个报告上传
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法:');
    console.log('  node generate-test-report.js <报告文件路径>');
    process.exit(1);
  }

  const filePath = args[0];
  console.log('正在上传报告:', filePath);

  uploadReportToAPIFromFile(filePath)
    .then(result => {
      console.log('报告上传成功');
      console.log('远程报告地址:', result.message);
    })
    .catch(error => {
      console.error('报告上传失败:', error.message);
      process.exit(1);
    });
}

/**
 * 从文件上传报告的便捷函数
 * @param {string} filePath - 报告文件路径
 * @returns {Promise<Object>} 上传结果
 */
async function uploadReportToAPIFromFile(filePath) {
  const reportContent = fs.readFileSync(filePath, 'utf8');
  const result = await uploadReportToAPI(reportContent);

  // 添加远程报告地址到原始文件
  if (result.message) {
    addRemoteReportUrl(filePath, result.message);
  }

  return result;
}