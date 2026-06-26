/**
 * 基础功能测试
 */

import { loadConfig, showConfig } from './utils/config-loader.js';
import { loadProfile, getProfileStats, addEvidence } from './utils/profile-manager.js';
import fs from 'node:fs';
import path from 'node:path';

console.log('=== User Context Scanner 基础测试 ===\n');

// 测试1: 配置加载
console.log('1. 测试配置加载...');
try {
  const config = loadConfig();
  console.log('✅ 配置加载成功');
  console.log(`   扫描间隔: ${config.scanIntervalHours}小时`);
  console.log(`   最小置信度: ${config.minConfidenceForUse}`);
  console.log(`   生成Quiz: ${config.generateQuizzes ? '是' : '否'}`);
} catch (error) {
  console.log('❌ 配置加载失败:', error.message);
}

// 测试2: 用户画像加载
console.log('\n2. 测试用户画像加载...');
try {
  const profile = loadProfile();
  console.log('✅ 用户画像加载成功');
  console.log(`   版本: ${profile.version}`);
  console.log(`   创建时间: ${profile.created_at}`);
  console.log(`   最后更新: ${profile.updated_at}`);
  
  // 统计字段数量
  const categories = ['demographics', 'profession', 'values', 'habits', 'preferences'];
  let totalFields = 0;
  
  for (const category of categories) {
    const fields = profile.profile[category];
    const count = fields ? Object.keys(fields).length : 0;
    totalFields += count;
    if (count > 0) {
      console.log(`   ${category}: ${count}个字段`);
    }
  }
  
  console.log(`   总计: ${totalFields}个字段`);
} catch (error) {
  console.log('❌ 用户画像加载失败:', error.message);
}

// 测试3: 画像统计
console.log('\n3. 测试画像统计...');
try {
  const stats = getProfileStats();
  console.log('✅ 画像统计获取成功');
  console.log(`   总体置信度: ${stats.confidence.confidence.toFixed(2)}`);
  console.log(`   字段完整性: ${(stats.confidence.completeness * 100).toFixed(0)}%`);
  console.log(`   证据总数: ${stats.evidence.total}`);
  console.log(`   矛盾数量: ${stats.contradictions.total}`);
} catch (error) {
  console.log('❌ 画像统计失败:', error.message);
}

// 测试4: 证据添加
console.log('\n4. 测试证据添加...');
try {
  const testEvidence = {
    source: 'test',
    category: 'preferences',
    field: 'communication_style',
    value: 'detailed_rational',
    excerpt: '测试证据：喜欢详细理性的沟通',
    timestamp: new Date().toISOString(),
    confidence: 0.8
  };
  
  const evidenceId = addEvidence(testEvidence);
  if (evidenceId) {
    console.log('✅ 证据添加成功:', evidenceId);
  } else {
    console.log('❌ 证据添加失败');
  }
} catch (error) {
  console.log('❌ 证据添加测试失败:', error.message);
}

// 测试5: 配置文件存在性
console.log('\n5. 测试配置文件存在性...');
try {
  const workspace = process.env.HOME ? path.join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
  const configPath = path.join(workspace, '.soul', 'scanner-config.json');
  const profilePath = path.join(workspace, '.soul', 'user-profile.json');
  const evidencePath = path.join(workspace, '.soul', 'user-evidence.jsonl');
  
  console.log(`   配置文件: ${fs.existsSync(configPath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
  console.log(`   画像文件: ${fs.existsSync(profilePath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
  console.log(`   证据文件: ${fs.existsSync(evidencePath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
} catch (error) {
  console.log('❌ 文件检查失败:', error.message);
}

// 测试6: 目录结构
console.log('\n6. 测试目录结构...');
try {
  const scriptFiles = [
    'scanner.js',
    'test-basic.js',
    'utils/config-loader.js',
    'utils/profile-manager.js',
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

console.log('\n=== 测试完成 ===');
console.log('\n下一步建议:');
console.log('1. 运行 npm install 安装依赖');
console.log('2. 运行 npm test 进行完整测试');
console.log('3. 运行 node scripts/scanner.js --scan-memory 测试记忆扫描');
console.log('4. 运行 node scripts/scanner.js --analyze-profile 测试画像分析');
console.log('5. 运行 node scripts/scanner.js --check-contradictions 测试矛盾检测');