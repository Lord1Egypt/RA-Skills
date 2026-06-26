#!/usr/bin/env node
/**
 * 电子签章 - 完整流程脚本
 * 
 * 用法1: 使用配置文件
 * node scripts/sign/workflow.js --file signers.json
 * 
 * 用法2: 使用命令行参数（推荐）
 * node scripts/sign/workflow.js --contract "合同文件路径" --signers 'JSON字符串'
 * 
 * 用法3: 使用交互式输入
 * node scripts/sign/workflow.js --interactive
 */

const path = require('path');
const fs = require('fs');
const readline = require('readline');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const sign = require(path.join(libPath, 'modules/sign'));

const config = require(configPath);
init(config);

// 创建 readline 接口
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

/**
 * 信息校验
 */
async function validateSigners(signers) {
  const errors = [];
  const existingEntities = [];

  for (const s of signers) {
    if (s.type === 'enterprise') {
      const listResult = await sign.enterprise.list(s.enterpriseName, s.creditCode);
      const enterpriseList = listResult && listResult.data ? listResult.data : (listResult || []);
      
      if (enterpriseList.length > 0) {
        const existing = enterpriseList[0];
        if (existing.principalName !== s.enterpriseName) {
          errors.push({
            signerNo: s.signerNo,
            type: 'enterprise',
            field: 'enterpriseName',
            provided: s.enterpriseName,
            systemValue: existing.principalName,
            creditCode: s.creditCode
          });
        } else {
          existingEntities.push({
            signerNo: s.signerNo,
            type: 'enterprise',
            userId: existing.userId,
            exists: true
          });
        }
      } else {
        existingEntities.push({
          signerNo: s.signerNo,
          type: 'enterprise',
          exists: false
        });
      }
    } else if (s.type === 'person') {
      const listResult = await sign.person.list(s.name, s.idCard);
      const personList = listResult && listResult.data ? listResult.data : (listResult || []);
      
      if (personList.length > 0) {
        const existing = personList[0];
        if (existing.name !== s.name) {
          errors.push({
            signerNo: s.signerNo,
            type: 'person',
            field: 'name',
            provided: s.name,
            systemValue: existing.name,
            idCard: s.idCard
          });
        } else {
          existingEntities.push({
            signerNo: s.signerNo,
            type: 'person',
            userId: existing.userId,
            exists: true
          });
        }
      } else {
        existingEntities.push({
          signerNo: s.signerNo,
          type: 'person',
          exists: false
        });
      }
    }
  }

  return { errors, existingEntities };
}

/**
 * 创建主体
 */
async function createEntity(signer, existingEntity) {
  if (existingEntity.exists) {
    return { userId: existingEntity.userId, existed: true };
  }

  if (signer.type === 'enterprise') {
    try {
      const result = await sign.enterprise.create(signer.enterpriseName, signer.creditCode);
      return { userId: result.userId, existed: false };
    } catch (error) {
      if (error.message && error.message.includes('重复')) {
        console.log('    ⚠️ 企业已存在，使用现有记录...');
        const listResult = await sign.enterprise.list(signer.enterpriseName, signer.creditCode);
        const enterpriseList = listResult && listResult.data ? listResult.data : (listResult || []);
        if (enterpriseList.length > 0) {
          return { userId: enterpriseList[0].userId, existed: true };
        }
      }
      throw error;
    }
  } else {
    try {
      const result = await sign.person.create(signer.name, signer.idCard);
      return { userId: result.userId, existed: false };
    } catch (error) {
      if (error.message && error.message.includes('重复')) {
        console.log('    ⚠️ 个人已存在，使用现有记录...');
        const listResult = await sign.person.list(signer.name, signer.idCard);
        const personList = listResult && listResult.data ? listResult.data : (listResult || []);
        if (personList.length > 0) {
          return { userId: personList[0].userId, existed: true };
        }
      }
      throw error;
    }
  }
}

/**
 * 创建印章
 */
async function createSeal(signer, userId) {
  if (signer.type === 'enterprise') {
    const sealList = await sign.enterpriseSeal.list({ principalName: signer.enterpriseName });
    const seals = sealList && sealList.data ? sealList.data : (sealList || []);
    if (seals.length > 0) {
      return { sealId: seals[0].sealId, existed: true };
    }

    const sealResult = await sign.enterpriseSeal.create({
      userId: userId,
      sealName: signer.enterpriseName + '印章',
      enterpriseSealType: 1,
      sealMode: 2
    });
    
    return { sealId: sealResult.sealId, existed: false };
  } else {
    const sealList = await sign.personSeal.list(signer.name, signer.idCard);
    const seals = sealList && sealList.data ? sealList.data : (sealList || []);
    if (seals.length > 0) {
      return { sealId: seals[0].sealId, existed: true };
    }

    const sealResult = await sign.personSeal.create({
      userId: userId,
      sealName: signer.name + '签名',
      sealMode: 2
    });
    
    return { sealId: sealResult.sealId, existed: false };
  }
}

/**
 * 完整流程
 */
