#!/usr/bin/env node

/**
 * Archive Sent Records - 发送记录自动归档脚本
 * 
 * 功能：
 * 1. 监听 task-001 邮件发送事件（或读取已发送邮件日志）
 * 2. 提取发送记录字段（recipient, template, campaign_id, subject, timestamp, sales_owner）
 * 3. 生成唯一 record_id（UUID 格式）
 * 4. 保存到归档文件（JSONL 或 SQLite，按 campaign_id 分组）
 * 5. 支持手动触发和自动触发两种模式
 * 6. 支持 dry-run 模式（预览将归档的记录）
 * 7. 记录归档日志（成功/失败）
 */

const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');
const crypto = require('crypto');

// ==================== 配置 ====================

const CONFIG = {
  // task-001 邮件系统目录
  emailSystemDir: process.env.EMAIL_SKILL_ROOT || path.join(__dirname, '..', '..', 'imap-smtp-email'),
  
  // 归档目录
  archiveDir: path.join(__dirname, '..', 'archive'),
  
  // 日志目录
  logsDir: path.join(__dirname, '..', 'logs'),
  
  // 已处理记录文件（去重用）
  processedFile: process.env.CAMPAIGN_TRACKER_PROCESSED_FILE || '/tmp/campaign-tracker-processed.json',
  
  // 跟踪 schema 路径
  trackingSchema: path.join(__dirname, '..', 'config', 'tracking-schema.json')
};

// 确保目录存在
[CONFIG.archiveDir, CONFIG.logsDir].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// ==================== 日志工具 ====================

