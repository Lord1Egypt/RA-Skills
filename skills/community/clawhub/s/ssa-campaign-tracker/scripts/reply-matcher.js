#!/usr/bin/env node

/**
 * Reply Matcher - 回复匹配和状态更新脚本
 * 
 * 功能：
 * 1. 监听 IMAP 收件箱新邮件（或读取 auto-capture.js 的捕获记录）
 * 2. 根据发件人邮箱/邮件主题/时间窗口匹配到 archive 中的 sent_records
 * 3. 更新匹配记录的状态（sent → replied）
 * 4. 记录回复时间、回复类型（positive/negative/neutral，调用 task-001 intent 识别）
 * 5. 更新转化漏斗状态（sent → replied → qualified）
 * 6. 支持手动触发和自动触发两种模式
 * 7. 支持 dry-run 模式（预览将匹配的回复）
 * 8. 记录匹配日志（成功/失败/未匹配）
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ==================== 配置 ====================

const CONFIG = {
  // campaign-tracker 根目录
  trackerRoot: path.join(__dirname, '..'),
  
  // 归档目录（sent_records）
  archiveDir: path.join(__dirname, '..', 'archive'),
  
  // 回复追踪目录（reply_tracking）
  replyTrackingDir: path.join(__dirname, '..', 'reply-tracking'),
  
  // 日志目录
  logsDir: path.join(__dirname, '..', 'logs'),
  
  // task-001 邮件系统目录
  emailSystemDir: process.env.EMAIL_SKILL_ROOT || path.join(__dirname, '..', '..', 'imap-smtp-email'),
  
  // 已处理回复文件（去重用）
  processedRepliesFile: process.env.CAMPAIGN_TRACKER_PROCESSED_FILE || '/tmp/campaign-tracker-processed-replies.json',
  
  // 匹配时间窗口（小时）
  matchTimeWindowHours: 72,
  
  // 主题相似度阈值（0-1）
  subjectSimilarityThreshold: 0.6
};

// 确保目录存在
[CONFIG.archiveDir, CONFIG.replyTrackingDir, CONFIG.logsDir].forEach(dir => {
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
  const logFile = path.join(CONFIG.logsDir, `reply-matcher-${new Date().toISOString().split('T')[0]}.log`);
  fs.appendFileSync(logFile, logLine + '\n');
}

// ==================== UUID 生成 ====================

function generateUUID() {
  return crypto.randomUUID();
}

// ==================== 已处理回复管理 ====================

function loadProcessedReplies() {
  try {
    if (fs.existsSync(CONFIG.processedRepliesFile)) {
      const data = fs.readFileSync(CONFIG.processedRepliesFile, 'utf8');
      return JSON.parse(data);
    }
  } catch (e) {
    log(`加载已处理回复失败：${e.message}`, 'WARN');
  }
  return {};
}

function saveProcessedReply(messageId, metadata = {}) {
  try {
    const replies = loadProcessedReplies();
    replies[messageId] = {
      processed_at: new Date().toISOString(),
      ...metadata
    };
    fs.writeFileSync(CONFIG.processedRepliesFile, JSON.stringify(replies, null, 2));
    return true;
  } catch (e) {
    log(`保存已处理回复失败：${e.message}`, 'WARN');
    return false;
  }
}

function isReplyProcessed(messageId) {
  const replies = loadProcessedReplies();
  return !!replies[messageId];
}

// ==================== 加载归档的发送记录 ====================

/**
 * 从归档目录加载所有 sent_records
 * 返回 Map: record_id -> record
 */
function loadSentRecords() {
  const records = new Map();
  const recordsByEmail = new Map(); // 用于快速查找：email -> [records]
  
  if (!fs.existsSync(CONFIG.archiveDir)) {
    log('归档目录不存在', 'WARN');
    return { records, recordsByEmail };
  }
  
  const files = fs.readdirSync(CONFIG.archiveDir);
  for (const file of files) {
    if (!file.endsWith('.jsonl')) continue;
    
    const filepath = path.join(CONFIG.archiveDir, file);
    try {
      const lines = fs.readFileSync(filepath, 'utf8').trim().split('\n');
      for (const line of lines) {
        if (!line.trim()) continue;
        const record = JSON.parse(line);
        records.set(record.record_id, record);
        
        // 建立邮箱索引
        const email = record.recipient_email?.toLowerCase();
        if (email) {
          if (!recordsByEmail.has(email)) {
            recordsByEmail.set(email, []);
          }
          recordsByEmail.get(email).push(record);
        }
      }
    } catch (e) {
      log(`读取归档文件失败 ${file}: ${e.message}`, 'WARN');
    }
  }
  
  log(`加载了 ${records.size} 条发送记录`);
  return { records, recordsByEmail };
}