async function workflow(signersData) {
  const { signers, contractFile } = signersData;

  if (signers.length > 6) {
    throw new Error('签署方数量超过限制，最多支持6个签署方');
  }

  console.log('============================================================');
  console.log('电子签章流程');
  console.log('============================================================');
  console.log(`\n签署方数量: ${signers.length}`);

  // Step 0: 信息校验
  console.log('\n【Step 0】信息校验...');
  const { errors, existingEntities } = await validateSigners(signers);
  
  if (errors.length > 0) {
    let message = '❌ 信息校验失败\n\n';
    for (const err of errors) {
      if (err.type === 'enterprise') {
        message += `【${err.signerNo}】企业信息不一致：\n`;
        message += `- 提供的企业名称：${err.provided}\n`;
        message += `- 系统中该信用代码对应的企业名称：${err.systemValue}\n`;
        message += `- 统一社会信用代码：${err.creditCode}\n\n`;
      } else {
        message += `【${err.signerNo}】个人信息不一致：\n`;
        message += `- 提供的姓名：${err.provided}\n`;
        message += `- 系统中该身份证对应的姓名：${err.systemValue}\n`;
        message += `- 身份证号：${err.idCard}\n\n`;
      }
    }
    message += '请确认信息是否正确，或联系管理员处理。';
    console.log(message);
    return { success: false, errors };
  }
  console.log('✅ 信息校验通过');

  const preparedSigners = [];

  // Step 1: 创建主体
  console.log('\n【Step 1】创建主体...');
  for (let i = 0; i < signers.length; i++) {
    const s = signers[i];
    const existing = existingEntities[i];
    
    console.log(`  ${s.signerNo}: ${s.type === 'enterprise' ? s.enterpriseName : s.name}`);
    
    const entityResult = await createEntity(s, existing);
    console.log(`    userId: ${entityResult.userId} ${entityResult.existed ? '(已存在)' : '(新建)'}`);
    
    preparedSigners.push({
      ...s,
      userId: entityResult.userId
    });
  }

  // Step 2: 创建印章
  console.log('\n【Step 2】创建印章...');
  for (const s of preparedSigners) {
    console.log(`  ${s.signerNo}: ${s.type === 'enterprise' ? s.enterpriseName : s.name}`);
    
    const sealResult = await createSeal(s, s.userId);
    s.sealId = sealResult.sealId;
    console.log(`    sealId: ${s.sealId} ${sealResult.existed ? '(已存在)' : '(新建)'}`);
  }

  // Step 3: 上传合同文件
  console.log('\n【Step 3】上传合同文件...');
  const fileBuffer = fs.readFileSync(contractFile);
  const base64 = fileBuffer.toString('base64');
  console.log(`  文件: ${contractFile}`);
  console.log(`  大小: ${(fileBuffer.length / 1024).toFixed(2)} KB`);

  const uploadResult = await sign.file.upload(base64, path.basename(contractFile), '.pdf');
  const fileId = uploadResult.fileId || (uploadResult.data && uploadResult.data.fileId);
  console.log(`  ✅ fileId: ${fileId}`);

  // Step 4: 创建合同模板
  console.log('\n【Step 4】创建合同模板...');
  const templateName = `合同模板_${Date.now()}`;
  const signerNoList = preparedSigners.map(s => s.signerNo);
  
  const templateResult = await sign.template.create({
    templateName: templateName,
    fileList: [{
      fileId: fileId,
      fileName: path.basename(contractFile),
      signerList: signerNoList,
      controlList: [
        { controlName: '签署日期', controlKey: 'sign_date', controlKeyType: 'text', allowEdit: 1, isRequired: 1 }
      ]
    }]
  });

  const templateId = templateResult.templateId || (templateResult.data && templateResult.data.templateId);
  const templatePreviewUrl = templateResult.previewUrl || (templateResult.data && templateResult.data.previewUrl);
  console.log(`  ✅ templateId: ${templateId}`);
  console.log(`  模板预览链接: ${templatePreviewUrl}`);

  return {
    success: true,
    signers: preparedSigners.map(s => ({
      signerNo: s.signerNo,
      type: s.type,
      userId: s.userId,
      sealId: s.sealId,
      name: s.type === 'enterprise' ? s.enterpriseName : s.name
    })),
    template: {
      templateId: templateId,
      templateName: templateName,
      previewUrl: templatePreviewUrl
    },
    fileId: fileId,
    nextStep: '请打开模板预览链接配置签署位置，配置完成后调用创建签署流程接口'
  };
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        params[key] = value;
        i++;
      }
    }
  }

  return params;
}

/**
 * 显示用法
 */
function showUsage() {
  console.log(`
用法:
  1. 使用配置文件:
     node workflow.js --file signers.json

  2. 使用命令行参数:
     node workflow.js --contract "合同文件路径" --signers '[...]'

  3. 交互式输入:
     node workflow.js --interactive

signers JSON 格式:
[
  {
    "signerNo": "甲方",
    "type": "enterprise",
    "enterpriseName": "公司名称",
    "creditCode": "统一社会信用代码",
    "contactName": "联系人姓名",
    "contactIdCard": "联系人身份证",
    "contactMobile": "联系人手机"
  },
  {
    "signerNo": "乙方",
    "type": "person",
    "name": "姓名",
    "idCard": "身份证号",
    "mobile": "手机号"
  }
]
`);
}

