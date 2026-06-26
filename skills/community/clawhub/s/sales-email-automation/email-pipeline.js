#!/usr/bin/env node

/**
 * 邮件智能回复 Pipeline
 * 整合：intent 识别 → 知识库检索 → 回复生成 → Discord 审阅
 */

const { classifyIntent, getIntentConfig } = require('./intent-recognition');
const { retrieveKnowledge } = require('./kb-retrieval');
const { generateReply } = require('./reply-generator');
const { sendForReview } = require('./discord-review');

/**
 * 处理单封邮件的完整流程
 */
async function processEmail(emailData) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`🚀 邮件智能回复 Pipeline 启动`);
  console.log(`   主题：${emailData.subject}`);
  console.log(`   发件人：${emailData.from}`);
  console.log(`${'='.repeat(60)}\n`);
  
  const result = {
    email: {
      subject: emailData.subject,
      from: emailData.from,
      date: emailData.date
    },
    steps: {},
    finalDraft: null,
    reviewStatus: null
  };
  
  try {
    // Step 1: Intent 识别
    console.log(`\n【Step 1/4】意图识别`);
    const intentResult = await classifyIntent(emailData.subject || '', emailData.body || '');
    result.steps.intent = intentResult;
    
    const intentConfig = getIntentConfig(intentResult.intent);
    
    // 检查是否需要自动草稿
    if (!intentConfig?.auto_draft) {
      console.log(`\n⚠️  此意图 (${intentResult.intent}) 不生成自动草稿`);
      console.log(`   Fallback: ${intentConfig?.fallback_behavior || 'manual_review'}`);
      
      result.finalDraft = null;
      result.reviewStatus = 'skipped';
      return result;
    }
    
    // Step 2: 知识库检索
    console.log(`\n【Step 2/4】知识库检索`);
    const kbResult = await retrieveKnowledge(
      intentResult.intent,
      intentResult.key_entities || [],
      intentResult.language
    );
    result.steps.knowledge = kbResult;
    
    // Step 3: 回复生成
    console.log(`\n【Step 3/4】回复生成`);
    const replyResult = await generateReply(
      {
        subject: emailData.subject,
        from: emailData.from,
        body: emailData.body
      },
      intentResult.intent,
      kbResult,
      intentResult.language
    );
    result.steps.reply = replyResult;
    
    if (!replyResult.success || !replyResult.reply) {
      console.log(`\n⚠️  回复生成失败`);
      result.finalDraft = null;
      result.reviewStatus = 'failed';
      return result;
    }
    
    result.finalDraft = replyResult.reply;
    
    // Step 4: Discord 审阅
    console.log(`\n【Step 4/4】发送 Discord 审阅`);
    const reviewResult = await sendForReview(
      {
        subject: emailData.subject,
        from: emailData.from,
        date: emailData.date
      },
      replyResult,
      intentResult.intent
    );
    result.reviewStatus = reviewResult;
    
    console.log(`\n${'='.repeat(60)}`);
    console.log(`✅ Pipeline 完成`);
    console.log(`   意图：${intentResult.intent} (${(intentResult.confidence * 100).toFixed(1)}%)`);
    console.log(`   知识库结果：${kbResult.found ? '找到' : '未找到'}相关文档`);
    console.log(`   回复字数：${replyResult.wordCount}`);
    console.log(`   审阅状态：${reviewResult.status}`);
    console.log(`${'='.repeat(60)}\n`);
    
    return result;
    
  } catch (err) {
    console.error(`\n❌ Pipeline 执行失败：${err.message}`);
    result.error = err.message;
    result.reviewStatus = 'error';
    return result;
  }
}

/**
 * CLI 入口
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args[0] === 'test') {
    // 测试模式：使用示例邮件
    const testEmail = {
      subject: 'Inquiry about HDMI cables - MOQ and pricing',
      from: 'john@example.com',
      body: `Hi,

We are interested in your HDMI cables for our retail business.

Could you please provide:
1. Your best price for 1000 units of HDMI 2.0 cables (1.5m)
2. MOQ requirements
3. Lead time for this quantity
4. Available certifications (CE, FCC, etc.)

Looking forward to your reply.

Best regards,
John Smith
ABC Electronics`,
      date: new Date()
    };
    
    console.log(`🧪 测试模式：使用示例邮件\n`);
    const result = await processEmail(testEmail);
    
    console.log(`\n📋 测试结果:`);
    console.log(JSON.stringify(result, null, 2));
    
    return;
  }
  
  // 正常模式：从 auto-capture 集成
  console.log(`用法：node email-pipeline.js test`);
  console.log(`此模块由 auto-capture.js 自动调用`);
}

main().catch(console.error);

module.exports = { processEmail };