// ==================== 加载收件箱邮件 ====================

/**
 * 从 task-001 系统读取收件箱邮件（回复）
 * 模拟：读取 auto-capture 捕获的邮件
 */
function loadInboxEmails() {
  const emails = [];
  
  // 尝试读取 auto-capture 的捕获记录
  const autoCaptureDir = path.join(CONFIG.emailSystemDir, 'captured');
  if (fs.existsSync(autoCaptureDir)) {
    const files = fs.readdirSync(autoCaptureDir);
    for (const file of files) {
      if (!file.endsWith('.json')) continue;
      
      try {
        const filepath = path.join(autoCaptureDir, file);
        const emailData = JSON.parse(fs.readFileSync(filepath, 'utf8'));
        
        // 只处理收件箱邮件（非发送的）
        if (emailData.direction === 'incoming' || emailData.folder === 'INBOX') {
          emails.push({
            uid: emailData.uid || file.replace('.json', ''),
            message_id: emailData.message_id,
            subject: emailData.subject,
            from: emailData.from,
            to: emailData.to,
            date: emailData.date,
            body: emailData.body || emailData.text || '',
            is_reply: emailData.subject?.startsWith('Re:') || emailData.subject?.startsWith('RE:'),
            in_reply_to: emailData.in_reply_to,
            references: emailData.references
          });
        }
      } catch (e) {
        log(`读取捕获邮件失败 ${file}: ${e.message}`, 'WARN');
      }
    }
  }
  
  // 如果没有 auto-capture 数据，尝试读取 reviews-pending 中的 incoming 邮件
  const reviewsDir = path.join(CONFIG.emailSystemDir, 'reviews-pending');
  if (fs.existsSync(reviewsDir) && emails.length === 0) {
    const files = fs.readdirSync(reviewsDir);
    for (const file of files) {
      if (!file.endsWith('.json')) continue;
      
      try {
        const filepath = path.join(reviewsDir, file);
        const review = JSON.parse(fs.readFileSync(filepath, 'utf8'));
        
        if (review.email && review.email.folder === 'INBOX') {
          emails.push({
            uid: review.reviewId,
            message_id: review.email.message_id,
            subject: review.email.subject,
            from: review.email.from,
            to: review.email.to,
            date: review.email.date,
            body: review.email.body || review.email.text || '',
            is_reply: review.email.subject?.startsWith('Re:') || review.email.subject?.startsWith('RE:'),
            in_reply_to: review.email.in_reply_to,
            references: review.email.references
          });
        }
      } catch (e) {
        log(`读取 review 邮件失败 ${file}: ${e.message}`, 'WARN');
      }
    }
  }
  
  log(`加载了 ${emails.length} 条收件箱邮件`);
  return emails;
}

// ==================== 意图识别集成 ====================

/**
 * 调用 task-001 的 intent-recognition 模块
 * 返回回复类型分类
 */
async function classifyReplyIntent(subject, body) {
  try {
    const intentModule = require(path.join(CONFIG.emailSystemDir, 'scripts', 'intent-recognition.js'));
    const result = await intentModule.classifyIntent(subject, body);
    
    // 映射到 reply_type
    const intentToReplyType = {
      'inquiry': 'inquiry',
      'quote_request': 'positive',
      'order': 'positive',
      'sample_request': 'positive',
      'complaint': 'negative',
      'unsubscribe': 'negative',
      'out_of_office': 'out_of_office',
      'spam': 'negative',
      'unknown': 'neutral'
    };
    
    const replyType = intentToReplyType[result.intent] || 'neutral';
    
    return {
      reply_type: replyType,
      detected_intent: result.intent,
      confidence_score: result.confidence,
      auto_classified_by_intent: result.method === 'llm',
      key_entities: result.key_entities || [],
      language: result.language
    };
  } catch (e) {
    log(`意图识别失败：${e.message}`, 'WARN');
    // 降级：基于关键词简单分类
    return classifyReplyByKeywords(subject, body);
  }
}

