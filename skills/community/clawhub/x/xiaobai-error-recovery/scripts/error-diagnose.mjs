#!/usr/bin/env node
/**
 * Error Diagnose - 错误诊断助手
 * 用法: node error-diagnose.mjs --error "ENOENT" --context "读取文件"
 */

const ERROR_KNOWLEDGE_BASE = {
  // 文件系统错误
  'ENOENT': {
    name: '文件不存在',
    commonCauses: ['路径错误', '文件名拼写错误', '文件已被删除'],
    quickFix: '用 ls 命令确认文件存在，检查路径拼写',
    suggestions: [
      '检查文件路径是否正确',
      '使用 ls -la 确认文件存在',
      '检查是否有addendum文件',
      '尝试使用绝对路径'
    ]
  },
  'EACCES': {
    name: '权限不足',
    commonCauses: ['文件权限不足', '需要sudo', '用户组不正确'],
    quickFix: '检查chmod权限，或尝试sudo',
    suggestions: [
      '检查文件权限: ls -la',
      '修改权限: chmod 644/600',
      '切换到正确用户组',
      '使用sudo（慎用）'
    ]
  },
  'EISDIR': {
    name: '期望文件但得到目录',
    commonCauses: ['路径指向了目录而不是文件'],
    quickFix: '检查路径，确保指向文件而非目录',
    suggestions: ['添加文件名', '检查路径层级']
  },
  
  // HTTP错误
  '401': {
    name: '未授权',
    commonCauses: ['Token过期', '权限不足', '未登录'],
    quickFix: '检查API key/token，重新认证',
    suggestions: [
      '检查API key是否过期',
      '重新设置环境变量',
      '检查权限范围'
    ]
  },
  '403': {
    name: '禁止访问',
    commonCauses: ['权限不足', 'IP限制', 'Token正确但权限不够'],
    quickFix: '检查权限设置，确认有访问权',
    suggestions: [
      '检查token权限范围',
      '确认有该资源访问权',
      '检查IP白名单'
    ]
  },
  '404': {
    name: '资源不存在',
    commonCauses: ['URL错误', '资源被删除', '路径拼写错误'],
    quickFix: '检查URL/路径，确认资源存在',
    suggestions: [
      '检查URL拼写',
      '用浏览器访问确认存在',
      '检查API版本'
    ]
  },
  '429': {
    name: 'Rate Limit',
    commonCauses: ['请求过于频繁', '达到配额上限'],
    quickFix: '等待后重试，减少请求频率',
    suggestions: [
      '等待60秒后重试',
      '减少并行请求数',
      '检查rate limit header',
      '考虑升级套餐'
    ]
  },
  '500': {
    name: '服务器错误',
    commonCauses: ['服务器内部错误', '服务不可用'],
    quickFix: '等待后重试，或尝试其他服务',
    suggestions: [
      '等待后重试（指数退避）',
      '检查服务状态页面',
      '尝试替代服务'
    ]
  },
  'timeout': {
    name: '超时',
    commonCauses: ['网络慢', '服务器响应慢', '数据量大'],
    quickFix: '增加timeout时间，或分批处理',
    suggestions: [
      '增加timeout参数',
      '减少单次请求数据量',
      '使用异步处理',
      '换网络环境'
    ]
  },
  
  // 进程错误
  'SIGKILL': {
    name: '进程被杀',
    commonCauses: ['OOM（内存不足）', '超时保护', '手动kill'],
    quickFix: '减少内存使用，分批处理',
    suggestions: [
      '减少内存使用',
      '分批处理大数据',
      '检查内存限制',
      '优化算法'
    ]
  },
  'SIGTERM': {
    name: '进程被终止',
    commonCauses: ['正常关机', '超时', '资源回收'],
    quickFix: '检查原因，必要时重新执行',
    suggestions: ['正常终止，检查任务状态', '重新执行']
  }
};

function diagnose(errorCode, context = '') {
  console.log(`🩹 Error Diagnose - 错误诊断\n`);
  console.log(`错误代码: ${errorCode}`);
  if (context) console.log(`上下文: ${context}\n`);
  
  const info = ERROR_KNOWLEDGE_BASE[errorCode];
  
  if (!info) {
    console.log(`⚠️ 未知错误代码: ${errorCode}`);
    console.log(`\n通用建议:`);
    console.log('  1. 搜索错误代码的含义');
    console.log('  2. 检查工具文档');
    console.log('  3. 尝试换一种方法');
    console.log('  4. 如果3次失败，向上汇报');
    return;
  }
  
  console.log(`错误类型: ${info.name}\n`);
  
  console.log('常见原因:');
  info.commonCauses.forEach((cause, i) => {
    console.log(`  ${i + 1}. ${cause}`);
  });
  
  console.log(`\n快速修复: ${info.quickFix}\n`);
  
  console.log('建议尝试:');
  info.suggestions.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s}`);
  });
  
  console.log('\n' + '='.repeat(50));
  console.log('提示: 同一方法最多重试3次');
  console.log('      每次重试必须改变参数');
  console.log('='.repeat(50));
}

function main() {
  const args = process.argv.slice(2);
  
  const errorIdx = args.indexOf('--error');
  const contextIdx = args.indexOf('--context');
  
  const errorCode = errorIdx >= 0 ? args[errorIdx + 1] : null;
  const context = contextIdx >= 0 ? args[contextIdx + 1] : '';
  
  if (!errorCode) {
    console.log('Error Diagnose - 错误诊断助手\n');
    console.log('用法:');
    console.log('  node error-diagnose.mjs --error "ENOENT"');
    console.log('  node error-diagnose.mjs --error "timeout" --context "git push"');
    console.log('\n支持的错误代码:');
    Object.keys(ERROR_KNOWLEDGE_BASE).forEach(code => {
      console.log(`  ${code}: ${ERROR_KNOWLEDGE_BASE[code].name}`);
    });
    return;
  }
  
  diagnose(errorCode, context);
}

main();
