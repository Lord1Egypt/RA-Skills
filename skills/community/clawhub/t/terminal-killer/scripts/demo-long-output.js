#!/usr/bin/env node

/**
 * Terminal Killer - Demo: Long Output Handling
 * 
 * Demonstrates the long output detection and terminal opening workflow.
 * 
 * Usage: node demo-long-output.js
 */

const { handleInput, handleLongOutputResponse } = require('./index');

console.log('═'.repeat(60));
console.log('🧪 Terminal Killer - 长输出处理演示');
console.log('═'.repeat(60));
console.log('');

// Test 1: Long output detection
console.log('📋 测试 1: 检测长输出');
console.log('─'.repeat(60));
const result = handleInput('curl www.baidu.com');

if (result.action === 'long_output') {
  console.log('✅ 检测到长输出');
  console.log('');
  console.log(result.message);
  console.log('');
  
  // Test 2: User responds "是"
  console.log('📋 测试 2: 用户回复"是"');
  console.log('─'.repeat(60));
  const response = handleLongOutputResponse(result.command, '是');
  
  if (response.action === 'open_terminal') {
    console.log('✅ 已打开新 Terminal 窗口');
  }
} else if (result.action === 'execute') {
  console.log('✅ 短输出，直接显示');
  console.log('');
  console.log(result.execution.output.substring(0, 200) + '...');
}

console.log('');
console.log('═'.repeat(60));
console.log('演示完成！');
console.log('═'.repeat(60));
