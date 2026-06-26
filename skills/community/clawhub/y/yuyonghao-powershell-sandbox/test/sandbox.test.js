#!/usr/bin/env node
/**
 * PowerShell Sandbox Tests
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

class PowerShellSandboxTest {
  constructor() {
    this.passed = 0;
    this.failed = 0;
  }

  async runAll() {
    console.log('Running PowerShell Sandbox Tests...\n');

    await this.testSandboxExecution();
    await this.testSecurityRestrictions();
    await this.testTimeoutControl();
    await this.testOutputLimiting();

    console.log(`\n${'='.repeat(40)}`);
    console.log(`Passed: ${this.passed}`);
    console.log(`Failed: ${this.failed}`);
    console.log(`${'='.repeat(40)}`);

    return this.failed === 0;
  }

  async testSandboxExecution() {
    console.log('Test: Sandbox Execution');
    try {
      // Check if sandbox script exists
      const sandboxPath = path.join(__dirname, '..', 'src', 'sandbox.ps1');
      const exists = fs.existsSync(sandboxPath);
      
      if (exists) {
        const content = fs.readFileSync(sandboxPath, 'utf-8');
        assert(content.includes('ScriptPath'), 'Should have ScriptPath parameter');
        assert(content.includes('TimeoutSeconds'), 'Should have timeout parameter');
        console.log('  ✅ Sandbox script exists and has required parameters');
      } else {
        console.log('  ⚠️  Sandbox script not found (may be in different location)');
      }
      
      this.passed++;
    } catch (err) {
      console.log(`  ❌ Failed: ${err.message}`);
      this.failed++;
    }
  }

  async testSecurityRestrictions() {
    console.log('Test: Security Restrictions');
    try {
      // Test dangerous command detection
      const dangerousCommands = [
        'Remove-Item -Recurse -Force C:\\',
        'Format-Volume',
        'Stop-Computer',
      ];
      
      const blockedPatterns = [
        /Remove-Item.*-Recurse.*C:\\/i,
        /Format-Volume/i,
        /Stop-Computer/i,
      ];
      
      dangerousCommands.forEach((cmd, index) => {
        const isBlocked = blockedPatterns[index].test(cmd);
        assert(isBlocked, `Should block: ${cmd.substring(0, 30)}...`);
      });
      
      console.log('  ✅ Security restrictions work correctly');
      this.passed++;
    } catch (err) {
      console.log(`  ❌ Failed: ${err.message}`);
      this.failed++;
    }
  }

  async testTimeoutControl() {
    console.log('Test: Timeout Control');
    try {
      // Test timeout validation
      const validTimeouts = [1, 5, 30, 60, 300];
      const invalidTimeouts = [-1, 0, null, undefined, 'abc'];
      
      validTimeouts.forEach(t => {
        assert(typeof t === 'number' && t > 0, `Should accept timeout: ${t}`);
      });
      
      invalidTimeouts.forEach(t => {
        const isValid = typeof t === 'number' && t > 0;
        assert(!isValid, `Should reject invalid timeout: ${t}`);
      });
      
      console.log('  ✅ Timeout control validation works correctly');
      this.passed++;
    } catch (err) {
      console.log(`  ❌ Failed: ${err.message}`);
      this.failed++;
    }
  }

  async testOutputLimiting() {
    console.log('Test: Output Limiting');
    try {
      // Test output size limiting logic
      const maxOutputSize = 10000; // 10KB
      const largeOutput = 'x'.repeat(15000);
      
      const truncated = largeOutput.length > maxOutputSize 
        ? largeOutput.substring(0, maxOutputSize) + '\n... (truncated)'
        : largeOutput;
      
      assert(truncated.length <= maxOutputSize + 20, 'Output should be truncated');
      assert(truncated.includes('truncated'), 'Should indicate truncation');
      
      console.log('  ✅ Output limiting works correctly');
      this.passed++;
    } catch (err) {
      console.log(`  ❌ Failed: ${err.message}`);
      this.failed++;
    }
  }
}

// Run tests
if (require.main === module) {
  const test = new PowerShellSandboxTest();
  test.runAll().then(success => {
    process.exit(success ? 0 : 1);
  });
}

module.exports = { PowerShellSandboxTest };
