#!/usr/bin/env node

/**
 * 集成测试脚本 (Integration Test Script)
 * 
 * 功能：
 * 1. 从 IMAP 邮箱拉取真实历史邮件（至少 2 封，目标 3 封不同 intent）
 * 2. 跑完整 pipeline：IMAP 拉取 → intent 识别 → KB 检索 → 回复生成 → Discord 审阅推送
 * 3. 支持 --dry-run 模式（不实际推送 Discord，仅打印结果）
 * 4. 保存测试结果到 test-results/integration-test-{timestamp}.json
 * 
 * 用法：
 *   node integration-test.js              # 完整测试（推送 Discord）
 *   node integration-test.js --dry-run    # 干跑模式（不推送）
 *   node integration-test.js --limit 2    # 只测试 2 封邮件
 */

const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

// 模块导入
const { classifyIntent, getIntentConfig } = require('./intent-recognition');
const { retrieveKnowledge } = require('./kb-retrieval');
const { generateReply } = require('./reply-generation');
const { sendForReview, buildEmbed, buildActionComponents } = require('./discord-review');

// 配置
const TEST_RESULTS_DIR = path.join(__dirname, 'test-results');
const DRAFTS_DIR = path.join(__dirname, 'drafts');

// 确保目录存在
if (!fs.existsSync(TEST_RESULTS_DIR)) {
  fs.mkdirSync(TEST_RESULTS_DIR, { recursive: true });
}

// 解析命令行参数
const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const LIMIT = parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1]) || 3;

console.log('🧪 集成测试启动');
console.log(`   模式：${DRY_RUN ? 'DRY-RUN（不推送 Discord）' : 'LIVE（推送 Discord）'}`);
console.log(`   邮件数量上限：${LIMIT}`);
console.log('');

/**
 * 从 IMAP 拉取邮件
 */
async function fetchEmailsFromIMAP(limit = 3) {
  console.log('📬 从 IMAP 拉取邮件...');
  
  const Imap = require('imap');
  const { simpleParser } = require('mailparser');
  
  const imapConfig = {
    user: process.env.IMAP_USER,
    password: process.env.IMAP_PASS,
    host: process.env.IMAP_HOST,
    port: parseInt(process.env.IMAP_PORT),
    tls: process.env.IMAP_TLS === 'true',
    connTimeout: 30000,
    authTimeout: 30000,
  };
  
  return new Promise((resolve, reject) => {
    const imap = new Imap(imapConfig);
    const emails = [];
    
    imap.once('ready', () => {
      imap.openBox('INBOX', false, (err, box) => {
        if (err) {
          imap.end();
          reject(err);
          return;
        }
        
        // 搜索最近的邮件（不限制未读）
        imap.search(['ALL'], (err, results) => {
          if (err) {
            imap.end();
            reject(err);
            return;
          }
          
          if (results.length === 0) {
            imap.end();
            resolve([]);
            return;
          }
          
          // 取最近的 limit 封邮件
          const fetchSeq = results.slice(-limit).reverse();
          const f = imap.fetch(fetchSeq, { bodies: '', markSeen: false });
          
          let completed = 0;
          
          f.on('message', (msg) => {
            let emailData = null;
            
            msg.on('body', (stream) => {
              simpleParser(stream, (err, parsed) => {
                if (!err && parsed) {
                  emailData = {
                    uid: msg.seqno,
                    from: parsed.from?.text || parsed.from?.value?.[0]?.address || 'unknown',
                    to: parsed.to?.text || parsed.to?.value?.map(v => v.address).join(', ') || '',
                    subject: parsed.subject || 'No Subject',
                    body: parsed.text || parsed.html || '',
                    receivedAt: parsed.date?.toISOString() || new Date().toISOString(),
                    attachments: parsed.attachments?.map(a => a.filename) || []
                  };
                }
              });
            });
            
            msg.once('end', () => {
              if (emailData) {
                emails.push(emailData);
                console.log(`   ✅ 邮件 ${emails.length}: ${emailData.subject.slice(0, 50)}...`);
              }
              completed++;
              if (completed >= fetchSeq.length) {
                imap.end();
                resolve(emails);
              }
            });
          });
          
          f.once('error', (err) => {
            imap.end();
            reject(err);
          });
        });
      });
    });
    
    imap.once('error', reject);
    imap.connect();
  });
}

