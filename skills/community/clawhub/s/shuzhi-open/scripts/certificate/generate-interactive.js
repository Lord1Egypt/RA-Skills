#!/usr/bin/env node
/**
 * 保管单生成 - 交互式脚本
 * 所有不确定的信息都会询问用户
 */

const path = require('path');
const crypto = require('crypto');
const readline = require('readline');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const chain = require(path.join(libPath, 'modules/chain'));
const certificate = require(path.join(libPath, 'modules/certificate'));

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

async function main() {
  console.log('\n📋 保管单生成向导');
  console.log('='.repeat(50));
  console.log('说明：所有不确定的信息都会询问您确认');
  console.log('='.repeat(50) + '\n');

  try {
    // Step 1: 查询模板
    console.log('Step 1: 查询可用模板...\n');
    const templates = await certificate.listTemplates();
    
    console.log('📋 可用的保管单模板：\n');
    console.log('| 序号 | 模板ID | 模板名称 |');
    console.log('|------|--------|----------|');
    templates.forEach((t, i) => {
      console.log(`| ${i + 1} | ${t.id} | ${t.tempName} |`);
    });
    console.log('');
    
    const templateInput = await ask('请选择模板（输入序号或模板ID）：');
    
    let selectedTemplate;
    const index = parseInt(templateInput) - 1;
    if (index >= 0 && index < templates.length) {
      selectedTemplate = templates[index];
    } else {
      selectedTemplate = templates.find(t => t.id === templateInput);
    }
    
    if (!selectedTemplate) {
      console.log('\n❌ 无效的选择');
      rl.close();
      return;
    }
    
    console.log(`\n✅ 已选择模板：${selectedTemplate.tempName} (${selectedTemplate.id})\n`);
    
    // Step 2: 询问字段信息
    console.log('Step 2: 请提供以下信息\n');
    console.log('⚠️ 模板字段因客户而异，需要您确认！\n');
    console.log('请登录数秦开放平台查看该模板的字段配置。\n');
    console.log('请按以下格式提供信息：\n');
    console.log('模板ID: [已自动填充]');
    console.log('');
    console.log('默认字段:');
    console.log('  申请人: [填写]');
    console.log('  账号: [填写]');
    console.log('  [其他字段...]');
    console.log('');
    console.log('自定义字段:');
    console.log('  [字段名]: [值]');
    console.log('  [如无则写"无"]');
    console.log('');
    
    const applicantName = await ask('默认字段 - 申请人: ');
    const applicantAccount = await ask('默认字段 - 账号: ');
    
    // 询问自定义字段
    console.log('\n自定义字段（格式：字段名:值，多个用逗号分隔）');
    const customFieldsInput = await ask('自定义字段: ');
    
    const customFields = {};
    if (customFieldsInput.trim() && customFieldsInput.toLowerCase() !== '无') {
      customFieldsInput.split(',').forEach(pair => {
        const [key, value] = pair.split(':').map(s => s.trim());
        if (key && value) customFields[key] = value;
      });
    }
    
    // 组装上链数据（用于确认信息展示）
    const chainData = {
      applicantName,
      applicantAccount,
      ...customFields,
      timestamp: new Date().toISOString()
    };
    
    // Step 3: 确认信息
    console.log('\n' + '='.repeat(50));
    console.log('📝 确认信息\n');
    console.log(`模板ID: ${selectedTemplate.id} (${selectedTemplate.tempName})`);
    console.log('');
    console.log('默认字段:');
    console.log(`  申请人: ${applicantName}`);
    console.log(`  账号: ${applicantAccount}`);
    console.log('');
    if (Object.keys(customFields).length > 0) {
      console.log('自定义字段:');
      Object.entries(customFields).forEach(([k, v]) => console.log(`  ${k}: ${v}`));
      console.log('');
    }
    console.log('上链数据:');
    console.log(`  applicantName: ${applicantName}`);
    console.log(`  applicantAccount: ${applicantAccount}`);
    Object.entries(customFields).forEach(([k, v]) => console.log(`  ${k}: ${v}`));
    console.log('  timestamp: （将在上链时自动生成）');
    console.log('');
    
    const confirmed = await askConfirm('\n确认生成保管单？');
    if (!confirmed) {
      console.log('\n❌ 已取消');
      rl.close();
      return;
    }
    
    // Step 4: 执行
    console.log('\nStep 3: 执行上链和生成保管单...\n');
    
    // 更新上链数据时间戳
    chainData.timestamp = new Date().toISOString();
    
    console.log('上链数据:', JSON.stringify(chainData));
    
    // 上链
    console.log('\n⏳ 正在上链...');
    const uploadResult = await chain.upload({
      business: ['EVIDENCE_PRESERVATION'],
      data: JSON.stringify(chainData),
      requestId: crypto.randomBytes(16).toString('hex'),
      source: ['BQ_INTERNATIONAL']
    });
    console.log('✅ 交易索引:', uploadResult.index);
    
    // 等待上链完成
    console.log('\n⏳ 等待上链确认...');
    const uploadComplete = await chain.waitUntilUploaded(uploadResult.index, {
      interval: 3000,
      timeout: 60000
    });
    const firstChain = uploadComplete.chain_results?.[0] || {};
    console.log('✅ 上链状态: 成功');
    console.log('   链类型:', firstChain.chain || 'N/A');
    console.log('   交易哈希:', firstChain.hash || 'N/A');
    console.log('   区块高度:', firstChain.height || 'N/A');
    
    // 生成保管单
    console.log('\n⏳ 正在生成保管单...');
    
    // 转换为本地时间字符串 (GMT+8)
    const localTime = new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString().substring(0, 19).replace('T', ' ');
    
    const custodyParams = {
      templateId: selectedTemplate.id,
      requestId: crypto.randomBytes(16).toString('hex'),
      defaultFields: {
        applicantName,
        applicantAccount,
        evidenceHash: crypto.createHash('sha256').update(JSON.stringify(chainData)).digest('hex'),
        blockchainHash: firstChain.hash || '',
        blockchainHeight: String(firstChain.height || 0),
        attestTime: localTime
      },
      customFieldList: Object.entries(customFields).map(([name, value]) => ({ name, value }))
    };
    
    const certNo = await certificate.create(custodyParams);
    console.log('✅ 存证编号:', certNo);
    
    // 获取下载链接
    console.log('\n⏳ 正在获取下载链接...');
    let downloadUrl = null;
    for (let i = 0; i < 12; i++) {
      try {
        const dl = await certificate.download(certNo);
        if (dl.url) {
          downloadUrl = dl.url;
          break;
        }
      } catch (e) {}
      await new Promise(r => setTimeout(r, 5000));
    }
    
    // 保存下载链接到文件
    if (downloadUrl) {
      const linkFile = path.join(process.cwd(), 'last-download-link.txt');
      require('fs').writeFileSync(linkFile, downloadUrl);
    }
    
    // 输出结果
    console.log('\n' + '='.repeat(50));
    console.log('🎉 保管单生成完成！');
    console.log('='.repeat(50));
    console.log('\n📄 保管单信息:');
    console.log('   存证编号:', certNo);
    console.log('   模板:', selectedTemplate.tempName);
    console.log('\n👤 申请人信息:');
    console.log('   姓名:', applicantName);
    console.log('   账号:', applicantAccount);
    console.log('\n🔗 区块链信息:');
    console.log('   链类型:', firstChain.chain || 'N/A');
    console.log('   交易索引:', uploadResult.index);
    console.log('   交易哈希:', firstChain.hash || 'N/A');
    console.log('   区块高度:', firstChain.height || 'N/A');
    console.log('\n📥 下载链接:');
    if (downloadUrl) {
      // Markdown 格式链接（适用于更多终端）
      console.log('\n   [点击下载保管单](' + downloadUrl + ')\n');
      console.log('   或复制以下链接：');
      console.log(downloadUrl);
    } else {
      console.log('   生成中，请稍后重试');
    }
    console.log('\n💡 后续操作:');
    console.log('   下载保管单：node scripts/certificate/download.js --cert-no ' + certNo);
    console.log('='.repeat(50) + '\n');
    
  } catch (error) {
    console.log('\n❌ 错误:', error.message);
  }
  
  rl.close();
}

main();