#!/usr/bin/env node

/**
 * P0-2: 完整的端到端测试（5 Agent 协作 + 版本管理 + 增量更新）
 * 
 * 测试场景：
 * 1. 创建 v1.0（5 Agent 协作生成项目）
 * 2. 增量更新 v2.0（基于 v1.0 修改）
 * 3. 验证版本管理和文件差异
 */

const { run } = require('./index.js');
const path = require('path');
const fs = require('fs').promises;

const OUTPUT_DIR = path.join(__dirname, 'test-output-p0');

/**
 * 模拟 LLM 回调（用于测试，不真实调用 API）
 */
async function mockLLMCallback(prompt, model, thinking) {
  console.log(`  🤖 [Mock LLM] ${model} (${thinking})`);
  
  // 根据 prompt 内容返回不同的模拟响应
  if (prompt.includes('需求分析师') || prompt.includes('功能清单')) {
    // Phase 1: 需求分析
    return `# 个税计算器 - 需求文档

## 1. 项目概述
- 项目背景：帮助用户快速计算个人所得税
- 目标用户：上班族、财务人员
- 核心价值：简化个税计算流程

## 2. 功能清单
| 功能名称 | 优先级 | 描述 |
|---------|--------|------|
| 收入输入 | P0 | 输入月收入金额 |
| 五险一金输入 | P0 | 输入五险一金金额 |
| 个税计算 | P0 | 根据公式计算个税 |
| 结果显示 | P0 | 显示计算明细 |

## 3. 用户故事（GWT 格式）
1. Given 用户有月收入，When 输入收入和五险一金，Then 显示应纳个税
2. Given 用户收入低于起征点，When 点击计算，Then 显示无需纳税

## 4. 验收标准
- [ ] 输入框支持小数
- [ ] 计算结果保留 2 位小数
- [ ] 错误输入有提示`;
  }
  
  if (prompt.includes('架构师') || prompt.includes('技术选型')) {
    // Phase 2: 架构设计
    return `# 个税计算器 - 架构设计

## 1. 技术选型
| 层次 | 技术 | 选择理由 |
|------|------|---------|
| 前端 | HTML+CSS+JS | 简单直接，无需构建 |

## 2. 系统架构
\`\`\`
┌─────────────┐
│   HTML UI   │
├─────────────┤
│ JavaScript  │
│  - Input    │
│  - Calculate│
│  - Display  │
└─────────────┘
\`\`\`

## 3. 模块设计
- **InputModule**: 处理用户输入
- **CalcModule**: 个税计算逻辑
- **DisplayModule**: 结果显示

## 4. 数据模型
\`\`\`javascript
interface TaxResult {
  taxableIncome: number;
  taxRate: number;
  tax: number;
}
\`\`\``;
  }
  
  if (prompt.includes('开发工程师') || prompt.includes('代码实现')) {
    // Phase 3: 代码实现
    return `我将创建以下文件：

\`\`\`index.html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>个税计算器</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; }
    .input-group { margin: 20px 0; }
    input { width: 100%; padding: 10px; }
    button { background: #667eea; color: white; padding: 12px 24px; border: none; }
    .result { margin-top: 20px; padding: 15px; background: #f0f0f0; }
  </style>
</head>
<body>
  <h1>💰 个税计算器</h1>
  <div class="input-group">
    <label>月收入（元）</label>
    <input type="number" id="income" placeholder="请输入月收入">
  </div>
  <div class="input-group">
    <label>五险一金（元）</label>
    <input type="number" id="insurance" placeholder="请输入五险一金">
  </div>
  <button onclick="calculate()">计算个税</button>
  <div class="result" id="result"></div>
  
  <script>
    function calculate() {
      const income = parseFloat(document.getElementById('income').value) || 0;
      const insurance = parseFloat(document.getElementById('insurance').value) || 0;
      const taxable = income - insurance - 5000;
      
      if (taxable <= 0) {
        document.getElementById('result').innerHTML = '无需纳税';
        return;
      }
      
      let rate, deduction;
      if (taxable < 3000) { rate = 0.03; deduction = 0; }
      else if (taxable < 12000) { rate = 0.10; deduction = 210; }
      else { rate = 0.20; deduction = 1410; }
      
      const tax = taxable * rate - deduction;
      document.getElementById('result').innerHTML = 
        '<h3>计算结果</h3>' +
        '<p>应纳税所得额：' + taxable.toFixed(2) + '元</p>' +
        '<p>税率：' + (rate * 100) + '%</p>' +
        '<p>速算扣除数：' + deduction + '元</p>' +
        '<p><strong>应纳个税：' + tax.toFixed(2) + '元</strong></p>';
    }
  </script>
</body>
</html>
\`\`\``;
  }
  
  if (prompt.includes('测试工程师') || prompt.includes('测试用例')) {
    // Phase 4: 测试编写
    return `# 个税计算器 - 测试用例

## 功能测试
1. **正常计算**
   - 输入：月收入 10000，五险一金 2000
   - 预期：应纳税所得额 3000，个税 90 元
   
2. **低于起征点**
   - 输入：月收入 4000，五险一金 1000
   - 预期：无需纳税

3. **边界值测试**
   - 输入：月收入 5000，五险一金 0
   - 预期：无需纳税（刚好起征点）

## 边界测试
- 输入负数：显示错误提示
- 输入空值：显示错误提示
- 输入超大数值：正常计算`;
  }
  
  // 默认响应
  return '完成';
}

