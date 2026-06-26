/**
 * VOKO Subagent Skill 测试脚本
 */

const path = require('path');

// 模拟 CLI 参数
process.argv = [
  'node',
  'index.js',
  '--visitor-uid=test-visitor-123',
  `--db-path=${path.join(process.cwd(), '..', 'voko', 'data', 'voko.db')}`,
  '--timeout=30'
];

// 运行主程序
require('./index.js');
