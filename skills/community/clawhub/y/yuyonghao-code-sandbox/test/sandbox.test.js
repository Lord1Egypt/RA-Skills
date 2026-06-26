/**
 * Code Sandbox Test Suite
 * 
 * Tests for all supported languages and edge cases
 */

const { CodeSandbox } = require('../src/sandbox');
const assert = require('assert');

const sandbox = new CodeSandbox({
  defaultTimeout: 10000,
  tmpDir: './test-tmp',
});

let passed = 0;
let failed = 0;

async function test(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    failed++;
  }
}

async function runTests() {
  console.log('🧪 Code Sandbox Test Suite\n');
  console.log('=' .repeat(50));
  
  // Test 1: Node.js Basic Execution
  await test('Node.js: Basic execution', async () => {
    const result = await sandbox.execute({
      language: 'node',
      code: 'console.log("Hello World!");',
    });
    
    assert.strictEqual(result.success, true);
    assert.strictEqual(result.output.trim(), 'Hello World!');
    assert.strictEqual(result.error, '');
  });
  
  // Test 2: Node.js Math
  await test('Node.js: Math operations', async () => {
    const result = await sandbox.execute({
      language: 'node',
      code: 'console.log(2 + 2 * 3);',
    });
    
    assert.strictEqual(result.success, true);
    assert.strictEqual(result.output.trim(), '8');
  });
  
  // Test 3: Node.js Error Handling
  await test('Node.js: Error handling', async () => {
    const result = await sandbox.execute({
      language: 'node',
      code: 'throw new Error("Test error");',
    });
    
    assert.strictEqual(result.success, false);
    assert.ok(result.error.includes('Error'));
  });
  
  // Test 4: Python Basic Execution
  await test('Python: Basic execution', async () => {
    const result = await sandbox.execute({
      language: 'python',
      code: 'print("Hello from Python!")',
    });
    
    assert.strictEqual(result.success, true);
    assert.ok(result.output.includes('Hello from Python!'));
  });
  
  // Test 5: Python Math
  await test('Python: Math operations', async () => {
    const result = await sandbox.execute({
      language: 'python',
      code: 'print(2 + 2 * 3)',
    });
    
    assert.strictEqual(result.success, true);
    assert.strictEqual(result.output.trim(), '8');
  });
  
  // Test 6: Python Error
  await test('Python: Error handling', async () => {
    const result = await sandbox.execute({
      language: 'python',
      code: 'raise Exception("Test error")',
    });
    
    assert.strictEqual(result.success, false);
  });
  
  // Test 7: Invalid Language
  await test('Error: Invalid language', async () => {
    const result = await sandbox.execute({
      language: 'invalid',
      code: 'console.log("test")',
    });
    
    assert.strictEqual(result.success, false);
    assert.ok(result.error.includes('Unsupported language'));
  });
  
  // Test 8: Missing Code
  await test('Error: Missing code', async () => {
    const result = await sandbox.execute({
      language: 'node',
      code: '',
    });
    
    assert.strictEqual(result.success, false);
  });
  
  // Test 9: Execution History
  await test('Feature: Execution history', async () => {
    await sandbox.execute({
      language: 'node',
      code: 'console.log("test")',
    });
    
    const history = sandbox.getHistory(10);
    assert.ok(Array.isArray(history));
    assert.ok(history.length > 0);
  });
  
  // Test 10: Supported Languages
  await test('Feature: Get supported languages', async () => {
    const languages = sandbox.getSupportedLanguages();
    assert.ok(Array.isArray(languages));
    assert.ok(languages.length >= 4); // node, python, go, rust
  });
  
  // Test 11: Timeout (should complete within timeout)
  await test('Node.js: Quick execution', async () => {
    const startTime = Date.now();
    const result = await sandbox.execute({
      language: 'node',
      code: 'console.log("fast");',
      config: { timeout: 5000 }
    });
    const duration = Date.now() - startTime;
    
    assert.strictEqual(result.success, true);
    assert.ok(duration < 5000, 'Should complete within timeout');
  });
  
  // Test 12: Multiple Executions
  await test('Feature: Multiple executions', async () => {
    const results = [];
    for (let i = 0; i < 3; i++) {
      const result = await sandbox.execute({
        language: 'node',
        code: `console.log("Execution ${i}");`,
      });
      results.push(result);
    }
    
    assert.strictEqual(results.length, 3);
    results.forEach((r, i) => {
      assert.strictEqual(r.success, true);
      assert.ok(r.output.includes(`Execution ${i}`));
    });
  });
  
  console.log('=' .repeat(50));
  console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
  console.log(`⏱️  Total tests: ${passed + failed}\n`);
  
  if (failed > 0) {
    process.exit(1);
  }
}

runTests().catch(error => {
  console.error('Test suite error:', error);
  process.exit(1);
});
