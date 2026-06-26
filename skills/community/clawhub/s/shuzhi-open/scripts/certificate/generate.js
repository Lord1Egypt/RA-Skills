#!/usr/bin/env node
/**
 * 保管单生成 - 快速执行脚本
 * 使用预定义参数快速生成保管单
 */

const path = require('path');
const crypto = require('crypto');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const chain = require(path.join(libPath, 'modules/chain'));
const certificate = require(path.join(libPath, 'modules/certificate'));

const config = require(configPath);
init(config);

// 默认参数（可修改）
const TEMPLATE_ID = '2036284038445596672';
const applicantName = '张三';
const applicantAccount = 'zhangsan';
const customFieldList = [];

async function main() {
  console.log('📋 保管单生成流程\n');
  console.log('='.repeat(50));
  console.log('模板 ID:', TEMPLATE_ID);
  console.log('申请人:', applicantName);
  console.log('账号:', applicantAccount);
  if (customFieldList.length > 0) {
    console.log('自定义字段:', JSON.stringify(customFieldList));
  }
  console.log('='.repeat(50));
  
  try {
    // 组装上链数据
    const chainData = {
      applicantName,
      applicantAccount,
      ...Object.fromEntries(customFieldList.map(f => [f.name, f.value])),
      timestamp: new Date().toISOString()
    };
    console.log('\n上链数据:', JSON.stringify(chainData));
    
    // 上链
    console.log('\n正在上链...');
    const uploadResult = await chain.upload({
      business: ['EVIDENCE_PRESERVATION'],
      data: JSON.stringify(chainData),
      requestId: crypto.randomBytes(16).toString('hex'),
      source: ['BQ_INTERNATIONAL']
    });
    console.log('✅ 交易索引:', uploadResult.index);
    
    // 查询结果
    console.log('\n查询上链结果...');
    const queryResult = await chain.queryResult([uploadResult.index]);
    const firstChain = queryResult[0]?.chain_results?.[0] || {};
    console.log('✅ 区块链哈希:', firstChain.hash || 'N/A');
    console.log('   区块高度:', firstChain.height || 'N/A');
    
    // 生成保管单
    console.log('\n生成保管单...');
    const custodyParams = {
      templateId: TEMPLATE_ID,
      requestId: crypto.randomBytes(16).toString('hex'),
      defaultFields: {
        applicantName,
        applicantAccount,
        evidenceHash: crypto.createHash('sha256').update(JSON.stringify(chainData)).digest('hex'),
        blockchainHash: firstChain.hash || '',
        blockchainHeight: String(firstChain.height || 0),
        attestTime: new Date().toISOString().substring(0, 19).replace('T', ' ')
      },
      customFieldList
    };
    
    const certNo = await certificate.create(custodyParams);
    console.log('✅ 存证编号:', certNo);
    
    // 获取下载链接
    console.log('\n获取下载链接...');
    let downloadUrl = null;
    for (let i = 0; i < 12; i++) {
      try {
        const dl = await certificate.download(certNo);
        if (dl.url) { downloadUrl = dl.url; break; }
      } catch (e) {}
      await new Promise(r => setTimeout(r, 5000));
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('🎉 保管单生成完成！');
    console.log('='.repeat(50));
    console.log('\n存证编号:', certNo);
    console.log('下载链接:', downloadUrl);
    
  } catch (error) {
    console.log('\n❌ 生成失败:', error.message);
  }
}

main();