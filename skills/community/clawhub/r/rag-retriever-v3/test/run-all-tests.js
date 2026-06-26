/**
 * RAG 3.0 测试运行器
 * 运行所有测试
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const tests = [
  { name: '单元测试', file: 'unit.test.js' },
  { name: '集成测试', file: 'integration.test.js' },
  { name: '中文测试', file: 'chinese.test.js' }
];

async function runTest(testFile) {
  return new Promise((resolve) => {
    const testPath = join(__dirname, testFile);
    const child = spawn('node', [testPath], {
      stdio: 'inherit',
      cwd: process.cwd()
    });

    child.on('close', (code) => {
      resolve(code === 0);
    });
  });
}

async function main() {
  console.log('🦞 RAG 3.0 测试套件\n');
  console.log('='.repeat(50));

  let totalPassed = 0;
  let totalFailed = 0;

  for (const test of tests) {
    console.log(`\n📦 运行: ${test.name}`);
    console.log('-'.repeat(50));
    
    const success = await runTest(test.file);
    
    if (success) {
      console.log(`✅ ${test.name} 通过`);
      totalPassed++;
    } else {
      console.log(`❌ ${test.name} 失败`);
      totalFailed++;
    }
  }

  console.log('\n' + '='.repeat(50));
  console.log(`测试总结: ${totalPassed} 通过, ${totalFailed} 失败`);
  console.log('='.repeat(50));

  process.exit(totalFailed > 0 ? 1 : 0);
}

main().catch(error => {
  console.error('测试运行器错误:', error);
  process.exit(1);
});