/**
 * 运行单封邮件的完整 pipeline
 */
async function runPipeline(email, index) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`📧 邮件 ${index + 1}: ${email.subject}`);
  console.log(`   From: ${email.from}`);
  console.log(`${'='.repeat(60)}`);
  
  const result = {
    email: {
      subject: email.subject,
      from: email.from,
      receivedAt: email.receivedAt
    },
    pipeline: {},
    draft: null,
    discord_sent: false,
    errors: []
  };
  
  try {
    // Step 1: Intent 识别
    console.log('\n🔍 Step 1: Intent 识别...');
    const intentResult = await classifyIntent(email.subject, email.body);
    result.pipeline.intent = intentResult;
    console.log(`   Intent: ${intentResult.intent}`);
    console.log(`   Confidence: ${intentResult.confidence}`);
    console.log(`   Language: ${intentResult.language}`);
    
    // Step 2: KB 检索
    console.log('\n📚 Step 2: KB 检索...');
    const kbResults = await retrieveKnowledge(
      intentResult.intent,
      intentResult.key_entities || [],
      intentResult.language || 'en'
    );
    result.pipeline.kb = kbResults;
    console.log(`   Found: ${kbResults.found}`);
    console.log(`   Source: ${kbResults.source}`);
    console.log(`   Results: ${kbResults.results?.length || 0} items`);
    
    // Step 3: 回复生成
    console.log('\n✍️  Step 3: 回复生成...');
    const replyResult = await generateReply({
      email: {
        subject: email.subject,
        from: email.from,
        body: email.body,
        receivedAt: email.receivedAt
      },
      intentResult,
      kbResults
    });
    result.pipeline.reply = replyResult;
    
    if (replyResult.needs_manual) {
      console.log(`   ⚠️  需要人工处理：${replyResult.reason}`);
      result.draft = null;
    } else if (replyResult.draft) {
      console.log(`   Draft ID: ${replyResult.draft_id}`);
      console.log(`   Template: ${replyResult.template_used}`);
      console.log(`   Escalate: ${replyResult.escalate || false}`);
      result.draft = replyResult.draft;
      
      // 修正 draft_id 前缀为 3 字母
      const intentPrefix = intentResult.intent.split('-').map(p => p[0].toUpperCase()).join('').slice(0, 3);
      const timestamp = new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14);
      result.draft.draft_id = `DRAFT-${timestamp}-${intentPrefix}`;
    }
    
    // Step 4: Discord 推送（如果不是 dry-run）
    if (result.draft && !DRY_RUN) {
      console.log('\n📤 Step 4: Discord 推送...');
      try {
        const reviewResult = await sendForReview(result.draft);
        result.discord_sent = true;
        result.discord_message_id = reviewResult.message_id;
        console.log(`   ✅ 已推送到 Discord`);
        console.log(`   Message ID: ${reviewResult.message_id}`);
      } catch (err) {
        console.log(`   ❌ Discord 推送失败：${err.message}`);
        result.errors.push(`Discord send failed: ${err.message}`);
      }
    } else if (result.draft && DRY_RUN) {
      console.log('\n📤 Step 4: Discord 推送（DRY-RUN，仅打印）...');
      const embed = buildEmbed(result.draft);
      console.log(`   Embed Title: ${embed.title}`);
      console.log(`   Embed Color: ${embed.color === 0xFF0000 ? 'RED (escalation)' : 'BLUE'}`);
      console.log(`   Buttons: ✅ Send, ✏️ Edit, ❌ Discard`);
    }
    
    console.log(`\n✅ 邮件 ${index + 1} pipeline 完成`);
    
  } catch (err) {
    console.log(`\n❌ 邮件 ${index + 1} pipeline 失败：${err.message}`);
    result.errors.push(err.message);
  }
  
  return result;
}