/**
 * 交互式输入
 */
async function interactive() {
  console.log('\n============================================================');
  console.log('电子签章 - 交互式工作流');
  console.log('============================================================\n');

  const ask = (question) => new Promise(resolve => rl.question(question, resolve));

  // 收集合同文件路径
  const contractFile = await ask('合同文件路径: ');
  if (!contractFile || !fs.existsSync(contractFile)) {
    console.log('\n❌ 文件不存在或路径无效');
    rl.close();
    return;
  }

  // 收集签署方数量
  const enterpriseCount = parseInt(await ask('企业方数量: ')) || 0;
  const personCount = parseInt(await ask('个人方数量: ')) || 0;

  if (enterpriseCount + personCount === 0) {
    console.log('\n❌ 至少需要一个签署方');
    rl.close();
    return;
  }

  const signers = [];
  let signerIndex = 1;

  // 收集企业方信息
  for (let i = 0; i < enterpriseCount; i++) {
    console.log(`\n【企业方${signerIndex}】`);
    const signerNo = await ask('  签署方标识（如甲方/乙方）: ');
    const enterpriseName = await ask('  企业名称: ');
    const creditCode = await ask('  统一社会信用代码: ');
    const contactName = await ask('  联系人姓名: ');
    const contactIdCard = await ask('  联系人身份证: ');
    const contactMobile = await ask('  联系人手机: ');

    signers.push({
      signerNo,
      type: 'enterprise',
      enterpriseName,
      creditCode,
      contactName,
      contactIdCard,
      contactMobile
    });
    signerIndex++;
  }

  // 收集个人方信息
  for (let i = 0; i < personCount; i++) {
    console.log(`\n【个人方${signerIndex}】`);
    const signerNo = await ask('  签署方标识（如甲方/乙方）: ');
    const name = await ask('  姓名: ');
    const idCard = await ask('  身份证号: ');
    const mobile = await ask('  手机号: ');

    signers.push({
      signerNo,
      type: 'person',
      name,
      idCard,
      mobile
    });
    signerIndex++;
  }

  // 确认信息
  console.log('\n============================================================');
  console.log('确认信息');
  console.log('============================================================');
  console.log(`合同文件: ${contractFile}`);
  console.log(`签署方: ${enterpriseCount}方企业 + ${personCount}方个人\n`);

  for (const s of signers) {
    console.log(`【${s.signerNo}】${s.type === 'enterprise' ? '企业' : '个人'}`);
    if (s.type === 'enterprise') {
      console.log(`  企业名称: ${s.enterpriseName}`);
      console.log(`  统一社会信用代码: ${s.creditCode}`);
      console.log(`  联系人: ${s.contactName}`);
      console.log(`  手机: ${s.contactMobile}`);
    } else {
      console.log(`  姓名: ${s.name}`);
      console.log(`  身份证: ${s.idCard}`);
      console.log(`  手机: ${s.mobile}`);
    }
    console.log('');
  }

  const confirmed = await ask('确认创建签署流程？(yes/no): ');
  if (confirmed.toLowerCase() !== 'yes' && confirmed.toLowerCase() !== 'y') {
    console.log('\n❌ 已取消');
    rl.close();
    return;
  }

  rl.close();

  // 执行流程
  try {
    const result = await workflow({ signers, contractFile });
    console.log('\n============================================================');
    console.log('【结果】');
    console.log('============================================================');
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('\n❌ 执行失败:', error.message);
    process.exit(1);
  }
}

/**
 * 主函数
 */
async function main() {
  const params = parseArgs();

  // 显示用法
  if (params.help || params.h) {
    showUsage();
    process.exit(0);
  }

  // 交互式模式
  if (params.interactive || params.i) {
    await interactive();
    return;
  }

  // 使用命令行参数
  if (params.contract && params.signers) {
    try {
      const signers = JSON.parse(params.signers);
      const result = await workflow({ signers, contractFile: params.contract });
      console.log('\n============================================================');
      console.log('【结果】');
      console.log('============================================================');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('\n❌ 执行失败:', error.message);
      process.exit(1);
    }
    return;
  }

  // 使用配置文件
  if (params.file) {
    if (!fs.existsSync(params.file)) {
      console.error(`❌ 文件不存在: ${params.file}`);
      process.exit(1);
    }
    const signersData = JSON.parse(fs.readFileSync(params.file, 'utf-8'));
    try {
      const result = await workflow(signersData);
      console.log('\n============================================================');
      console.log('【结果】');
      console.log('============================================================');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('\n❌ 执行失败:', error.message);
      process.exit(1);
    }
    return;
  }

  // 显示用法
  showUsage();
  process.exit(1);
}

main();