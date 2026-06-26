/**
 * Code Refactor Test Suite
 */

const { CodeRefactor, CodeAnalyzer, RefactoringEngine, ChangeApplier, TestValidator } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Simple test framework
class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('\n🧪 Running Code Refactor Tests\n');
    console.log('=' .repeat(50));
    
    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✅ PASS: ${name}`);
        this.passed++;
      } catch (error) {
        console.log(`❌ FAIL: ${name}`);
        console.log(`   Error: ${error.message}`);
        this.failed++;
      }
    }
    
    console.log('=' .repeat(50));
    console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
    console.log(`Success Rate: ${((this.passed / this.tests.length) * 100).toFixed(1)}%\n`);
    
    return this.failed === 0;
  }

  assert(condition, message) {
    if (!condition) {
      throw new Error(message || 'Assertion failed');
    }
  }

  assertEquals(actual, expected, message) {
    if (actual !== expected) {
      throw new Error(message || `Expected ${expected}, got ${actual}`);
    }
  }
}

const runner = new TestRunner();

// Create test file
const testDir = path.join(__dirname, 'fixtures');
if (!fs.existsSync(testDir)) {
  fs.mkdirSync(testDir, { recursive: true });
}

const testFile = path.join(testDir, 'test-code.js');
const testCode = `
function calculateTotal(price, quantity, tax, discount, shipping) {
  if (price > 0) {
    if (quantity > 0) {
      if (tax > 0) {
        if (discount > 0) {
          if (shipping > 0) {
            let subtotal = price * quantity;
            let taxAmount = subtotal * 0.08;
            let discountAmount = subtotal * 0.10;
            let total = subtotal + taxAmount - discountAmount + shipping;
            return total;
          }
        }
      }
    }
  }
  return 0;
}

function processData(data) {
  let unused = 42;
  let result = 0;
  for (let i = 0; i < 1000; i++) {
    if (data[i] > 50) {
      result += data[i] * 2;
    } else if (data[i] > 25) {
      result += data[i] * 1.5;
    } else if (data[i] > 10) {
      result += data[i];
    } else {
      result += 5;
    }
  }
  return result;
}
`;

fs.writeFileSync(testFile, testCode);

// Test 1: CodeAnalyzer - Basic Analysis
runner.test('CodeAnalyzer should analyze a file', () => {
  const analyzer = new CodeAnalyzer();
  const result = analyzer.analyze(testFile);
  
  runner.assert(result.filePath === testFile, 'File path should match');
  runner.assert(result.metrics.totalLines > 0, 'Should have lines');
  runner.assert(result.issues.length > 0, 'Should detect issues');
});

// Test 2: CodeAnalyzer - Detect Long Function
runner.test('CodeAnalyzer should detect long functions', () => {
  const analyzer = new CodeAnalyzer({ maxFunctionLength: 10 });
  const result = analyzer.analyze(testFile);
  
  const longFunctionIssue = result.issues.find(i => i.type === 'long-function');
  runner.assert(longFunctionIssue, 'Should detect long function');
});

// Test 3: CodeAnalyzer - Detect Too Many Parameters
runner.test('CodeAnalyzer should detect too many parameters', () => {
  const analyzer = new CodeAnalyzer({ maxParameters: 3 });
  const result = analyzer.analyze(testFile);
  
  const paramIssue = result.issues.find(i => i.type === 'too-many-parameters');
  runner.assert(paramIssue, 'Should detect too many parameters');
});

// Test 4: CodeAnalyzer - Detect Deep Nesting
runner.test('CodeAnalyzer should detect deep nesting', () => {
  const analyzer = new CodeAnalyzer({ maxNestingDepth: 2 });
  const result = analyzer.analyze(testFile);
  
  const nestingIssue = result.issues.find(i => i.type === 'deep-nesting');
  runner.assert(nestingIssue, 'Should detect deep nesting');
});

// Test 5: CodeAnalyzer - Detect High Complexity
runner.test('CodeAnalyzer should detect high complexity', () => {
  const analyzer = new CodeAnalyzer({ complexityThreshold: 5 });
  const result = analyzer.analyze(testFile);
  
  const complexityIssue = result.issues.find(i => i.type === 'high-complexity');
  runner.assert(complexityIssue, 'Should detect high complexity');
});

// Test 6: CodeAnalyzer - Detect Magic Numbers
runner.test('CodeAnalyzer should detect magic numbers', () => {
  const analyzer = new CodeAnalyzer();
  const result = analyzer.analyze(testFile);
  
  const magicNumberIssue = result.issues.find(i => i.type === 'magic-number');
  runner.assert(magicNumberIssue, 'Should detect magic numbers');
});

// Test 7: RefactoringEngine - Generate Plan
runner.test('RefactoringEngine should generate refactoring plan', () => {
  const analyzer = new CodeAnalyzer();
  const refactorer = new RefactoringEngine();
  
  const analysis = analyzer.analyze(testFile);
  const plan = refactorer.generateRefactoringPlan(analysis);
  
  runner.assert(plan.filePath === testFile, 'Plan should reference file');
  runner.assert(plan.changes.length > 0, 'Should have changes');
  runner.assert(plan.summary.totalChanges > 0, 'Should have total changes');
});

// Test 8: RefactoringEngine - Export Plan
runner.test('RefactoringEngine should export plan as markdown', () => {
  const analyzer = new CodeAnalyzer();
  const refactorer = new RefactoringEngine();
  
  const analysis = analyzer.analyze(testFile);
  const plan = refactorer.generateRefactoringPlan(analysis);
  const markdown = refactorer.exportPlan(plan, 'markdown');
  
  runner.assert(markdown.includes('# Refactoring Plan'), 'Should have header');
  runner.assert(markdown.includes('Total Changes'), 'Should have summary');
});

// Test 9: ChangeApplier - Dry Run Mode
runner.test('ChangeApplier should support dry-run mode', async () => {
  const applier = new ChangeApplier({ dryRun: true });
  
  const change = {
    type: 'extract-constant',
    location: { line: 1, column: 1 },
    original: 'Magic number: 42'
  };
  
  const result = await applier.applyChange(change, { filePath: testFile });
  
  runner.assert(result.success, 'Dry run should succeed');
  runner.assert(result.dryRun, 'Should indicate dry run');
});

// Test 10: TestValidator - Syntax Check
runner.test('TestValidator should check syntax', async () => {
  const validator = new TestValidator();
  
  const result = await validator.checkSyntax(testFile);
  
  runner.assert(result.valid, 'Valid code should pass syntax check');
});

// Test 11: CodeRefactor - Full Integration
runner.test('CodeRefactor should perform full refactor flow', async () => {
  const refactor = new CodeRefactor();
  
  const result = await refactor.refactor(testFile, { dryRun: true });
  
  runner.assert(result.filePath === testFile, 'Should reference file');
  runner.assert(result.analysis, 'Should have analysis');
  runner.assert(result.plan, 'Should have plan');
  runner.assert(result.status === 'dry-run', 'Should be dry run');
});

// Test 12: CodeRefactor - Export Report
runner.test('CodeRefactor should export report', async () => {
  const refactor = new CodeRefactor();
  
  const result = await refactor.refactor(testFile, { dryRun: true });
  const report = refactor.exportReport(result, 'markdown');
  
  runner.assert(report.includes('# Code Refactoring Report'), 'Should have header');
  runner.assert(report.includes(testFile), 'Should reference file');
});

// Run tests
runner.run().then(success => {
  // Cleanup
  if (fs.existsSync(testDir)) {
    fs.rmSync(testDir, { recursive: true });
  }
  
  process.exit(success ? 0 : 1);
});