/**
 * 降级方案：基于关键词的简单分类
 */
function classifyReplyByKeywords(subject, body) {
  const text = `${subject} ${body}`.toLowerCase();
  
  if (text.includes('out of office') || text.includes('vacation') || text.includes('away')) {
    return {
      reply_type: 'out_of_office',
      detected_intent: 'out_of_office',
      confidence_score: 0.8,
      auto_classified_by_intent: false
    };
  }
  
  if (text.includes('unsubscribe') || text.includes('remove') || text.includes('stop')) {
    return {
      reply_type: 'negative',
      detected_intent: 'unsubscribe',
      confidence_score: 0.7,
      auto_classified_by_intent: false
    };
  }
  
  if (text.includes('price') || text.includes('quote') || text.includes('order') || 
      text.includes('sample') || text.includes('interested') || text.includes('buy')) {
    return {
      reply_type: 'positive',
      detected_intent: 'inquiry',
      confidence_score: 0.6,
      auto_classified_by_intent: false
    };
  }
  
  if (text.includes('complaint') || text.includes('problem') || text.includes('issue') || 
      text.includes('wrong') || text.includes('defect')) {
    return {
      reply_type: 'negative',
      detected_intent: 'complaint',
      confidence_score: 0.6,
      auto_classified_by_intent: false
    };
  }
  
  return {
    reply_type: 'neutral',
    detected_intent: 'unknown',
    confidence_score: 0.3,
    auto_classified_by_intent: false
  };
}

// ==================== 匹配逻辑 ====================

/**
 * 计算主题相似度
 * 简化版：去除 Re:/RE: 前缀后比较
 */
function normalizeSubject(subject) {
  if (!subject) return '';
  return subject
    .replace(/^(Re:|RE:|Fwd:|FWD:)\s*/i, '')
    .trim()
    .toLowerCase();
}

/**
 * 简单主题相似度计算
 */
function subjectSimilarity(subject1, subject2) {
  const norm1 = normalizeSubject(subject1);
  const norm2 = normalizeSubject(subject2);
  
  if (norm1 === norm2) return 1.0;
  
  // 检查是否包含
  if (norm1.includes(norm2) || norm2.includes(norm1)) {
    return 0.8;
  }
  
  // 简单词重叠
  const words1 = new Set(norm1.split(/\s+/));
  const words2 = new Set(norm2.split(/\s+/));
  
  let overlap = 0;
  for (const word of words1) {
    if (words2.has(word) && word.length > 3) {
      overlap++;
    }
  }
  
  const totalWords = Math.max(words1.size, words2.size);
  return totalWords > 0 ? overlap / totalWords : 0;
}

/**
 * 匹配回复到发送记录
 * 优先级：
 * 1. In-Reply-To 头匹配（最准确）
 * 2. 发件人邮箱 + 主题相似度 + 时间窗口
 */
function matchReplyToSentRecord(email, recordsByEmail, sentRecords) {
  const fromEmail = email.from?.email || email.from?.toLowerCase() || '';
  const replyTime = new Date(email.date);
  
  log(`尝试匹配回复：${fromEmail} - ${email.subject?.slice(0, 50)}`);
  
  // 优先级 1: 检查 In-Reply-To 头
  if (email.in_reply_to) {
    // 尝试直接匹配 message_id（如果 sent_records 中有存储）
    for (const [recordId, record] of sentRecords) {
      if (record.message_id && record.message_id === email.in_reply_to) {
        log(`✓ 通过 In-Reply-To 匹配到记录：${recordId}`);
        return { record, matchMethod: 'in_reply_to', confidence: 1.0 };
      }
    }
  }
  
  // 优先级 2: 发件人邮箱 + 主题 + 时间窗口匹配
  const candidateEmails = recordsByEmail.get(fromEmail) || [];
  
  if (candidateEmails.length === 0) {
    log(`⚠️ 未找到发件人 ${fromEmail} 的发送记录`);
    return null;
  }
  
  let bestMatch = null;
  let bestScore = 0;
  
  for (const record of candidateEmails) {
    let score = 0;
    
    // 时间窗口检查
    const sentTime = new Date(record.sent_timestamp);
    const hoursDiff = Math.abs(replyTime - sentTime) / (1000 * 60 * 60);
    
    if (hoursDiff > CONFIG.matchTimeWindowHours) {
      continue; // 超出时间窗口
    }
    
    // 时间越近分数越高
    score += Math.max(0, 1 - hoursDiff / CONFIG.matchTimeWindowHours) * 0.4;
    
    // 主题相似度
    const subjectSim = subjectSimilarity(email.subject, record.subject_line);
    if (subjectSim >= CONFIG.subjectSimilarityThreshold) {
      score += subjectSim * 0.5;
    }
    
    // 公司名匹配（如果有）
    if (record.company_name && email.from?.name) {
      if (email.from.name.toLowerCase().includes(record.company_name.toLowerCase()) ||
          record.company_name.toLowerCase().includes(email.from.name.toLowerCase())) {
        score += 0.1;
      }
    }
    
    if (score > bestScore) {
      bestScore = score;
      bestMatch = record;
    }
  }
  
  if (bestMatch && bestScore >= CONFIG.subjectSimilarityThreshold) {
    log(`✓ 匹配到记录：${bestMatch.record_id} (confidence: ${bestScore.toFixed(2)})`);
    return { record: bestMatch, matchMethod: 'email_subject_time', confidence: bestScore };
  }
  
  log(`⚠️ 未找到匹配的发送记录`);
  return null;
}

