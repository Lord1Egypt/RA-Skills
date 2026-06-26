#!/usr/bin/env node

/**
 * 邮件自动捕获系统
 * 功能：
 * 1. 读取新邮件
 * 2. 解析发件人信息
 * 3. 关联 OKKI 客户档案
 * 4. 保存邮件到本地/Obsidian
 */

const Imap = require('imap');
const { simpleParser } = require('mailparser');
const fs = require('fs');
const path = require('path');
// Load default .env, then override with profile if specified
require('dotenv').config({ path: '.env' });
const _profile = process.env.EMAIL_PROFILE || (process.argv.find(a => a.startsWith('--profile=')) || '').split('=')[1] || (process.argv.indexOf('--profile') > -1 ? process.argv[process.argv.indexOf('--profile') + 1] : '');
if (_profile) {
  const _pPath = path.resolve(__dirname, `profiles/${_profile}.env`);
  if (fs.existsSync(_pPath)) {
    require('dotenv').config({ path: _pPath, override: true });
    console.log(`[auto-capture] Using profile: ${_profile}`);
  } else {
    console.error(`[auto-capture] Profile not found: ${_pPath}`);
    process.exit(1);
  }
}

// Intent recognition module
const { classifyIntent, getIntentConfig } = require('./intent-recognition');

// 配置
const CONFIG = {
  outputDir: process.env.MAIL_OUTPUT_DIR || '/Users/wilson/.openclaw/workspace/mail-archive',
  okkiCliPath: process.env.OKKI_CLI_PATH || '/Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki_cli.py',
  vectorSearchPath: process.env.VECTOR_SEARCH_PATH || '/Users/wilson/.openclaw/workspace/vector_store/okki_vector_search_v3.py',
};

// 确保输出目录存在
if (!fs.existsSync(CONFIG.outputDir)) {
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
}

const imapConfig = {
  user: process.env.IMAP_USER,
  password: process.env.IMAP_PASS,
  host: process.env.IMAP_HOST,
  port: parseInt(process.env.IMAP_PORT),
  tls: process.env.IMAP_TLS === 'true',
  connTimeout: 30000,
  authTimeout: 30000,
};

/**
 * 从邮箱地址提取域名
 */
function extractDomain(email) {
  const match = email.match(/@(.+)>?/);
  return match ? match[1] : null;
}

/**
 * 清理文件名
 */
function sanitizeFilename(str) {
  return str.replace(/[^a-zA-Z0-9\u4e00-\u9fa5_-]/g, '_').slice(0, 100);
}

/**
 * 搜索 OKKI 客户
 */
async function searchOkkiCustomer(email, companyName) {
  const domain = extractDomain(email);
  
  console.log(`🔍 搜索 OKKI 客户...`);
  console.log(`   邮箱：${email}`);
  console.log(`   域名：${domain}`);
  console.log(`   公司：${companyName}`);

  try {
    // 使用向量搜索
    const { execSync } = require('child_process');
    
    // 先尝试用域名搜索
    if (domain) {
      try {
        const result = execSync(
          `python3 "${CONFIG.vectorSearchPath}" search "${domain}"`,
          { encoding: 'utf8', timeout: 10000 }
        );
        if (result && result.trim()) {
          console.log(`✅ 通过域名找到客户：${result.slice(0, 200)}`);
          return { source: 'domain', data: result };
        }
      } catch (e) {
        // 忽略错误，继续尝试其他方法
      }
    }

    // 尝试用公司名搜索
    if (companyName) {
      try {
        const result = execSync(
          `python3 "${CONFIG.vectorSearchPath}" search "${companyName}"`,
          { encoding: 'utf8', timeout: 10000 }
        );
        if (result && result.trim()) {
          console.log(`✅ 通过公司名找到客户：${result.slice(0, 200)}`);
          return { source: 'company', data: result };
        }
      } catch (e) {
        // 忽略错误
      }
    }

    console.log('⚠️  未在 OKKI 中找到匹配客户');
    return null;
  } catch (err) {
    console.error(`❌ OKKI 搜索失败：${err.message}`);
    return null;
  }
}