/**
 * 主函数
 */
async function main() {
  const startTime = Date.now();
  const timestamp = new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14);
  
  // 加载环境变量
  const envPath = path.join(__dirname, '..', '..', '.env');
  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    envContent.split('\n').forEach(line => {
      const [key, value] = line.split('=');
      if (key && value) {
        process.env[key.trim()] = value.trim();
      }
    });
  }
  
  // 拉取邮件
  let emails = [];
  try {
    emails = await fetchEmailsFromIMAP(LIMIT);
  } catch (err) {
    console.log(`⚠️  IMAP 拉取失败：${err.message}`);
    console.log('   使用备用测试邮件...');
    
    // 备用测试邮件（如果 IMAP 失败）
    emails = [
      {
        uid: 'test-1',
        from: 'customer@example.com',
        to: 'sale-9@farreach-electronic.com',
        subject: 'Inquiry: HDMI Cable 2.1 - 4K 120Hz',
        body: 'Hi,\n\nWe are interested in your HDMI 2.1 cables. Can you send us a quote for 500 units?\n\nBest regards,\nJohn',
        receivedAt: new Date().toISOString(),
        attachments: []
      },
      {
        uid: 'test-2',
        from: 'tech@client.com',
        to: 'sale-9@farreach-electronic.com',
        subject: 'Technical Question: DP 1.4 Compatibility',
        body: 'Hello,\n\nDoes your DP 1.4 cable support 8K resolution at 60Hz?\n\nThanks,\nSarah',
        receivedAt: new Date().toISOString(),
        attachments: []
      }
    ];
  }
  
  if (emails.length === 0) {
    console.log('❌ 没有邮件可测试');
    process.exit(1);
  }
  
  console.log(`\n📬 找到 ${emails.length} 封邮件`);
  
  // 运行 pipeline
  const results = [];
  for (let i = 0; i < emails.length; i++) {
    const result = await runPipeline(emails[i], i);
    results.push(result);
  }
  
  // 生成测试报告
  const report = {
    test_id: `integration-test-${timestamp}`,
    timestamp: new Date().toISOString(),
    mode: DRY_RUN ? 'dry-run' : 'live',
    emails_processed: emails.length,
    duration_ms: Date.now() - startTime,
    results,
    summary: {
      successful: results.filter(r => r.errors.length === 0).length,
      failed: results.filter(r => r.errors.length > 0).length,
      discord_sent: results.filter(r => r.discord_sent).length,
      intents: results.map(r => r.pipeline.intent?.intent).filter(Boolean)
    }
  };
  
  // 保存报告
  const reportPath = path.join(TEST_RESULTS_DIR, `integration-test-${timestamp}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), 'utf8');
  console.log(`\n📊 测试报告已保存：${reportPath}`);
  
  // 打印摘要
  console.log('\n' + '='.repeat(60));
  console.log('📊 测试摘要');
  console.log('='.repeat(60));
  console.log(`   总邮件数：${report.emails_processed}`);
  console.log(`   成功：${report.summary.successful}`);
  console.log(`   失败：${report.summary.failed}`);
  console.log(`   Discord 推送：${report.summary.discord_sent}`);
  console.log(`   Intents 分布：${[...new Set(report.summary.intents)].join(', ')}`);
  console.log(`   耗时：${report.duration_ms}ms`);
  console.log('='.repeat(60));
  
  // 返回结果（用于 task-001 更新）
  return report;
}

// 运行
main()
  .then((report) => {
    console.log('\n✅ 集成测试完成');
    if (DRY_RUN) {
      console.log('   提示：使用 node integration-test.js（不带 --dry-run）进行实际 Discord 推送测试');
    }
    process.exit(0);
  })
  .catch((err) => {
    console.error('\n❌ 集成测试失败:', err.message);
    process.exit(1);
  });

// 导出用于其他模块调用
module.exports = { main, runPipeline, fetchEmailsFromIMAP };