// ==================== 更新记录状态 ====================

/**
 * 更新 sent_record 状态为 replied
 */
function updateSentRecordStatus(recordId, replyInfo) {
  // 找到记录所在的归档文件
  const files = fs.readdirSync(CONFIG.archiveDir);
  for (const file of files) {
    if (!file.endsWith('.jsonl')) continue;
    
    const filepath = path.join(CONFIG.archiveDir, file);
    const lines = fs.readFileSync(filepath, 'utf8').trim().split('\n');
    let updated = false;
    let newLines = [];
    
    for (const line of lines) {
      if (!line.trim()) continue;
      const record = JSON.parse(line);
      
      if (record.record_id === recordId) {
        // 更新状态
        record.reply_tracking = {
          reply_received: true,
          reply_timestamp: replyInfo.reply_timestamp,
          reply_type: replyInfo.reply_type,
          detected_intent: replyInfo.detected_intent,
          confidence_score: replyInfo.confidence_score,
          auto_classified_by_intent: replyInfo.auto_classified_by_intent,
          reply_snippet: replyInfo.reply_snippet,
          requires_manual_review: ['positive', 'inquiry'].includes(replyInfo.reply_type),
          follow_up_action: determineFollowUpAction(replyInfo.reply_type, replyInfo.detected_intent)
        };
        
        // 更新转化漏斗状态
        record.conversion_funnel_stage = 'replied';
        updated = true;
      }
      
      newLines.push(JSON.stringify(record));
    }
    
    if (updated) {
      fs.writeFileSync(filepath, newLines.join('\n') + '\n');
      log(`✓ 更新记录 ${recordId} 状态为 replied`);
      return true;
    }
  }
  
  log(`⚠️ 未找到记录 ${recordId} 进行更新`, 'WARN');
  return false;
}

/**
 * 根据回复类型确定后续动作
 */
function determineFollowUpAction(replyType, intent) {
  const actionMap = {
    'positive': 'quote',
    'inquiry': 'quote',
    'quote_request': 'quote',
    'sample_request': 'sample',
    'order': 'close',
    'neutral': 'call',
    'negative': 'discard',
    'out_of_office': 'call',
    'complaint': 'call',
    'unsubscribe': 'discard',
    'unknown': 'call'
  };
  
  return actionMap[intent] || actionMap[replyType] || 'call';
}

/**
 * 创建回复追踪记录
 */
function createReplyTrackingRecord(matchResult, email, intentResult) {
  const trackingRecord = {
    reply_id: generateUUID(),
    sent_record_id: matchResult.record.record_id,
    campaign_id: matchResult.record.campaign_id,
    reply_received: true,
    reply_timestamp: new Date(email.date).toISOString(),
    reply_type: intentResult.reply_type,
    detected_intent: intentResult.detected_intent,
    confidence_score: intentResult.confidence_score,
    auto_classified_by_intent: intentResult.auto_classified_by_intent,
    reply_snippet: (email.body || '').slice(0, 200),
    requires_manual_review: ['positive', 'inquiry'].includes(intentResult.reply_type),
    follow_up_action: intentResult.follow_up_action || determineFollowUpAction(intentResult.reply_type, intentResult.detected_intent),
    matched_by: matchResult.matchMethod,
    match_confidence: matchResult.confidence,
    created_at: new Date().toISOString()
  };
  
  // 保存到 reply-tracking 目录（按 campaign_id 分组）
  const trackingFile = path.join(CONFIG.replyTrackingDir, `${trackingRecord.campaign_id || 'unknown'}.jsonl`);
  fs.appendFileSync(trackingFile, JSON.stringify(trackingRecord) + '\n');
  
  log(`✓ 创建回复追踪记录：${trackingRecord.reply_id}`);
  return trackingRecord;
}