function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] [${level}] ${message}`;
  console.log(logLine);
  
  // 写入日志文件
  const logFile = path.join(CONFIG.logsDir, `archive-sent-${new Date().toISOString().split('T')[0]}.log`);
  fs.appendFileSync(logFile, logLine + '\n');
}

// ==================== UUID 生成 ====================

/**
 * 生成 UUID v4
 */
function generateUUID() {
  return crypto.randomUUID();
}

// ==================== 已处理记录管理 ====================

/**
 * 加载已处理记录
 */
function loadProcessedRecords() {
  try {
    if (fs.existsSync(CONFIG.processedFile)) {
      const data = fs.readFileSync(CONFIG.processedFile, 'utf8');
      return JSON.parse(data);
    }
  } catch (e) {
    log(`加载已处理记录失败：${e.message}`, 'WARN');
  }
  return {};
}

/**
 * 保存已处理记录
 */
function saveProcessedRecord(uid, metadata = {}) {
  try {
    const records = loadProcessedRecords();
    records[uid] = {
      processed_at: new Date().toISOString(),
      ...metadata
    };
    fs.writeFileSync(CONFIG.processedFile, JSON.stringify(records, null, 2));
    return true;
  } catch (e) {
    log(`保存已处理记录失败：${e.message}`, 'WARN');
    return false;
  }
}

/**
 * 检查记录是否已处理
 */
function isProcessed(uid) {
  const records = loadProcessedRecords();
  return !!records[uid];
}

// ==================== 邮件发送记录读取 ====================

/**
 * 从 task-001 系统读取已发送/待审阅邮件
 */
function loadSentEmails() {
  const emails = [];
  
  // 读取 reviews-pending 目录（已生成草稿的邮件）
  const reviewsDir = path.join(CONFIG.emailSystemDir, 'reviews-pending');
  if (fs.existsSync(reviewsDir)) {
    const files = fs.readdirSync(reviewsDir);
    for (const file of files) {
      if (!file.endsWith('.json')) continue;
      
      try {
        const filepath = path.join(reviewsDir, file);
        const review = JSON.parse(fs.readFileSync(filepath, 'utf8'));
        
        // 提取邮件数据
        if (review.email && review.draft) {
          emails.push({
            uid: review.reviewId,
            source_file: filepath,
            subject: review.email.subject,
            from: review.email.from,
            to: null, // 需要从草稿或原始邮件获取
            date: review.email.date,
            template_id: review.email.intent ? `template-${review.email.intent}` : null,
            draft_content: review.draft.content,
            status: 'pending_review'
          });
        }
      } catch (e) {
        log(`读取 review 文件失败 ${file}: ${e.message}`, 'WARN');
      }
    }
  }
  
  // 读取 drafts 目录（已生成的草稿）
  const draftsDir = path.join(CONFIG.emailSystemDir, 'drafts');
  if (fs.existsSync(draftsDir)) {
    const files = fs.readdirSync(draftsDir);
    for (const file of files) {
      if (!file.endsWith('.json')) continue;
      
      try {
        const filepath = path.join(draftsDir, file);
        const draft = JSON.parse(fs.readFileSync(filepath, 'utf8'));
        
        emails.push({
          uid: `draft-${file}`,
          source_file: filepath,
          subject: draft.subject || '(未知)',
          from: draft.from || null,
          to: draft.to || null,
          date: draft.date || new Date().toISOString(),
          template_id: draft.template_id || null,
          draft_content: draft.content || draft.body || null,
          status: 'draft'
        });
      } catch (e) {
        log(`读取 draft 文件失败 ${file}: ${e.message}`, 'WARN');
      }
    }
  }
  
  return emails;
}

/**
 * 模拟已发送邮件数据（用于测试）
 */
function getMockSentEmails() {
  return [
    {
      uid: 'mock-001',
      subject: 'Inquiry about HDMI cables - MOQ and pricing',
      from: 'wilson@farreach-electronic.com',
      to: 'john@abctrading.com',
      date: new Date().toISOString(),
      template_id: 'template-inquiry-001',
      campaign_id: 'campaign-2026-q1',
      recipient_name: 'John Smith',
      company_name: 'ABC Trading Ltd',
      sales_owner: 'wilson',
      status: 'sent'
    },
    {
      uid: 'mock-002',
      subject: 'Follow-up: DP Cable quotation QT-2026-0042',
      from: 'wilson@farreach-electronic.com',
      to: 'sales@xyzelec.com',
      date: new Date().toISOString(),
      template_id: 'template-followup-002',
      campaign_id: 'campaign-2026-q1',
      recipient_name: 'Sarah Johnson',
      company_name: 'XYZ Electronics',
      sales_owner: 'wilson',
      status: 'sent'
    },
    {
      uid: 'mock-003',
      subject: 'USB-C Cable sample shipped - tracking SF1234567890',
      from: 'wilson@farreach-electronic.com',
      to: 'purchasing@globaltech.com',
      date: new Date().toISOString(),
      template_id: 'template-sample-001',
      campaign_id: 'campaign-2026-q1',
      recipient_name: 'Mike Chen',
      company_name: 'Global Tech Inc',
      sales_owner: 'wilson',
      status: 'sent'
    }
  ];
}

// ==================== 记录转换 ====================

/**
 * 将邮件数据转换为 sent_records 格式
 */
function convertToSentRecord(email, options = {}) {
  const {
    campaign_id = options.campaign_id || 'campaign-default',
    template_variant = options.template_variant || null,
    send_status = 'sent',
    error_message = null
  } = options;
  
  // 从邮箱提取收件人信息
  const recipientEmail = email.to || email.recipient_email;
  const recipientName = email.recipient_name || extractNameFromEmail(recipientEmail);
  const companyName = email.company_name || extractCompanyFromEmail(recipientEmail);
  
  // 生成唯一 record_id
  const record_id = generateUUID();
  
  return {
    record_id,
    campaign_id,
    recipient_email: recipientEmail,
    recipient_name: recipientName,
    company_name: companyName,
    template_id: email.template_id || 'template-unknown',
    template_variant,
    subject_line: email.subject,
    sent_timestamp: email.date || new Date().toISOString(),
    sales_owner: email.sales_owner || 'wilson',
    send_status,
    error_message,
    // 额外元数据
    _source_uid: email.uid,
    _source_file: email.source_file
  };
}

/**
 * 从邮箱地址提取人名（简单实现）
 */
function extractNameFromEmail(email) {
  if (!email) return null;
  const match = email.match(/^([^@]+)@/);
  return match ? match[1].replace(/[._-]/g, ' ').trim() : null;
}

/**
 * 从邮箱地址提取公司名（简单实现）
 */
function extractCompanyFromEmail(email) {
  if (!email) return null;
  const domain = email.match(/@([^.]+)/);
  return domain ? domain[1].charAt(0).toUpperCase() + domain[1].slice(1) : null;
}

// ==================== 归档保存 ====================

/**
 * 保存记录到归档文件（JSONL 格式，按 campaign_id 分组）
 */
function saveToArchive(record) {
  const campaignId = record.campaign_id || 'campaign-unknown';
  const archiveFile = path.join(CONFIG.archiveDir, `${campaignId}.jsonl`);
  
  const line = JSON.stringify(record) + '\n';
  fs.appendFileSync(archiveFile, line, 'utf8');
  
  log(`记录已归档：${record.record_id} → ${path.basename(archiveFile)}`);
  
  return archiveFile;
}

/**
 * 批量保存记录
 */
function saveBatchToArchive(records) {
  const byCampaign = {};
  
  for (const record of records) {
    const campaignId = record.campaign_id || 'campaign-unknown';
    if (!byCampaign[campaignId]) {
      byCampaign[campaignId] = [];
    }
    byCampaign[campaignId].push(record);
  }
  
  const savedFiles = [];
  for (const [campaignId, campaignRecords] of Object.entries(byCampaign)) {
    const archiveFile = path.join(CONFIG.archiveDir, `${campaignId}.jsonl`);
    const lines = campaignRecords.map(r => JSON.stringify(r)).join('\n') + '\n';
    fs.appendFileSync(archiveFile, lines, 'utf8');
    savedFiles.push({ campaign: campaignId, file: archiveFile, count: campaignRecords.length });
    log(`批量归档：${campaignRecords.length} 条记录 → ${path.basename(archiveFile)}`);
  }
  
  return savedFiles;
}

// ==================== 主归档逻辑 ====================

/**
 * 执行归档
 */
async function runArchive(options = {}) {
  const {
    dryRun = false,
    useMock = false,
    campaign_id = null,
    template_variant = null
  } = options;
  
  log('='.repeat(60));
  log('Archive Sent Records - 发送记录自动归档');
  log(`模式：${dryRun ? 'DRY-RUN' : 'LIVE'} | 数据源：${useMock ? 'MOCK' : 'EMAIL-SYSTEM'}`);
  log('='.repeat(60));
  
  const results = {
    total_emails: 0,
    archived: 0,
    skipped: 0,
    failed: 0,
    details: []
  };
  
  try {
    // 1. 加载邮件数据
    let emails = useMock ? getMockSentEmails() : loadSentEmails();
    
    // 如果指定了 campaign_id，只处理这个活动的邮件
    if (campaign_id) {
      emails = emails.filter(e => e.campaign_id === campaign_id);
    }
    
    results.total_emails = emails.length;
    log(`找到 ${emails.length} 封邮件`);
    
    if (emails.length === 0) {
      log('没有需要归档的邮件');
      return { success: true, ...results };
    }
    
    log('-'.repeat(60));
    
    // 2. 逐个处理邮件
    const recordsToArchive = [];
    
    for (const email of emails) {
      log(`处理邮件：${email.uid}`);
      log(`  主题：${email.subject}`);
      log(`  收件人：${email.to || email.recipient_email || '(未知)'}`);
      log(`  模板：${email.template_id || '(未知)'}`);
      
      // 检查是否已处理
      if (isProcessed(email.uid)) {
        log(`  跳过：已处理`);
        results.skipped++;
        results.details.push({
          uid: email.uid,
          status: 'skipped',
          reason: 'already_processed'
        });
        continue;
      }
      
      // 转换为 sent_record 格式
      const record = convertToSentRecord(email, {
        campaign_id: email.campaign_id || campaign_id,
        template_variant,
        send_status: email.status === 'sent' ? 'sent' : 'pending'
      });
      
      if (dryRun) {
        log(`  [DRY-RUN] 将归档记录：${record.record_id}`);
        results.archived++;
        results.details.push({
          uid: email.uid,
          status: 'dry_run',
          record_id: record.record_id,
          campaign_id: record.campaign_id
        });
        continue;
      }
      
      // 保存到归档
      saveToArchive(record);
      
      // 记录已处理
      saveProcessedRecord(email.uid, {
        record_id: record.record_id,
        campaign_id: record.campaign_id
      });
      
      results.archived++;
      results.details.push({
        uid: email.uid,
        status: 'archived',
        record_id: record.record_id,
        campaign_id: record.campaign_id
      });
    }
    
    // 3. 输出摘要
    log('='.repeat(60));
    log('归档完成摘要');
    log('='.repeat(60));
    log(`邮件总数：${results.total_emails}`);
    log(`归档成功：${results.archived}`);
    log(`跳过：${results.skipped}`);
    log(`失败：${results.failed}`);
    
    if (dryRun) {
      log('');
      log('DRY-RUN 模式：未实际写入归档文件');
    }
    
    return { success: true, ...results };
    
  } catch (error) {
    log(`执行失败：${error.message}`, 'ERROR');
    return {
      success: false,
      error: error.message,
      ...results
    };
  }
}

// ==================== CLI 入口 ====================

function main() {
  const args = process.argv.slice(2);
  
  const options = {
    dryRun: args.includes('--dry-run') || args.includes('-n'),
    useMock: args.includes('--mock') || args.includes('-m'),
    campaign_id: null,
    template_variant: null
  };
  
  // 解析参数
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--campaign' && args[i + 1]) {
      options.campaign_id = args[i + 1];
      i++;
    } else if (args[i] === '--variant' && args[i + 1]) {
      options.template_variant = args[i + 1];
      i++;
    }
  }
  
  runArchive(options).then(result => {
    // 输出 JSON 结果（便于 cron 调用）
    console.log('\n--- JSON RESULT ---');
    console.log(JSON.stringify(result, null, 2));
    
    // 退出码
    process.exit(result.success ? 0 : 1);
  }).catch(error => {
    log(`致命错误：${error.message}`, 'ERROR');
    process.exit(1);
  });
}

// ==================== 导出 ====================

module.exports = {
  runArchive,
  loadSentEmails,
  convertToSentRecord,
  saveToArchive,
  saveBatchToArchive,
  loadProcessedRecords,
  saveProcessedRecord,
  isProcessed,
  generateUUID,
  CONFIG
};

// 直接运行时执行
if (require.main === module) {
  main();
}