/**
 * 运行端到端测试
 */
async function runE2ETest() {
  console.log('🧪 '.repeat(30));
  console.log('P0-2: 完整端到端测试');
  console.log('5 Agent 协作 + 版本管理 + 增量更新');
  console.log('🧪 '.repeat(30));
  console.log();
  
  const results = {
    v1Success: false,
    v2Success: false,
    versionCheck: false,
    fileCheck: false
  };
  
  try {
    // ========== v1.0: 初始版本 ==========
    console.log('【v1.0】创建初始版本（5 Agent 协作）\n');
    console.log('使用模拟 LLM 回调（不真实调用 API）\n');
    
    const v1 = await run('做个个税计算器', {
      outputDir: OUTPUT_DIR,
      llmCallback: mockLLMCallback
    });
    
    console.log('\n✅ v1.0 完成\n');
    console.log(`  项目 ID: ${v1.projectId}`);
    console.log(`  版本：${v1.version}`);
    console.log(`  文件数：${v1.files?.length || 0}`);
    console.log(`  耗时：${Math.round(v1.duration / 1000)}秒`);
    console.log(`  LLM 模式：${v1.llmMode ? 'OpenClaw 集成' : '模拟'}`);
    
    results.v1Success = true;
    
    // ========== v2.0: 增量更新 ==========
    console.log('\n\n【v2.0】增量更新（使用模拟 LLM）\n');
    
    const v2 = await run('做个更专业的个税计算器，界面更美观', {
      projectId: v1.projectId,
      parentVersion: v1.version,
      outputDir: OUTPUT_DIR,
      llmCallback: mockLLMCallback,
      conservatism: 'balanced'
    });
    
    console.log('\n✅ v2.0 完成\n');
    console.log(`  项目 ID: ${v2.projectId}`);
    console.log(`  版本：${v2.version}`);
    console.log(`  增量更新：${v2.isIncremental}`);
    console.log(`  文件数：${v2.files?.length || 0}`);
    console.log(`  耗时：${Math.round(v2.duration / 1000)}秒`);
    
    results.v2Success = true;
    
    // ========== 验证版本管理 ==========
    console.log('\n\n【验证】版本管理\n');
    
    const { VersionManager } = require('./executors/version-manager');
    const vm = new VersionManager(OUTPUT_DIR);
    const project = await vm.loadOrCreateProject(v1.projectId, '');
    const versions = project.getVersions();
    
    console.log(`  总版本数：${versions.length}`);
    versions.forEach(v => {
      console.log(`    - ${v.version}: ${v.requirement} (${v.status})`);
    });
    
    if (versions.length === 2 && versions[1].status === 'current') {
      console.log('  ✅ 版本管理验证通过');
      results.versionCheck = true;
    } else {
      console.log('  ❌ 版本管理验证失败');
    }
    
    // ========== 验证文件生成 ==========
    console.log('\n【验证】文件生成\n');
    
    try {
      const v1Dir = path.join(OUTPUT_DIR, v1.projectId, 'v1.0');
      const v2Dir = path.join(OUTPUT_DIR, v1.projectId, 'v2.0');
      
      const v1Files = await fs.readdir(v1Dir, { recursive: true });
      const v2Files = await fs.readdir(v2Dir, { recursive: true });
      
      console.log(`  v1.0 文件数：${v1Files.length}`);
      console.log(`  v2.0 文件数：${v2Files.length}`);
      console.log(`  输出目录：${OUTPUT_DIR}`);
      
      if (v1Files.length > 0 && v2Files.length > 0) {
        console.log('  ✅ 文件生成验证通过');
        results.fileCheck = true;
      } else {
        console.log('  ❌ 文件生成验证失败');
      }
    } catch (error) {
      console.log('  ❌ 文件读取失败:', error.message);
    }
    
    // ========== 汇总报告 ==========
    console.log('\n' + '='.repeat(60));
    console.log('📊 测试汇总报告');
    console.log('='.repeat(60));
    
    const tests = [
      { name: 'v1.0 创建（5 Agent 协作）', result: results.v1Success },
      { name: 'v2.0 增量更新', result: results.v2Success },
      { name: '版本管理验证', result: results.versionCheck },
      { name: '文件生成验证', result: results.fileCheck }
    ];
    
    const passed = tests.filter(t => t.result).length;
    const total = tests.length;
    
    console.log(`\n总测试数：${total}`);
    console.log(`通过：${passed}`);
    console.log(`失败：${total - passed}`);
    console.log(`通过率：${Math.round(passed / total * 100)}%\n`);
    
    tests.forEach(t => {
      console.log(`${t.result ? '✅' : '❌'} ${t.name}`);
    });
    
    console.log('\n' + '='.repeat(60));
    if (passed === total) {
      console.log('🎉 所有测试通过！P0 任务完成！\n');
    } else {
      console.log('⚠️ 部分测试失败\n');
    }
    
    return { success: passed === total, results };
    
  } catch (error) {
    console.error('\n❌ 测试异常:', error.message);
    console.error(error.stack);
    return { success: false, error: error.message };
  }
}

// 运行测试
if (require.main === module) {
  runE2ETest().catch(console.error);
}

module.exports = { runE2ETest, mockLLMCallback };