/**
 * 保存邮件到本地
 */
function saveEmail(emailData, okkiMatch) {
  const date = new Date(emailData.date);
  const dateStr = date.toISOString().split('T')[0];
  const timeStr = date.toTimeString().split(' ')[0].replace(/:/g, '-');
  
  const filename = `${dateStr}_${timeStr}_${sanitizeFilename(emailData.subject || 'no-subject')}.md`;
  const filepath = path.join(CONFIG.outputDir, dateStr, filename);
  
  // 创建日期目录
  const dir = path.dirname(filepath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // 生成 Markdown 内容
  let content = `---\n`;
  content += `date: ${emailData.date.toISOString()}\n`;
  content += `from: ${emailData.from}\n`;
  content += `to: ${emailData.to || ''}\n`;
  content += `subject: ${emailData.subject}\n`;
  if (okkiMatch) {
    content += `okki_matched: true\n`;
    content += `okki_source: ${okkiMatch.source}\n`;
  }
  content += `tags: [email, archived]\n`;
  if (emailData.intent) {
    content += `intent: ${emailData.intent}\n`;
    content += `intent_confidence: ${emailData.intentConfidence}\n`;
    content += `auto_draft: ${emailData.autoDraft}\n`;
  }
  content += `---\n\n`;
  
  content += `# ${emailData.subject || '无主题'}\n\n`;
  content += `**发件人:** ${emailData.from}\n`;
  content += `**收件人:** ${emailData.to || ''}\n`;
  content += `**日期:** ${emailData.date.toLocaleString('zh-CN')}\n\n`;
  
  if (emailData.intent) {
    content += `## 🎯 意图识别\n\n`;
    content += `**意图:** ${emailData.intent}\n\n`;
    content += `**置信度:** ${(emailData.intentConfidence * 100).toFixed(1)}%\n\n`;
    if (emailData.keyEntities && emailData.keyEntities.length > 0) {
      content += `**关键实体:** ${emailData.keyEntities.join(', ')}\n\n`;
    }
    content += `**自动草稿:** ${emailData.autoDraft ? '✅ 是' : '❌ 否'}\n\n`;
  }
  
  if (okkiMatch) {
    content += `## 🎯 OKKI 客户匹配\n\n`;
    content += `匹配来源：${okkiMatch.source === 'domain' ? '邮箱域名' : '公司名'}\n\n`;
    content += `\`\`\`\n${okkiMatch.data}\n\`\`\`\n\n`;
  }
  
  content += `---\n\n`;
  content += `${emailData.text || emailData.html?.replace(/<[^>]*>/g, '') || '无正文内容'}\n`;
  
  if (emailData.attachments && emailData.attachments.length > 0) {
    content += `\n\n## 📎 附件 (${emailData.attachments.length})\n\n`;
    emailData.attachments.forEach((att, i) => {
      content += `${i + 1}. ${att.filename} (${(att.size / 1024).toFixed(2)} KB)\n`;
    });
  }

  fs.writeFileSync(filepath, content, 'utf8');
  console.log(`💾 邮件已保存：${filepath}`);
  
  return filepath;
}

/**
 * 检查并处理新邮件
 */
async function checkAndProcessEmails(options = {}) {
  const {
    limit = 10,
    unseenOnly = false,
    processAll = false,
  } = options;

  return new Promise((resolve, reject) => {
    const imap = new Imap(imapConfig);
    const processed = [];

    imap.once('ready', () => {
      imap.openBox('INBOX', false, (err, box) => {
        if (err) {
          reject(err);
          return;
        }

        console.log(`📬 开始检查邮件...`);
        console.log(`   总邮件数：${box.messages.total}`);
        console.log(`   未读邮件：${box.messages.new}`);

        const searchCriteria = unseenOnly ? ['UNSEEN'] : ['ALL'];
        const fetchOptions = {
          bodies: [''],
          markSeen: !processAll, // 除非处理所有，否则标记为已读
        };

        imap.search(searchCriteria, (err, results) => {
          if (err) {
            reject(err);
            return;
          }

          if (results.length === 0) {
            console.log('📭 没有新邮件');
            imap.end();
            resolve([]);
            return;
          }

          // 取最新的 limit 封
          const toProcess = results.slice(-limit).reverse();
          console.log(`📥 将处理 ${toProcess.length} 封邮件\n`);

          const fetch = imap.fetch(toProcess, fetchOptions);
          let processedCount = 0;

          fetch.on('message', (msg) => {
            let buffer = '';
            msg.on('body', (stream) => {
              stream.on('data', (chunk) => {
                buffer += chunk.toString('utf8');
              });
              stream.on('end', async () => {
                try {
                  const parsed = await simpleParser(buffer);
                  
                  console.log(`\n${'='.repeat(60)}`);
                  console.log(`📧 处理邮件 #${processedCount + 1}/${toProcess.length}`);
                  console.log(`   主题：${parsed.subject}`);
                  console.log(`   发件人：${parsed.from?.text}`);
                  
                  // 搜索 OKKI 客户
                  const email = parsed.from?.value?.[0]?.address || '';
                  const companyName = parsed.from?.text?.replace(/<.*>/, '').trim() || '';
                  const okkiMatch = await searchOkkiCustomer(email, companyName);
                  
                  // 意图识别
                  const intentClassification = await classifyIntent(
                    parsed.subject || '',
                    parsed.text || parsed.html || ''
                  );
                  const intentConfig = getIntentConfig(intentClassification.intent);
                  
                  console.log(`🎯 意图配置: ${intentClassification.intent}`);
                  console.log(`   优先级：${intentConfig?.priority || 'normal'}`);
                  console.log(`   自动草稿：${intentConfig?.auto_draft ? '是' : '否'}`);
                  console.log(`   Fallback: ${intentConfig?.fallback_behavior || 'none'}`);
                  
                  // 保存邮件
                  const savedPath = saveEmail({
                    date: parsed.date,
                    from: parsed.from?.text,
                    to: parsed.to?.text,
                    subject: parsed.subject,
                    text: parsed.text,
                    html: parsed.html,
                    attachments: parsed.attachments?.map(a => ({
                      filename: a.filename,
                      size: a.size,
                    })),
                    intent: intentClassification.intent,
                    intentConfidence: intentClassification.confidence,
                    keyEntities: intentClassification.key_entities,
                    language: intentClassification.language,
                    autoDraft: intentConfig?.auto_draft || false,
                  }, okkiMatch);

                  processed.push({
                    uid: msg.seqno,
                    subject: parsed.subject,
                    from: parsed.from?.text,
                    date: parsed.date,
                    savedPath,
                    okkiMatch,
                    intent: intentClassification.intent,
                    intentConfidence: intentClassification.confidence,
                    keyEntities: intentClassification.key_entities,
                    autoDraft: intentConfig?.auto_draft || false,
                  });

                  processedCount++;
                  if (processedCount === toProcess.length) {
                    imap.end();
                    resolve(processed);
                  }
                } catch (e) {
                  console.error('❌ 解析错误:', e.message);
                  processedCount++;
                  if (processedCount === toProcess.length) {
                    imap.end();
                    resolve(processed);
                  }
                }
              });
            });
          });

          fetch.once('error', reject);
        });
      });
    });

    imap.once('error', reject);
    imap.connect();
  });
}

// CLI 入口
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'check';

  try {
    switch (command) {
      case 'check':
        await checkAndProcessEmails({
          limit: parseInt(args[1]) || 10,
          unseenOnly: args.includes('--unseen'),
          processAll: args.includes('--all'),
        });
        break;

      case 'test':
        console.log('🧪 测试 IMAP 连接...');
        await checkAndProcessEmails({ limit: 1, unseenOnly: true });
        break;

      default:
        console.log('用法：node auto-capture.js [check|test] [limit] [--unseen] [--all]');
        console.log('\n示例:');
        console.log('  node auto-capture.js check 10        # 检查最新 10 封邮件');
        console.log('  node auto-capture.js check --unseen  # 只检查未读邮件');
        console.log('  node auto-capture.js test            # 测试连接');
    }
  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
