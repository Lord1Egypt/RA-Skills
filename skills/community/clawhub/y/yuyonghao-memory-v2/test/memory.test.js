/**
 * Memory V2 - 主测试入口
 * 运行所有测试
 */

import { run } from 'node:test';
import { spec } from 'node:test/reporters';

// 导入所有测试
import './vector-store.test.js';
import './graph-store.test.js';
import './ner-extractor.test.js';
import './memory-manager.test.js';

console.log('🧪 Memory V2 Test Suite Starting...\n');

// 测试会自动运行
console.log('All test modules loaded. Running tests...\n');
