#!/usr/bin/env node
/**
 * UTF-8编码工具 - 集成测试
 * 使用真实API测试Discord和GitHub功能
 */

const { UTF8Encoder } = require('./utf8-encoder');
const encoder = new UTF8Encoder();

// 配置 - 从环境变量获取
const DISCORD_WEBHOOK = process.env.DISCORD_WEBHOOK_URL || 'https://discord.com/api/webhooks/1482573744688857109/tD4x8oDKD539koQEeBauFe12N-K2fI1Iydh2Sjvyl23_3JYO08qgXbpBcRFRemKsPUq6';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || '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';

console.log('🚀 UTF-8编码工具 - 集成测试');
console.log('='.repeat(60));
console.log(`时间: ${new Date().toISOString()}`);
console.log(`Discord Webhook: ${DISCORD_WEBHOOK ? '已设置' : '未设置'}`);
console.log(`GitHub Token: ${GITHUB_TOKEN ? '已设置' : '未设置'}`);
console.log('');

async function runIntegrationTest() {
  const testResults = [];
  
  // 测试1: 基本功能验证
  console.log('📝 测试1: 基本功能验证');
  const testText = '集成测试：中文Chinese, Emoji🎯, 特殊符号!@#$ ' + new Date().toISOString();
  
  const validation = encoder.validateNoGarbledChars(testText);
  console.log(`  ✅ 乱码检测: ${validation.valid ? '通过' : '失败'}`);
  console.log(`  ✅ 字符数: ${validation.totalChars}, 中文: ${validation.chineseChars}`);
  
  testResults.push({
    name: '基本功能验证',
    success: validation.valid,
    details: validation
  });
  
  // 测试2: Discord Webhook发送
  console.log('\n📨 测试2: Discord Webhook发送');
  try {
    const discordResult = await encoder.sendToDiscord(
      DISCORD_WEBHOOK,
      `Discord集成测试：\n${testText}\n\n测试时间: ${new Date().toISOString()}`,
      {
        username: 'UTF8-Encoder-Test',
        avatar_url: ''
      }
    );
    
    console.log(`  ✅ Discord发送: ${discordResult.success ? '成功' : '失败'}`);
    console.log(`     状态码: ${discordResult.statusCode}`);
    console.log(`     消息长度: ${discordResult.messageLength} 字符`);
    
    testResults.push({
      name: 'Discord Webhook发送',
      success: discordResult.success,
      details: discordResult
    });
    
    // 等待一会儿，避免速率限制
    await new Promise(resolve => setTimeout(resolve, 1000));
    
  } catch (error) {
    console.log(`  ❌ Discord发送失败: ${error.message}`);
    testResults.push({
      name: 'Discord Webhook发送',
      success: false,
      error: error.message
    });
  }
  
  // 测试3: GitHub Gist创建（私有）
  console.log('\n🐙 测试3: GitHub Gist创建');
  try {
    const gistContent = `# UTF-8编码集成测试

测试时间: ${new Date().toISOString()}

## 测试内容
- 中文测试：这是一个集成测试，验证UTF-8编码是否正确
- 英文测试：English text for testing
- Emoji测试：🎯 ✅ 🔤 
- 特殊符号：!@#$%^&*()

## 编码验证
- 中文字符数: ${validation.chineseChars}
- 总字符数: ${validation.totalChars}
- 乱码检测: ${validation.valid ? '✅ 通过' : '❌ 失败'}

## 测试目的
验证UTF-8编码工具在真实GitHub API环境下的表现。`;
    
    const gistResult = await encoder.createGitHubGist(
      GITHUB_TOKEN,
      gistContent,
      'utf8-integration-test.md',
      'UTF-8编码集成测试 - ' + new Date().toISOString(),
      false // 私有Gist
    );
    
    console.log(`  ✅ GitHub Gist创建: ${gistResult.success ? '成功' : '失败'}`);
    console.log(`     状态码: ${gistResult.statusCode}`);
    console.log(`     内容长度: ${gistResult.contentLength} 字符`);
    
    if (gistResult.gistUrl) {
      console.log(`     Gist URL: ${gistResult.gistUrl}`);
    }
    
    testResults.push({
      name: 'GitHub Gist创建',
      success: gistResult.success,
      details: gistResult
    });
    
  } catch (error) {
    console.log(`  ❌ GitHub Gist创建失败: ${error.message}`);
    testResults.push({
      name: 'GitHub Gist创建',
      success: false,
      error: error.message
    });
  }
  
  // 生成测试报告
  console.log('\n' + '='.repeat(60));
  console.log('📊 集成测试报告');
  
  const totalTests = testResults.length;
  const passedTests = testResults.filter(t => t.success).length;
  const failedTests = totalTests - passedTests;
  
  console.log(`测试总数: ${totalTests}`);
  console.log(`通过数量: ${passedTests}`);
  console.log(`失败数量: ${failedTests}`);
  console.log(`通过率: ${((passedTests / totalTests) * 100).toFixed(1)}%`);
  
  if (failedTests > 0) {
    console.log('\n❌ 失败的测试:');
    testResults.filter(t => !t.success).forEach((test, index) => {
      console.log(`  ${index + 1}. ${test.name}`);
      if (test.error) console.log(`     错误: ${test.error}`);
      if (test.details && test.details.statusCode) console.log(`     状态码: ${test.details.statusCode}`);
    });
    
    console.log('\n💡 故障排除建议:');
    console.log('  1. 检查API Token/Webhook URL是否正确');
    console.log('  2. 检查网络连接');
    console.log('  3. 检查Token权限（GitHub Token需要gist权限）');
    console.log('  4. 检查Discord Webhook是否有效');
    
    return false;
  } else {
    console.log('\n🎉 所有集成测试通过！');
    console.log('UTF-8编码工具在真实API环境中工作正常。');
    
    console.log('\n💡 下一步建议:');
    console.log('  1. 创建GitHub仓库发布技能');
    console.log('  2. 编写详细使用文档');
    console.log('  3. 添加更多平台支持（Reddit、Telegram等）');
    
    return true;
  }
}

// 执行测试
if (require.main === module) {
  console.log('注意: 正在使用真实API进行测试，请确保Token和Webhook有效。');
  console.log('5秒后开始测试...');
  
  setTimeout(async () => {
    try {
      const success = await runIntegrationTest();
      process.exit(success ? 0 : 1);
    } catch (error) {
      console.error('❌ 测试执行出错:', error);
      process.exit(1);
    }
  }, 5000);
}

module.exports = { runIntegrationTest };