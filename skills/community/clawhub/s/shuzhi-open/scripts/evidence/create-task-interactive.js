#!/usr/bin/env node
/**
 * 自动化取证 - 交互式脚本
 * 所有不确定的信息都会询问用户
 */

const path = require('path');
const readline = require('readline');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const evidence = require(path.join(libPath, 'modules/evidence'));

const config = require(configPath);
init(config);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

function askConfirm(question) {
  return ask(question + ' (yes/no): ').then(answer => 
    answer.toLowerCase() === 'yes' || answer.toLowerCase() === 'y'
  );
}

const EVIDENCE_TYPES = {
  '1': { name: '拼多多电商取证', desc: '商品详情页、店铺信息等' },
  '3': { name: '淘宝电商取证', desc: '商品详情页、店铺信息等' },
  '4': { name: '抖音电商取证', desc: '商品详情页、店铺信息等' },
  '12': { name: '公众号取证', desc: '公众号文章内容' }
};

async function main() {
  console.log('\n📋 自动化取证向导');
  console.log('='.repeat(50));
  console.log('说明：所有不确定的信息都会询问您确认');
  console.log('='.repeat(50) + '\n');

  try {
    // Step 1: 选择取证类型
    console.log('Step 1: 选择取证类型\n');
    console.log('📋 请选择取证类型：\n');
    console.log('| 序号 | 类型 | 说明 |');
    console.log('|------|------|------|');
    Object.entries(EVIDENCE_TYPES).forEach(([code, info]) => {
      console.log(`| ${code} | ${info.name} | ${info.desc} |`);
    });
    console.log('');
    
    const typeInput = await ask('请输入序号或类型代码：');
    const typeInfo = EVIDENCE_TYPES[typeInput];
    
    if (!typeInfo) {
      console.log('\n❌ 无效的取证类型');
      rl.close();
      return;
    }
    
    console.log(`\n✅ 已选择：${typeInfo.name}\n`);
    
    // Step 2: 输入取证信息
    console.log('Step 2: 请提供以下信息\n');
    console.log('取证类型: [已选择]\n');
    console.log('取证信息:');
    const url = await ask('  取证URL: ');
    const batchId = await ask('  批次ID: ');
    const attId = await ask('  保全号: ');
    const evidenceName = await ask('  取证名称 (可选，直接回车跳过): ');
    
    console.log('\n可选参数:');
    const needLicense = await askConfirm('  是否取证营业执照');
    
    if (!url || !batchId || !attId) {
      console.log('\n❌ 取证URL、批次ID、保全号不能为空');
      rl.close();
      return;
    }
    
    // Step 3: 确认信息
    console.log('\n' + '='.repeat(50));
    console.log('📝 确认信息\n');
    console.log('取证类型:', typeInfo.name);
    console.log('');
    console.log('取证信息:');
    console.log('  取证URL:', url);
    console.log('  批次ID:', batchId);
    console.log('  保全号:', attId);
    if (evidenceName) console.log('  取证名称:', evidenceName);
    console.log('');
    console.log('可选参数:');
    console.log('  是否取证营业执照:', needLicense ? '是' : '否');
    console.log('');
    
    const confirmed = await askConfirm('确认创建取证任务？');
    if (!confirmed) {
      console.log('\n❌ 已取消');
      rl.close();
      return;
    }
    
    // Step 4: 执行
    console.log('\nStep 3: 创建取证任务...\n');
    
    const taskParams = {
      batch_id: batchId,
      tasks: [{
        att_id: attId,
        url: url.trim(),
        evidence_name: evidenceName || `取证-${attId}`,
        type: parseInt(typeInput),
        business_license_status: needLicense
      }]
    };
    
    const result = await evidence.createTask(taskParams);
    
    console.log('✅ 取证任务创建成功！\n');
    console.log('='.repeat(50));
    console.log('🎉 任务信息');
    console.log('='.repeat(50));
    console.log('\n取证信息:');
    console.log('  取证类型:', typeInfo.name);
    console.log('  批次ID:', batchId);
    console.log('  保全号:', attId);
    console.log('\n💡 后续操作:');
    console.log('   查询状态：node scripts/evidence/query.js --batch-id ' + batchId);
    console.log('   下载证据：node scripts/evidence/download.js --att-id ' + attId);
    console.log('='.repeat(50) + '\n');
    
  } catch (error) {
    console.log('\n❌ 错误:', error.message);
  }
  
  rl.close();
}

main();