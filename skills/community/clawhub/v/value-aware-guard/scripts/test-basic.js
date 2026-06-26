/**
 * 基础功能测试
 */

import { loadConfig, getConfigSummary, getTimeBoundaryStatus } from './utils/config-loader.js';
import fs from 'node:fs';
import path from 'node:path';

console.log('=== Value-Aware Guard 基础测试 ===\n');

// 测试1: 配置加载
console.log('1. 测试配置加载...');
try {
  const config = loadConfig();
  console.log('✅ 配置加载成功');
  console.log(`   漂移阈值: L1=${config.driftThresholdL1}, L2=${config.driftThresholdL2}, L3=${config.driftThresholdL3}, L4=${config.driftThresholdL4}`);
  console.log(`   时间边界: ${config.timeBoundaryStart}:00-${config.timeBoundaryEnd}:00`);
  console.log(`   每日最大干预: ${config.maxDailyInterventions}`);
  
  const summary = getConfigSummary();
  console.log(`   边界配置: ${summary.boundaries.time}`);
  console.log(`   能量阈值: ${summary.boundaries.energy}`);
} catch (error) {
  console.log('❌ 配置加载失败:', error.message);
}

// 测试2: 时间边界状态
console.log('\n2. 测试时间边界状态...');
try {
  const boundaryStatus = getTimeBoundaryStatus();
  console.log(`✅ 时间边界检查完成`);
  console.log(`   当前时间: ${boundaryStatus.currentHour}:00`);
  console.log(`   边界时段: ${boundaryStatus.boundaryStart}:00-${boundaryStatus.boundaryEnd}:00`);
  console.log(`   是否在边界内: ${boundaryStatus.inBoundary ? '是' : '否'}`);
  console.log(`   边界压力: ${boundaryStatus.pressure.toFixed(2)}`);
} catch (error) {
  console.log('❌ 时间边界测试失败:', error.message);
}

// 测试3: 配置文件存在性
console.log('\n3. 测试配置文件存在性...');
try {
  const workspace = process.env.HOME ? path.join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
  const configPath = path.join(workspace, '.soul', 'guard-config.json');
  const statePath = path.join(workspace, '.soul', 'guard-state.json');
  const valuesPath = path.join(workspace, '.soul', 'user-values.json');
  const interventionsPath = path.join(workspace, '.soul', 'interventions.jsonl');
  
  console.log(`   配置文件: ${fs.existsSync(configPath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
  console.log(`   状态文件: ${fs.existsSync(statePath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
  console.log(`   价值文件: ${fs.existsSync(valuesPath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
  console.log(`   干预记录: ${fs.existsSync(interventionsPath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
} catch (error) {
  console.log('❌ 文件检查失败:', error.message);
}

// 测试4: 目录结构
console.log('\n4. 测试目录结构...');
try {
  const scriptFiles = [
    'guard.js',
    'test-basic.js',
    'utils/config-loader.js',
    'utils/signal-manager.js'
  ];
  
  let allExist = true;
  for (const file of scriptFiles) {
    const filePath = path.join(process.cwd(), 'scripts', file);
    const exists = fs.existsSync(filePath);
    console.log(`   ${file}: ${exists ? '✅ 存在' : '❌ 缺失'}`);
    if (!exists) allExist = false;
  }
  
  if (allExist) {
    console.log('✅ 所有脚本文件就绪');
  } else {
    console.log('⚠️  部分脚本文件缺失');
  }
} catch (error) {
  console.log('❌ 目录结构测试失败:', error.message);
}

// 测试5: 配置验证
console.log('\n5. 测试配置验证...');
try {
  const issues = loadConfig().validateConfig ? loadConfig().validateConfig() : [];
  if (issues.length === 0) {
    console.log('✅ 配置验证通过');
  } else {
    console.log('⚠️  配置验证发现问题:');
    for (const issue of issues) {
      console.log(`   - ${issue}`);
    }
  }
} catch (error) {
  console.log('❌ 配置验证失败:', error.message);
}

// 测试6: 信号管理器
console.log('\n6. 测试信号管理器...');
try {
  const signalManagerPath = path.join(process.cwd(), 'scripts', 'utils', 'signal-manager.js');
  if (fs.existsSync(signalManagerPath)) {
    console.log('✅ 信号管理器文件存在');
    
    // 尝试导入（但不执行）
    const fileContent = fs.readFileSync(signalManagerPath, 'utf-8');
    const hasPublishFunction = fileContent.includes('publishSignal');
    const hasGetPendingFunction = fileContent.includes('getPendingSignals');
    
    console.log(`   包含发布函数: ${hasPublishFunction ? '✅' : '❌'}`);
    console.log(`   包含查询函数: ${hasGetPendingFunction ? '✅' : '❌'}`);
  } else {
    console.log('❌ 信号管理器文件缺失');
  }
} catch (error) {
  console.log('❌ 信号管理器测试失败:', error.message);
}

// 测试7: 用户价值文件
console.log('\n7. 测试用户价值文件...');
try {
  const valuesPath = path.join(process.env.HOME ? process.env.HOME : '/tmp', '.openclaw/workspace/.soul/user-values.json');
  
  if (fs.existsSync(valuesPath)) {
    const values = JSON.parse(fs.readFileSync(valuesPath, 'utf-8'));
    console.log('✅ 用户价值文件存在');
    console.log(`   核心价值数量: ${values.core_values?.length || 0}`);
    console.log(`   工作原则数量: ${values.work_principles?.length || 0}`);
    console.log(`   生活优先级数量: ${values.life_priorities?.length || 0}`);
    console.log(`   创建时间: ${values.created_at || '未知'}`);
  } else {
    console.log('ℹ️ 用户价值文件不存在（首次运行时创建）');
    
    // 检查用户画像文件
    const profilePath = path.join(process.env.HOME ? process.env.HOME : '/tmp', '.openclaw/workspace/.soul/user-profile.json');
    if (fs.existsSync(profilePath)) {
      console.log('✅ 用户画像文件存在，将从中提取价值');
    } else {
      console.log('ℹ️ 用户画像文件也不存在，需要用户明确声明价值');
    }
  }
} catch (error) {
  console.log('❌ 用户价值测试失败:', error.message);
}

console.log('\n=== 测试完成 ===');
console.log('\n下一步建议:');
console.log('1. 运行 npm install 安装依赖');
console.log('2. 运行 npm test 进行完整测试');
console.log('3. 运行 node scripts/guard.js --test 测试价值守护');
console.log('4. 运行 node scripts/guard.js --check-boundaries 测试边界检查');
console.log('5. 运行 node scripts/guard.js --assess-drift 测试价值漂移评估');