// ==================== 主处理流程 ====================

async function processReplies(dryRun = false) {
  log(`========== 开始回复匹配 (dryRun: ${dryRun}) ==========`);
  
  // 加载发送记录
  const { records, recordsByEmail } = loadSentRecords();
  if (records.size === 0) {
    log('⚠️ 没有发送记录，跳过匹配', 'WARN');
    return { matched: 0, skipped: 0, failed: 0 };
  }
  
  // 加载收件箱邮件
  const inboxEmails = loadInboxEmails();
  if (inboxEmails.length === 0) {
    log('⚠️ 没有收件箱邮件，跳过匹配', 'WARN');
    return { matched: 0, skipped: 0, failed: 0 };
  }
  
  const stats = { matched: 0, skipped: 0, failed: 0 };
  
  for (const email of inboxEmails) {
    // 检查是否已处理
    if (isReplyProcessed(email.uid)) {
      log(`⊘ 跳过已处理回复：${email.uid}`);
      stats.skipped++;
      continue;
    }
    
    // 只处理回复邮件
    if (!email.is_reply) {
      log(`⊘ 跳过非回复邮件：${email.subject}`);
      stats.skipped++;
      continue;
    }
    
    // 匹配到发送记录
    const matchResult = matchReplyToSentRecord(email, recordsByEmail, records);
    
    if (!matchResult) {
      log(`⊘ 未匹配到发送记录：${email.from?.email || 'unknown'}`);
      stats.failed++;
      continue;
    }
    
    if (dryRun) {
      log(`[DRY-RUN] 将匹配：${matchResult.record.record_id} -> ${email.subject}`);
      stats.matched++;
      continue;
    }
    
    // 进行意图识别
    const intentResult = await classifyReplyIntent(email.subject, email.body);
    intentResult.follow_up_action = determineFollowUpAction(intentResult.reply_type, intentResult.detected_intent);
    
    // 更新发送记录状态
    const updateSuccess = updateSentRecordStatus(matchResult.record.record_id, {
      reply_timestamp: new Date(email.date).toISOString(),
      reply_type: intentResult.reply_type,
      detected_intent: intentResult.detected_intent,
      confidence_score: intentResult.confidence_score,
      auto_classified_by_intent: intentResult.auto_classified_by_intent,
      reply_snippet: (email.body || '').slice(0, 200)
    });
    
    if (updateSuccess) {
      // 创建回复追踪记录
      createReplyTrackingRecord(matchResult, email, intentResult);
      
      // 标记为已处理
      saveProcessedReply(email.uid, {
        matched_record_id: matchResult.record.record_id,
        reply_type: intentResult.reply_type,
        processed_at: new Date().toISOString()
      });
      
      stats.matched++;
    } else {
      stats.failed++;
    }
  }
  
  log(`========== 回复匹配完成：匹配=${stats.matched}, 跳过=${stats.skipped}, 失败=${stats.failed} ==========`);
  return stats;
}

// ==================== CLI 入口 ====================

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run') || args.includes('-n');
  const autoMode = args.includes('--auto') || args.includes('-a');
  
  log(`启动参数：dryRun=${dryRun}, autoMode=${autoMode}`);
  
  try {
    const stats = await processReplies(dryRun);
    
    if (autoMode) {
      // 自动模式：输出 JSON 结果供其他系统消费
      console.log(JSON.stringify(stats, null, 2));
    }
    
    process.exit(stats.failed > 0 ? 1 : 0);
  } catch (e) {
    log(`❌ 执行失败：${e.message}`, 'ERROR');
    console.error(e.stack);
    process.exit(1);
  }
}

// 运行
if (require.main === module) {
  main();
}

module.exports = {
  processReplies,
  matchReplyToSentRecord,
  classifyReplyIntent,
  loadSentRecords,
  loadInboxEmails,
  CONFIG
};
